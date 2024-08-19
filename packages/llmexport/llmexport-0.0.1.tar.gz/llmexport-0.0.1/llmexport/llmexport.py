import os
import sys
import math
import copy
import json
import time
import base64
import logging
import warnings
import argparse
import functools
from typing import Optional, Tuple

from yaspin import yaspin

import onnx
import torch
import numpy as np
from transformers import AutoModel, AutoModelForCausalLM, AutoTokenizer

RESET = "\033[0m"
GREEN = "\033[32;1m"
YELLOW = "\033[33;4m"
EXPORT_LOG = '.export.log'

# ignore warnning info
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.ERROR)

def spinner_run(text='Processing...'):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with yaspin(text=text, color="cyan") as spinner:
                start = time.time()
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    spinner.fail("💥 Failed")
                    print(e)
                    exit(1)
                end = time.time()
                during = f'[{end-start:05.2f} s]'.replace('[0', '[ ')
                padding = ' ' * (64 - len(spinner.text) - len(result))
                spinner.text = f'{spinner.text}{YELLOW}{result}{RESET}{padding}{GREEN}{during}{RESET}'
                spinner.ok("✅ Done")
                return result
        return wrapper
    return decorator

class ModelMapper:
    def __init__(self):
        self.attrs = []
        self.mapper = dict()
        self.regist_models()

    def get_map(self, config):
        model_type = config.model_type
        if model_type == 'chatglm':
            if hasattr(config, 'vocab_size') and config.vocab_size == 130528:
                model_type = 'chatglm'
            else:
                model_type = 'chatglm2'
        if model_type in self.mapper:
            return model_type, self.mapper[model_type]
        return model_type, self.default_map

    def regist(self, model_type, model_map):
        assert('config' in model_map and
               'decoder' in model_map and
               'attention' in model_map)
        self.mapper[model_type] = model_map

    def regist_models(self):
        self.defualt_map()
        # regist models
        self.regist_llama()
        self.regist_qwen()
        self.regist_glm()
        self.regist_glm2()
        self.regist_phi()
        self.regist_gemma2()

    def regist_llama(self):
        llama_map = self.default_map
        self.regist('llama', llama_map)
        self.regist('qwen2', llama_map)
        self.regist('internlm', llama_map)
        baichuan_map = copy.deepcopy(self.default_map)
        baichuan_map[self.attention_key] = {
            'qkv_proj': 'W_pack',
            'o_proj': 'o_proj'
        }
        self.regist('baichuan', baichuan_map)

    def regist_qwen(self):
        qwen_map = {
            'config': {
                'hidden_size': 'hidden_size',
                'num_attention_heads': 'num_attention_heads',
                'num_hidden_layers': 'num_hidden_layers',
                'rope_theta': 'rotary_emb_base',
            },
            'model': {
                'lm_': 'lm_head',
                'embed_': 'transformer.wte',
                'blocks_': 'transformer.h',
                'final_layernorm_': 'transformer.ln_f',
                'visual': 'transformer.visual'
            },
            'decoder': {
                'self_attn': 'attn',
                'mlp': 'mlp',
                'input_layernorm': 'ln_1',
                'post_attention_layernorm': 'ln_2'
            },
            'attention': {
                'qkv_proj': 'c_attn',
                'o_proj': 'c_proj'
            }
        }
        self.regist('qwen', qwen_map)

    def regist_glm(self):
        glm_map = {
            'config': {
                'hidden_size': 'hidden_size',
                'num_attention_heads': 'num_attention_heads',
                'num_hidden_layers': 'num_layers'
            },
            'model': {
                'lm_': 'lm_head',
                'embed_': 'transformer.word_embeddings',
                'blocks_': 'transformer.layers',
                'final_layernorm_': 'transformer.final_layernorm',
            },
            'decoder': {
                'self_attn': 'attention',
                'mlp': 'mlp',
                'input_layernorm': 'input_layernorm',
                'post_attention_layernorm': 'post_attention_layernorm'
            },
            'attention': {
                'qkv_proj': 'query_key_value',
                'o_proj': 'dense'
            }
        }
        self.regist('chatglm', glm_map)

    def regist_glm2(self):
        glm2_map = {
            'config': {
                'hidden_size': 'hidden_size',
                'num_attention_heads': 'num_attention_heads',
                'num_key_value_heads': 'multi_query_group_num',
                'num_hidden_layers': 'num_layers',
            },
            'model': {
                'lm_': 'transformer.output_layer',
                'embed_': 'transformer.embedding.word_embeddings',
                'blocks_': 'transformer.encoder.layers',
                'final_layernorm_': 'transformer.encoder.final_layernorm',
            },
            'decoder': {
                'self_attn': 'self_attention',
                'mlp': 'mlp',
                'input_layernorm': 'input_layernorm',
                'post_attention_layernorm': 'post_attention_layernorm'
            },
            'attention': {
                'qkv_proj': 'query_key_value',
                'o_proj': 'dense'
            }
        }
        self.regist('chatglm2', glm2_map)

    def regist_phi(self):
        phi_map = {
            'config': {
                'hidden_size': 'n_embd',
                'num_attention_heads': 'n_head',
                'num_hidden_layers': 'n_layer',
                'rotary_dim': 'rotary_dim'
            },
            'model': {
                'lm_': 'lm_head.linear',
                'embed_': 'transformer.embd.wte',
                'blocks_': 'transformer.h',
                'final_layernorm_': 'lm_head.ln',
            },
            'decoder': {
                'self_attn': 'mixer',
                'mlp': 'mlp',
                'input_layernorm': 'ln',
            },
            'attention': {
                'qkv_proj': 'Wqkv',
                'o_proj': 'out_proj'
            }
        }
        self.regist('phi-msft', phi_map)

    def regist_gemma2(self):
        gemma2_config = copy.deepcopy(self.default_config)
        gemma2_config['head_dim'] = 'head_dim'
        gemma2_decoder = copy.deepcopy(self.default_decoder)
        gemma2_decoder['pre_feedforward_layernorm'] = 'pre_feedforward_layernorm'
        gemma2_decoder['post_feedforward_layernorm'] = 'post_feedforward_layernorm'
        gemma2_map = {
            'config': gemma2_config,
            'model': self.defualt_model,
            'decoder': gemma2_decoder,
            'attention': self.default_attention
        }
        self.regist('gemma2', gemma2_map)

    def defualt_map(self):
        # default map is `LlamaForCausalLM`
        self.config_key = 'config'
        self.model_key = 'model'
        self.decoder_key = 'decoder'
        self.attention_key = 'attention'
        self.default_config = {
            'hidden_size': 'hidden_size',
            'num_attention_heads': 'num_attention_heads',
            'num_hidden_layers': 'num_hidden_layers',
            'num_key_value_heads': 'num_key_value_heads',
            'rope_theta': 'rope_theta'
        }
        self.defualt_model = {
            'lm_': 'lm_head',
            'embed_': 'model.embed_tokens',
            'blocks_': 'model.layers',
            'final_layernorm_': 'model.norm',
        }
        self.default_decoder = {
            'self_attn': 'self_attn',
            'mlp': 'mlp',
            'input_layernorm': 'input_layernorm',
            'post_attention_layernorm': 'post_attention_layernorm'
        }
        self.default_attention = {
            'q_proj': 'q_proj',
            'k_proj': 'k_proj',
            'v_proj': 'v_proj',
            'o_proj': 'o_proj'
        }
        self.default_map = {
            'config': self.default_config,
            'model': self.defualt_model,
            'decoder': self.default_decoder,
            'attention': self.default_attention
        }

    @staticmethod
    def do_map(dst, src, map):
        for dst_attr, src_attr in map.items():
            attributes = src_attr.split('.')
            obj = src
            for attr in attributes:
                if hasattr(obj, attr):
                    obj = getattr(obj, attr)
                else:
                    obj = None
                    break
            setattr(dst, dst_attr, obj)


# Export class
class LlmExporterOp(torch.autograd.Function):
    @staticmethod
    def symbolic(g, input, in_features, out_features, has_bias, name):
        args = [input]
        # These become the operator attributes.
        kwargs = {
            "in_features_i": in_features,
            "out_features_i": out_features,
            "has_bias_i": has_bias,
            "name_s": name
        }
        from torch.onnx.symbolic_helper import _get_tensor_sizes
        out_sizes = _get_tensor_sizes(input)[:-1] + [out_features]
        output_type = input.type().with_sizes(out_sizes)
        return g.op("LlmExporter::FakeLinear", input, **kwargs).setType(output_type)

    @staticmethod
    def forward(ctx, input, in_features, out_features, has_bias, name):
        out_shape = list(input.shape)[:-1] + [out_features]
        return input.new_zeros(out_shape)

class FakeLinear(torch.nn.Module):
    def __init__(self, in_features, out_features, has_bias, name):
        super(FakeLinear, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.has_bias = has_bias
        self.name = name

    def forward(self, x):
        return LlmExporterOp.apply(x, self.in_features, self.out_features, self.has_bias, self.name)

class OnnxRebuilder:
    def __init__(self, onnx_path, weight_ops):
        self.weight_ops = weight_ops
        self.onnx_model = onnx.load(onnx_path)
        self.dst_path = onnx_path
        self.onnx_weight_path = f'{onnx_path}.data'
        self.onnx_weight_offset = 0

    def make_external(self, name, data, shape):
        # write to external weight
        length = self.onnx_weight.write(data.tobytes())
        location = self.onnx_weight_path
        offset = self.onnx_weight_offset
        self.onnx_weight_offset += length
        tensor = onnx.TensorProto()
        tensor.name = name
        tensor.data_type = onnx.TensorProto.FLOAT
        tensor.dims.extend(shape)
        # external info
        tensor.data_location = onnx.TensorProto.EXTERNAL
        for k, v in { "location": location, "offset": offset, "length": length }.items():
            entry = tensor.external_data.add()
            entry.key = k
            entry.value = str(v)
        self.onnx_model.graph.initializer.append(tensor)

    def build_weight(self, name, has_bias, ic, oc):
        assert(name in self.weight_ops)
        linear = self.weight_ops[name]
        assert(linear.in_features == ic and
               linear.out_features == oc and
               (linear.bias is not None) == has_bias)
        weight_name, bias_name = f'{name}_weight', f'{name}_bias'
        weight = linear.weight.data.transpose(1, 0).flatten().numpy()
        self.make_external(weight_name, weight, [ic, oc])
        if has_bias:
            bias = linear.bias.data.flatten().numpy()
            self.make_external(bias_name, bias, [oc])
        return weight_name, bias_name

    def rebuild(self):
        from onnx import helper
        new_nodes = []
        self.onnx_weight = open(self.onnx_weight_path, 'wb')
        for node in self.onnx_model.graph.node:
            if node.op_type == 'FakeLinear':
                attributes = {a.name: a for a in node.attribute}
                name = attributes.get('name').s.decode('utf-8')
                has_bias = attributes.get('has_bias').i
                ic = attributes.get('in_features').i
                oc = attributes.get('out_features').i
                weight, bias = self.build_weight(name, has_bias, ic, oc)
                if has_bias:
                    # fakelinear -> matmul + add
                    middle_tensor = f'{name}_matmul'
                    new_nodes.append(helper.make_node('MatMul', [node.input[0], weight], [middle_tensor], name))
                    new_nodes.append(helper.make_node('Add', [middle_tensor, bias], node.output, name))
                else:
                    # fakelinear -> matmul
                    new_nodes.append(helper.make_node('MatMul', [node.input[0], weight], node.output, name))
            else:
                new_nodes.append(node)
        self.onnx_weight.close()
        del self.onnx_model.graph.node[:]
        self.onnx_model.graph.node.extend(new_nodes)
        onnx.save(self.onnx_model, self.dst_path)
        return self.onnx_weight_path

class MNNConveter:
    def __init__(self, onnx_path, weight_ops, config):
        self.weight_ops = weight_ops
        self.quant_block = config.quant_block
        self.quant_bit = config.quant_bit
        self.lm_quant_bit = config.lm_quant_bit
        self.mnn_weight_offset = 0
        self.onnx_model_path = onnx_path
        self.mnn_model_path = onnx_path.replace('.onnx', '.mnn')
        self.mnn_weight_path = f'{self.mnn_model_path}.weight'

    @staticmethod
    def convert(convert_args):
        sfd = os.dup(1)
        log_fp = open(EXPORT_LOG, "a")
        log_fd = log_fp.fileno()
        # mnnconvert ... > .convert_mnn.log
        os.dup2(log_fd, 1)
        try:
            sys.argv = convert_args
            sys.argc = len(convert_args)
            from MNN.tools import mnnconvert
            mnnconvert.main()
            sys.argv = []
        finally:
            os.dup2(sfd, 1)
            os.close(log_fd)

    @staticmethod
    @spinner_run(f'convert onnx model to ')
    def onnx2mnn(onnx_path, mnn_path, args = []):
        convert_args = [
            '',
            '-f',
            'ONNX',
            '--modelFile',
            str(onnx_path),
            '--MNNModel',
            str(mnn_path),
            '--transformerFuse',
            '--allowCustomOp'
        ]
        convert_args += args
        MNNConveter.convert(convert_args)
        return mnn_path

    @staticmethod
    def mnn2json(mnn_path, json_path):
        convert_args = [
            '',
            '-f',
            'MNN',
            '--modelFile',
            str(mnn_path),
            '--JsonFile',
            str(json_path)
        ]
        MNNConveter.convert(convert_args)
        return json_path

    @staticmethod
    def json2mnn(json_path, mnn_path):
        convert_args = [
            '',
            '-f',
            'JSON',
            '--modelFile',
            str(json_path),
            '--MNNModel',
            str(mnn_path)
        ]
        MNNConveter.convert(convert_args)
        return mnn_path

    def export(self):
        if self.weight_ops is None:
            quant_args = [
                '--weightQuantBits',
                str(self.quant_bit),
                '--weightQuantBlock',
                str(self.quant_block)
            ]
            MNNConveter.onnx2mnn(self.onnx_model_path, self.mnn_model_path, quant_args)
        else:
            mnn_json = f'{self.mnn_model_path}.json'
            MNNConveter.onnx2mnn(self.onnx_model_path, self.mnn_model_path)
            MNNConveter.mnn2json(self.mnn_model_path, mnn_json)
            self.rebuild(mnn_json)
            MNNConveter.json2mnn(mnn_json, self.mnn_model_path)

    @spinner_run(f'quant model weight to ')
    def rebuild(self, json_path):
        self.mnn_weight = open(self.mnn_weight_path, 'wb')
        mnn_graph = json.load(open(json_path, 'rt'))
        new_ops = []
        for op in mnn_graph['oplists']:
            if op['type'] == 'Extra':
                new_ops += self.rebuild_op(op, mnn_graph)
            else:
                new_ops.append(op)
        mnn_graph['oplists'] = new_ops
        with open(json_path, 'w', encoding='utf-8') as file:
            json.dump(mnn_graph, file, ensure_ascii=False, indent=4)
        return self.mnn_weight_path

    def quant(self, weight, quant_bit, quant_block):
        weight = weight.numpy()
        oc, ic = weight.shape
        if quant_block == 0:
            block_size = ic
        else:
            block_size = quant_block
        block_num = ic // block_size
        weight = weight.reshape(oc, block_num, block_size)
        max_val = np.max(weight, axis=-1, keepdims=True)
        min_val = np.min(weight, axis=-1, keepdims=True)
        offset = 1 << (quant_bit - 1)
        clip_max = offset - 1
        clip_min = -offset
        scale = (max_val - min_val) / (clip_max - clip_min)
        q_weight = np.round((weight - min_val) / scale).astype(np.int8) + clip_min
        q_weight = (np.clip(q_weight.flatten(), clip_min, clip_max) + offset).astype(np.uint8)
        q_weight = q_weight.reshape(-1, 2)
        if quant_bit == 4:
            q_weight = q_weight[:, 0] * 16 + q_weight[:, 1]
        alpha = np.stack([min_val.flatten(), scale.flatten()], axis=-1).flatten()
        return q_weight, alpha, clip_min

    def write_npy(self, data):
        return self.mnn_weight.write(data.tobytes())

    def write_header(self, ic, oc, quant_bit):
        dim_num = self.mnn_weight.write(b'\x02')
        shape_dtype = np.int16
        if oc > 65535 or ic > 65535:
            shape_dtype = np.int32
        dim_length = self.write_npy(np.array([oc, ic]).astype(shape_dtype))
        offset = 1 << (quant_bit - 1)
        weight_map = [i for i in range(-offset, offset)]
        weight_map.insert(0, len(weight_map))
        map_length = self.write_npy(np.array(weight_map, dtype=np.int8))
        header_length = dim_num + dim_length + map_length
        return header_length, shape_dtype == np.int32

    def build_weight(self, linear, quant_bit, quant_block):
        ic, oc = linear.in_features, linear.out_features
        q_weight, alpha, q_min = self.quant(linear.weight.data, quant_bit, quant_block)
        header_len, shape_int32 = self.write_header(ic, oc, quant_bit)
        weight_len = self.write_npy(q_weight) + header_len
        alpha_len = self.write_npy(alpha)
        if linear.bias is not None:
            bias = linear.bias.data.flatten().numpy()
            bias_length = self.write_npy(bias)
        else:
            bias_length = 0
            # bias = np.zeros([oc], dtype=np.float32)
            # bias_length = self.write_npy(bias)
        external = [self.mnn_weight_offset, weight_len, alpha_len, bias_length, 0]
        self.mnn_weight_offset += (weight_len + alpha_len + bias_length)
        return external, q_min, shape_int32

    def build_tensor(self, graph, tensor_name):
        tensor_idx = [len(graph['tensorName'])]
        graph['tensorName'].append(tensor_name)
        return tensor_idx

    def rebuild_op(self, op, graph):
        attrs = op['main']['attr']
        for attr in attrs:
            if attr['key'] == 'name':
                name = attr['s']
            elif attr['key'] == "in_features":
                ic = attr["i"]
            elif attr['key'] == "out_features":
                oc = attr["i"]
            elif attr['key'] == "has_bias":
                has_bias = attr["i"]
        linear = self.weight_ops[name]
        assert(linear.in_features == ic and
               linear.out_features == oc and
               (linear.bias is not None) == has_bias)


        quant_bit = self.lm_quant_bit if 'lm_head' in name else self.quant_bit
        external, q_min, shape_int32 = self.build_weight(linear, quant_bit, self.quant_block)

        origin_input = op['inputIndexes']
        origin_output = op['outputIndexes']
        # build new tensor
        pre_reshape_name = f'{name}/pre_reshape'
        pre_convert_name = f'{name}/pre_convert'
        conv_name = name
        post_convert_name = f'{name}/post_convert'
        post_reshape_name = f'{name}/post_reshape'
        pre_reshape_output = self.build_tensor(graph, pre_reshape_name)
        pre_convert_output = self.build_tensor(graph, pre_convert_name)
        conv_output = self.build_tensor(graph, conv_name)
        post_convert_output = self.build_tensor(graph, post_convert_name)
        # [batch, seq, hidden_size_i] -[Linear] -> [batch, seq, hidden_size_o]
        # [1, seq, hidden_size_i] ->[Reshape]-> [seq, hidden_size_i, 1, 1]
        # -[Convert]-[Convolution]-[Convert]-> [Reshape] -> [1, seq, hidden_size_o]
        pre_reshape = {
            "name": pre_reshape_name,
            "type": "Reshape",
            "inputIndexes": origin_input,
            "outputIndexes": pre_reshape_output,
            "main_type": "Reshape",
            "main": {
                "dims": [-1, ic, 1, 1],
                "dimType": "NCHW"
            },
            "defaultDimentionFormat": "NHWC"
        }
        pre_convert = {
            "name": pre_convert_name,
            "inputIndexes": pre_reshape_output,
            "outputIndexes": pre_convert_output,
            "type": "ConvertTensor",
            "main_type": "TensorConvertInfo",
            "main": {
                "source": "NCHW",
                "dest": "NC4HW4"
            },
            "defaultDimentionFormat": "NHWC"
        }
        conv_op = {
            "name": conv_name,
            "inputIndexes": pre_convert_output,
            "outputIndexes": conv_output,
            "type": "Convolution",
            "main_type": "Convolution2D",
            "main": {
                'common': {
                    'dilateX': 1, 'dilateY': 1, 'strideX': 1, 'strideY': 1,
                    'kernelX': 1, 'kernelY': 1, 'padX': 0, 'padY': 0, 'group': 1,
                    'outputCount': oc, 'relu': False, 'padMode': 'CAFFE',
                    'relu6': False, 'inputCount': ic, 'hasOutputShape': False
                },
                "quanParameter": {
                    "quantScale": 1.0, "scaleIn": 0.0, "scaleOut": 0.0,
                    "useInt32": False, "has_scaleInt": False, "shapeInt32": shape_int32,
                    "type": 1, "aMax": 0, "aMin": q_min, "readType": oc, "weightSize": 0
                },
                "external": external
            },
            "defaultDimentionFormat": "NHWC"
        }
        post_convert = {
            "name": post_convert_name,
            "inputIndexes": conv_output,
            "outputIndexes": post_convert_output,
            "type": "ConvertTensor",
            "main_type": "TensorConvertInfo",
            "main": {
                "source": "NC4HW4",
                "dest": "NCHW"
            },
            "defaultDimentionFormat": "NHWC"
        }
        post_reshape = {
            "name": post_reshape_name,
            "type": "Reshape",
            "inputIndexes": post_convert_output,
            "outputIndexes": origin_output,
            "main_type": "Reshape",
            "main": {
                "dims": [1, -1, oc],
                "dimType": "NCHW"
            },
            "defaultDimentionFormat": "NHWC"
        }
        return [pre_reshape, pre_convert, conv_op, post_convert, post_reshape]

# some wrapper class for export
class Embedding(torch.nn.Module):
    def __init__(self, embed, config):
        super().__init__()
        self.hidden_size = config.hidden_size
        self.embed = embed
        if config.model_type == 'gemma2':
            normalizer = torch.tensor(self.hidden_size**0.5)
            self.embed.weight.data *= normalizer

    def forward(self, input_ids):
        inputs_embeds = self.embed(input_ids).view(-1, 1, self.hidden_size)
        return inputs_embeds

def repeat_kv(hidden_states: torch.Tensor, n_rep: int) -> torch.Tensor:
    batch, num_key_value_heads, slen, head_dim = hidden_states.shape
    if n_rep == 1:
        return hidden_states
    hidden_states = hidden_states[:, :, None, :, :].expand(batch, num_key_value_heads, n_rep, slen, head_dim)
    return hidden_states.reshape(batch, num_key_value_heads * n_rep, slen, head_dim)

class Attention(torch.nn.Module):
    def __init__(self, attn, config):
        super().__init__()
        self.hidden_size = config.hidden_size
        self.num_heads = config.num_attention_heads
        self.head_dim = config.head_dim
        self.num_key_value_heads = config.num_key_value_heads
        self.num_key_value_groups = self.num_heads // self.num_key_value_heads
        self.rotary = config.rotary
        ModelMapper.do_map(self, attn, config.model_map['attention'])
        if hasattr(self, 'qkv_proj') and self.qkv_proj is not None:
            # split qkv linear to q, k, v
            split_sizes = [self.hidden_size] * 3
            if self.qkv_proj.weight.shape[0] != self.hidden_size * 3:
                # M/GQA
                qkv_hidden_size = self.qkv_proj.weight.shape[0]
                kv_hidden_size = (qkv_hidden_size - self.hidden_size) // 2
                split_sizes = [self.hidden_size, kv_hidden_size, kv_hidden_size]
            self.q_proj = torch.nn.Linear(self.hidden_size, split_sizes[0])
            self.k_proj = torch.nn.Linear(self.hidden_size, split_sizes[1])
            self.v_proj = torch.nn.Linear(self.hidden_size, split_sizes[2])
            if config.model_type == 'chatglm':
                # chatglm-6b
                qkv_weight = self.qkv_proj.weight.data.view(self.num_heads, 3, self.head_dim, self.hidden_size)
                self.q_proj.weight.data = qkv_weight[:, 0, :, :].reshape(self.hidden_size, self.hidden_size)
                self.k_proj.weight.data = qkv_weight[:, 1, :, :].reshape(self.hidden_size, self.hidden_size)
                self.v_proj.weight.data = qkv_weight[:, 2, :, :].reshape(self.hidden_size, self.hidden_size)
                qkv_bias = self.qkv_proj.bias.data.view(self.num_heads, 3, self.head_dim)
                self.q_proj.bias.data = qkv_bias[:, 0, :].reshape(self.hidden_size)
                self.k_proj.bias.data = qkv_bias[:, 1, :].reshape(self.hidden_size)
                self.v_proj.bias.data = qkv_bias[:, 2, :].reshape(self.hidden_size)
            else:
                # other
                qw, kw, vw = torch.split(self.qkv_proj.weight, split_sizes)
                self.q_proj.weight.data = qw
                self.k_proj.weight.data = kw
                self.v_proj.weight.data = vw
                if self.qkv_proj.bias is not None:
                    qb, kb, vb = torch.split(self.qkv_proj.bias, split_sizes)
                    self.q_proj.bias.data = qb
                    self.k_proj.bias.data = kb
                    self.v_proj.bias.data = vb

    def forward(
        self,
        hidden_states: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        past_key_value: Optional[Tuple[torch.Tensor]] = None,
        rotary_pos_emb: Optional[torch.Tensor] = None,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        bsz, q_len, _ = hidden_states.size()
        query_states = self.q_proj(hidden_states)
        key_states = self.k_proj(hidden_states)
        value_states = self.v_proj(hidden_states)
        # print(f'hidden_states.shape = {hidden_states.shape}, query_states.shape = {query_states.shape}')
        query_states = query_states.view(bsz, q_len, self.num_heads, self.head_dim)
        key_states = key_states.view(bsz, q_len, self.num_key_value_heads, self.head_dim)
        value_states = value_states.view(bsz, q_len, self.num_key_value_heads, self.head_dim)
        kv_seq_len = key_states.shape[1]
        if past_key_value is not None:
            kv_seq_len += past_key_value[0].shape[1]

        # rope
        cos, sin = rotary_pos_emb[0], rotary_pos_emb[1]
        query_states = self.rotary.apply_rotary_pos(query_states, cos, sin)
        key_states = self.rotary.apply_rotary_pos(key_states, cos, sin)
        # kv cache
        if past_key_value is not None:
            past_key, past_value = past_key_value[0], past_key_value[1]
            key_states = torch.cat((past_key, key_states), dim=1)
            value_states = torch.cat((past_value, value_states), dim=1)

        past_key_value = torch.stack((key_states, value_states))
        query_states = query_states.transpose(1, 2)
        key_states = key_states.permute([0, 2, 3, 1])
        value_states = value_states.transpose(1, 2)
        # repeat k/v heads if n_kv_heads < n_heads
        key_states = repeat_kv(key_states, self.num_key_value_groups)
        value_states = repeat_kv(value_states, self.num_key_value_groups)
        #------- attention ----------
        # query_states @ key_states
        attn_weights = torch.matmul(query_states, key_states) / math.sqrt(self.head_dim)
        # attention_mask
        if attention_mask.dtype in (torch.bool, torch.int32):
            # chatglm
            attn_weights.masked_fill_(attention_mask, -10000.0)
        else:
            attn_weights = attn_weights + attention_mask
        # upcast softmax to fp32
        attn_weights = torch.nn.functional.softmax(attn_weights, dim=-1, dtype=torch.float32).to(query_states.dtype)
        # attn_weights @ value_states
        attn_output = torch.matmul(attn_weights, value_states)

        attn_output = attn_output.transpose(1, 2).contiguous()
        attn_output = attn_output.reshape(bsz, q_len, -1)
        attn_output = self.o_proj(attn_output)
        return attn_output, past_key_value

def rotate_half(x):
    x1 = x[..., : x.shape[-1] // 2]
    x2 = x[..., x.shape[-1] // 2 :]
    return torch.cat((-x2, x1), dim=-1)

class Rotary(torch.nn.Module):
    def __init__(self, config):
        super().__init__()
        self.rope_theta = config.rope_theta
        self.rotary_dim = config.head_dim
        self.model_type = config.model_type
        if hasattr(config, 'rotary_dim'):
            self.rotary_dim = config.rotary_dim
        if self.model_type == 'chatglm':
            self.rotary_dim = config.head_dim // 2

    def forward(self, position_ids):
        theta = 1.0 / (self.rope_theta ** (torch.arange(0, self.rotary_dim, 2, dtype=torch.float32) / self.rotary_dim))
        position_ids = position_ids.float().reshape(-1, 1)
        idx_theta = position_ids * theta
        rotary_pos_emb = torch.stack([torch.cos(idx_theta), torch.sin(idx_theta)])
        if self.model_type != 'chatglm2':
            rotary_pos_emb = torch.cat((rotary_pos_emb, rotary_pos_emb), dim=-1)
        rotary_pos_emb = rotary_pos_emb.unsqueeze(2).unsqueeze(1)
        return rotary_pos_emb

    def apply_rotary_pos(self, x, cos, sin):
        if self.model_type == 'chatglm':
            return self.chatglm_rotary_pos(x, cos, sin)
        if self.model_type == 'chatglm2':
            return self.chatglm2_rotary_pos(x, cos, sin)
        if self.model_type == 'phi-msft':
            return self.phi_rotary_pos(x, cos, sin)
        return self.llama_rotary_pos(x, cos, sin)

    def llama_rotary_pos(self, x, cos, sin):
        x = (x * cos) + (rotate_half(x) * sin)
        return x

    def phi_rotary_pos(self, x, cos, sin):
        x, x_pass = x[..., :self.rotary_dim], x[..., self.rotary_dim:]
        x = (x * cos) + (rotate_half(x) * sin)
        return torch.cat((x, x_pass), dim=-1)

    def chatglm2_rotary_pos(self, x, cos, sin):
        x, x_pass = x[..., :self.rotary_dim], x[..., self.rotary_dim:]
        b, s, n, h = x.shape
        xshaped = x.view(b, s, n, h//2, 2)
        x = torch.concat(
            [
                xshaped[..., 0] * cos - xshaped[..., 1] * sin,
                xshaped[..., 1] * cos + xshaped[..., 0] * sin,
            ],
            -1,
        )
        return torch.cat((x, x_pass), dim=-1)

    def chatglm_rotary_pos(self, x, cos, sin):
        seq = x.shape[1]
        x1, x2 = x[..., :self.rotary_dim], x[..., self.rotary_dim:]
        cos1, sin1 = cos[:, :seq, ...], sin[:, :seq, ...]
        cos2, sin2 = cos[:, seq:, ...], sin[:, seq:, ...]
        x1 = (x1 * cos1) + (rotate_half(x1) * sin1)
        x2 = (x2 * cos2) + (rotate_half(x2) * sin2)
        return torch.cat((x1, x2), dim=-1)

class Decoder(torch.nn.Module):
    def __init__(self, decoder, config):
        super().__init__()
        ModelMapper.do_map(self, decoder, config.model_map['decoder'])
        self.hidden_size = config.hidden_size
        self.self_attn = Attention(self.self_attn, config)
        # chatglm
        self.alpha = (2 * config.num_hidden_layers) ** 0.5 if config.model_type == 'chatglm' else 1.0

    def forward(
        self,
        hidden_states: torch.Tensor,
        rotary_pos_emb: Optional[torch.Tensor] = None,
        attention_mask: Optional[torch.Tensor] = None,
        past_key_value: Optional[Tuple[torch.Tensor]] = None,
    ) -> Tuple[torch.FloatTensor, Optional[Tuple[torch.FloatTensor, torch.FloatTensor]]]:
        hidden_states = hidden_states.view(1, -1, self.hidden_size)
        residual = hidden_states
        hidden_states = self.input_layernorm(hidden_states)
        norm_hidden_states = hidden_states
        # Self Attention
        hidden_states, present_key_value = self.self_attn(
            hidden_states=hidden_states,
            rotary_pos_emb=rotary_pos_emb,
            attention_mask=attention_mask,
            past_key_value=past_key_value,
        )
        # Fully Connected
        if not hasattr(self, 'post_attention_layernorm'):
            # phi
            feed_forward_hidden_states = self.mlp(norm_hidden_states)
            hidden_states = hidden_states + feed_forward_hidden_states + residual
        elif self.alpha != 1.0:
            # chatglm-6b
            hidden_states = norm_hidden_states * self.alpha + hidden_states
            mlp_input = self.post_attention_layernorm(hidden_states)
            mlp_output = self.mlp(mlp_input)
            hidden_states = mlp_input * self.alpha + mlp_output
        elif hasattr(self, 'pre_feedforward_layernorm'):
            # gemma2
            hidden_states = self.post_attention_layernorm(hidden_states)
            hidden_states = residual + hidden_states
            residual = hidden_states
            hidden_states = self.pre_feedforward_layernorm(hidden_states)
            hidden_states = self.mlp(hidden_states)
            hidden_states = self.post_feedforward_layernorm(hidden_states)
            hidden_states = residual + hidden_states
        else:
            # general
            hidden_states = residual + hidden_states
            residual = hidden_states
            hidden_states = self.post_attention_layernorm(hidden_states)
            hidden_states = self.mlp(hidden_states)
            hidden_states = residual + hidden_states

        return hidden_states, present_key_value

class Lm(torch.nn.Module):
    def __init__(self, lm_, final_layernorm_, config):
        super().__init__()
        self.final_layernorm = final_layernorm_
        self.lm = lm_
        self.hidden_size = config.hidden_size

    def forward(self, hidden_states):
        hidden_states = hidden_states.view(-1, self.hidden_size)[-1].view(1, 1, self.hidden_size)
        hidden_states = self.final_layernorm(hidden_states)
        m_logits = self.lm(hidden_states)
        return m_logits

class LlmExporter(torch.nn.Module):
    '''
    Base class for all llm model export. Inherits from [`torch.nn.Module`].
    '''

    def __init__(self, args):
        super().__init__()
        self.init_from_args(args)
        self.load_model(args.path)

    def init_from_args(self, args):
        self.max_length = 1024
        self.stop_ids = []
        self.visual = None
        self.withou_embedding = False
        # load config from args
        self.path = args.path
        self.dst_path = args.dst_path
        self.lora_path = args.lora_path
        self.skip_slim = args.skip_slim
        self.quant_bit = args.quant_bit
        self.quant_block = args.quant_block
        if args.lm_quant_bit is not None:
            self.lm_quant_bit = args.lm_quant_bit
        else:
            self.lm_quant_bit = self.quant_bit
        # init export dst dir
        if not os.path.exists(self.dst_path):
            os.makedirs(self.dst_path)

    def load_pretrained(self, model_path: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        try:
            self.model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True).float().eval()
        except:
            self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True).float().eval()
        self.config = self.model.config
        if self.lora_path is not None:
            from peft import PeftModel
            adapter = PeftModel.from_pretrained(self.model, model_id=self.lora_path)
            self.model = adapter.merge_and_unload(progressbar=True)

    @spinner_run(f'load pretrained model ')
    def load_model(self, model_path):
        self.load_pretrained(model_path)
        self.attention_mask_type = 'float'
        # load tokenizer info
        self.stop_ids.append(self.tokenizer.eos_token_id)
        if hasattr(self.tokenizer, 'im_end_id'):
            self.stop_ids.append(self.tokenizer.im_end_id)
        if hasattr(self.model, 'generation_config'):
            eos_token_id = self.model.generation_config.eos_token_id
            from collections.abc import Iterable
            if isinstance(eos_token_id, int):
                self.stop_ids.append(eos_token_id)
            elif isinstance(eos_token_id, Iterable):
                for id in eos_token_id:
                    self.stop_ids.append(id)
        self.stop_ids = [stop_id for stop_id in self.stop_ids if stop_id is not None]
        model_mapper = ModelMapper()

        self.model_type, self.model_map = model_mapper.get_map(self.config)
        # print(self.model)
        # print(self.model_type, self.model_map)
        # load config info
        ModelMapper.do_map(self, self.config, self.model_map['config'])
        if not hasattr(self, 'num_key_value_heads') or self.num_key_value_heads is None:
            self.num_key_value_heads = self.num_attention_heads
        if not hasattr(self, 'rope_theta') or self.rope_theta is None:
            self.rope_theta = 10000.0
        if not hasattr(self, 'head_dim') or self.head_dim is None:
            self.head_dim = self.hidden_size // self.num_attention_heads
        # some export info
        self.past_kv_shape = [self.num_hidden_layers, 2, 1, 0, self.num_key_value_heads, self.head_dim]
        self.block_dynamic_axes = {
            "inputs_embeds" : { 0: "seq_len" },
            "attention_mask" : { 2: "seq_len", 3: "seq_len" },
            "position_ids" : { 0: "seq_len" },
            "past_key_values" : { 1: "history_len" }
        }
        self.model_dynamic_axes = {
            "input_ids" : { 0: "seq_len" },
            "attention_mask" : { 2: "seq_len", 3: "seq_len" },
            "position_ids" : { 0: "seq_len" },
            "past_key_values" : { 2: "history_len" }
        }
        self.llm_config = {
            'hidden_size' : self.hidden_size,
            'layer_nums' : self.num_hidden_layers,
            'attention_mask': self.attention_mask_type,
            'key_value_shape': self.past_kv_shape[1:],
            "prompt_template": self.build_prompt('%s'),
            'is_visual': False
        }
        # load modules
        ModelMapper.do_map(self, self.model, self.model_map['model'])
        # rebuild modules
        if self.embed_.weight is self.lm_.weight:
            import copy
            embed_copy = copy.deepcopy(self.embed_)
            self.embed = Embedding(embed_copy, self)
        else:
            self.embed = Embedding(self.embed_, self)
        # Rotary
        self.rotary = Rotary(self)
        self.blocks = []
        for block in self.blocks_.children():
            self.blocks.append(Decoder(block, self))
        self.lm = Lm(self.lm_, self.final_layernorm_, self)
        # visual model
        if self.visual is not None:
            self.image_start_id = self.config.visual['image_start_id']
            self.image_size = self.config.visual['image_size']
            self.llm_config['is_visual'] = True
            self.llm_config['img_size'] = self.image_size
            self.llm_config['imgpad_len'] = 256
            self.llm_config['img_start'] = self.tokenizer.img_start_id
            self.llm_config['img_end'] = self.tokenizer.img_end_id
            self.llm_config['img_pad'] = self.tokenizer.img_pad_id
        return model_path

    def get_attention_mask(self) -> torch.Tensor:
        if self.model_type == 'chatglm':
            return self.chatglm_attention_mask()
        if self.token_len:
            return torch.zeros([1, 1, 1, self.seq_len], dtype=torch.float32)
        return (1 - torch.tril(torch.ones([1, 1, self.seq_len, self.seq_len]))) * torch.finfo(torch.float32).min

    def get_position_ids(self) -> torch.Tensor:
        if self.model_type == 'chatglm':
            return self.chatglm_position_ids()
        if self.token_len:
            return torch.tensor([[self.seq_len - 1]], dtype=torch.long)
        return torch.arange(self.seq_len, dtype=torch.long).unsqueeze(0)

    def chatglm_attention_mask(self):
        if self.token_len:
            return torch.zeros([1]).bool().reshape([1, 1, 1, 1])
        attention_mask = torch.zeros([self.seq_len, self.seq_len], dtype=torch.bool)
        for i in range(self.seq_len - 1):
            attention_mask[i][-1] = True
        attention_mask = attention_mask.reshape([1, 1, self.seq_len, self.seq_len])
        return attention_mask

    def chatglm_position_ids(self):
        if self.token_len:
            return torch.tensor([self.context_len, self.token_len + 1]).reshape([1, 2, 1])
        position_ids_0 = torch.arange(self.seq_len, dtype=torch.long)
        position_ids_1 = torch.zeros(self.seq_len, dtype=torch.long)
        position_ids_0[-1] = position_ids_0[-2]
        position_ids_1[-1] = 1
        position_ids = torch.stack([position_ids_0, position_ids_1]).view(1, 2, -1)
        return position_ids

    def visual_embed(self, input_ids):
        if not torch.any(input_ids == self.image_start_id):
            return self.embed(input_ids)
        bos_pos = torch.where(input_ids == self.image_start_id)
        eos_pos = torch.where(input_ids == self.image_start_id + 1)
        img_pos = torch.stack((bos_pos[0], bos_pos[1], eos_pos[1]), dim=1)
        images = []
        for i, a, b in img_pos:
            image = input_ids[i][a + 1 : b - 1].tolist()
            image = image[ : image.index(self.image_start_id + 2)]
            images.append(bytes(image).decode('utf-8'))
        images = self.visual.encode(images)
        hidden_states = self.embed(input_ids).view(1, -1, self.hidden_size)
        for idx, (i, a, b) in enumerate(img_pos):
            hidden_states[i][a + 1 : b] = images[idx]
        return hidden_states.view(-1, 1, self.hidden_size)

    def embedding(self, input_ids):
        if self.visual is not None and self.token_len == 0:
            input_embeds = self.visual_embed(input_ids)
        else:
            input_embeds = self.embed(input_ids)
        return input_embeds

    def forward_impl(self, hidden_states, attention_mask, position_ids, past_key_values):
        presents = []
        rotary_pos_emb = self.rotary(position_ids)
        for i in range(self.num_hidden_layers):
            hidden_states, kv = self.blocks[i](hidden_states, rotary_pos_emb, attention_mask, past_key_values[i])
            presents.append(kv)
        logits = self.lm(hidden_states).reshape(-1)
        presents = torch.stack(presents)
        self.seq_len += 1
        self.token_len += 1
        return logits, presents

    def forward(self, input_ids, attention_mask, position_ids, past_key_values):
        if self.withou_embedding:
            return self.forward_impl(input_ids, attention_mask, position_ids, past_key_values)
        return self.forward_impl(self.embedding(input_ids), attention_mask, position_ids, past_key_values)

    # some test functions
    def build_prompt(self, query):
        # just for test
        if 'Qwen2' in self.path:
            return f'<|im_start|>user\n{query}<|im_end|>\n<|im_start|>assistant\n'
        if 'Qwen' in self.path:
            return f'\n<|im_start|>user\n{query}<|im_end|>\n<|im_start|>assistant\n'
        if 'Baichuan2' in self.path:
            return f'<reserved_106>{query}<reserved_107>'
        if 'internlm' in self.path:
            return f'<|User|>:{query}<eoh>\n<|Bot|>:'
        if 'TinyLlama' in self.path:
            return f'<s><|system|>\nYou are a friendly chatbot who always responds in the style of a pirate</s>\n<|user|>\n{query}</s>\n<|assistant|>\n'
        if 'Yi' in self.path:
            return f'<|im_start|> user\n{query}<|im_end|>\n<|im_start|> assistant\n'
        if 'deepseek' in self.path:
            return f'<|begin_of_sentence|>User: {query}\n\nAssistant:'
        if 'Llama-3' in self.path:
            return f'<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n{query}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n'
        if 'Llama-2' in self.path:
            return f'<s>[INST]{query}[/INST]'
        if 'chatglm2' in self.path:
            return f'[Round 1]\n\n问：{query}\n\n答：'
        if 'chatglm3' in self.path or 'glm-4' in self.path:
            return f'<|user|>\n{query}\n<|assistant|>\n'
        if 'chatglm' in self.path:
            return f'{query}[gMASK]<sop>'
        if 'phi-2' in self.path:
            return f'Instruct: {query}\nOutput:'
        if 'gemma-2' in self.path:
            return f'<bos><start_of_turn>user\n{query}<end_of_turn>\n<start_of_turn>model\n'
        return query

    def str_to_ids(self, prompt):
        input_ids = self.tokenizer(prompt, return_tensors="pt")['input_ids']
        return input_ids

    def id_to_str(self, token_id):
        word = self.tokenizer._convert_id_to_token(int(token_id))
        word = self.tokenizer.convert_tokens_to_string([word])
        return word

    def response(self, query):
        prompt = self.build_prompt(query)
        input_ids = self.str_to_ids(prompt)
        self.seq_len = input_ids.numel()
        self.context_len = self.seq_len - 2
        self.token_len = 0
        past_key_values = [None for i in range(self.num_hidden_layers)]
        token_id = input_ids
        while self.token_len < self.max_length:
            attention_mask = self.get_attention_mask()
            position_ids = self.get_position_ids()
            logits, past_key_values = self.forward(token_id, attention_mask, position_ids, past_key_values)
            token_id = torch.argmax(logits)
            # print(token_id)
            if token_id in self.stop_ids:
                print("", end='\n')
                break
            word = self.id_to_str(token_id)
            print(word, end="", flush=True)

    def export_visual(self):
        if self.visual is None:
            return
        input_images = torch.randn((1, 3, self.image_size, self.image_size))
        model = self.visual
        onnx_model = f'{self.dst_path}/visual.onnx'
        torch.onnx.export(model, (input_images),
                        onnx_model,
                        input_names=['input_images'],
                        output_names=['image_embeds'],
                        dynamic_axes={"input_images": {
                            0: "size"
                        }},
                        do_constant_folding=True,
                        opset_version=15)
        return onnx_model
        if not self.skip_slim:
            slim(onnx_model, output_model=onnx_model)

    @spinner_run(f'export embedding to ')
    def export_embed(self):
        if not hasattr(self, 'embed') or not isinstance(self.embed.embed, torch.nn.Embedding):
            return
        import ctypes
        tensor_data = self.embed.embed.weight.data.bfloat16()
        data_ptr = tensor_data.untyped_storage().data_ptr()
        buffer = (ctypes.c_byte * (tensor_data.numel() * 2)).from_address(data_ptr)
        embedding_file = f'{self.dst_path}/embeddings_bf16.bin'
        with open(embedding_file, 'wb') as f:
            f.write(buffer)
        return embedding_file

    @spinner_run(f'export config to ')
    def export_config(self):
        config_json = f'{self.dst_path}/llm_config.json'
        with open(config_json, 'w', encoding='utf-8') as f:
            json.dump(self.llm_config, f, ensure_ascii=False, indent=4)
        with open(f'{self.dst_path}/config.json', 'w', encoding='utf-8') as f:
            config = {
                "llm_model": "llm.mnn",
                "llm_weight": "llm.mnn.weight",
                "backend_type": "cpu",
                "thread_num": 4,
                "precision": "low",
                "memory": "low"
            }
            json.dump(config, f, ensure_ascii=False, indent=4)
        return config_json

    def unload_param(self):
        self.unloaded_ops = {}
        def build_faker(real, name):
            faker = FakeLinear(real.in_features, real.out_features, real.bias is not None, name)
            self.unloaded_ops[name] = real
            return faker
        # replace linear with fakelinear to save export memory and time
        with torch.no_grad():
            for i in range(self.num_hidden_layers):
                for name, child in self.blocks[i].self_attn.named_children():
                    if isinstance(child, torch.nn.Linear):
                        setattr(self.blocks[i].self_attn, name, build_faker(child, f'/layers.{i}/self_attn/{name}/Linear'))
                for name, child in self.blocks[i].mlp.named_children():
                    if isinstance(child, torch.nn.Linear):
                        setattr(self.blocks[i].mlp, name, build_faker(child, f'/layers.{i}/mlp/{name}/Linear'))
            self.lm.lm = build_faker(self.lm.lm, f'/lm/lm_head/Linear')

    @spinner_run(f'export model weight to ')
    def onnx_load_param(self, onnx_path):
        return OnnxRebuilder(onnx_path, self.unloaded_ops).rebuild()

    def onnx_export(self, model, onnx_model, inputs, input_names, output_names, dynamic_axes):
        torch.onnx.export(
            model, inputs,
            onnx_model,
            input_names=input_names,
            output_names=output_names,
            dynamic_axes=dynamic_axes,
            do_constant_folding=True,
            opset_version=15)

    @spinner_run(f'slim the graph of ')
    def onnx_slim(self, onnx_model):
        import onnxslim
        model = onnxslim.slim(onnx_model)
        onnx.save(model, onnx_model)
        return onnx_model

    @spinner_run(f'export onnx model to ')
    def export_onnx(self):
        # unload linear weight to save export memory
        self.unload_param()
        model = self
        self.seq_len = 3
        self.token_len = 0
        input_ids = torch.arange(3, dtype=torch.long)
        attention_mask =  self.get_attention_mask()
        position_ids = self.get_position_ids()
        past_key_values = torch.zeros(self.past_kv_shape)
        onnx_model = f'{self.dst_path}/llm.onnx'
        # mnn export
        if self.withou_embedding:
            input_ids = self.embedding(input_ids)
        # export to onnx
        torch.onnx.export(
            model, (input_ids, attention_mask, position_ids, past_key_values),
            onnx_model,
            input_names=[
                'input_ids', 'attention_mask', 'position_ids', 'past_key_values'
            ],
            output_names=['logits', 'presents'],
            dynamic_axes=self.model_dynamic_axes,
            do_constant_folding=True,
            opset_version=15)
        return onnx_model

    def export(self, export_type):
        export_mnn = export_type == 'mnn'
        # export tokenizer
        self.export_tokenizer()
        if self.visual:
            self.export_visual()
        if export_mnn:
            self.export_config()
            self.export_embed()
            self.withou_embedding = True
        # export graph to llm.onnx
        onnx_model = self.export_onnx()
        if not self.skip_slim:
            self.onnx_slim(onnx_model)
        if export_mnn:
            # convert onnx to mnn and quant weight
            MNNConveter(onnx_model, self.unloaded_ops, self).export()
        else:
            # export weight to llm.onnx.data
            self.onnx_load_param(onnx_model)

    @spinner_run(f'export tokenizer to ')
    def export_tokenizer(self):
        # load tokenizer file
        tokenizer_model = os.path.join(self.path, 'tokenizer.model')
        ice_text_model = os.path.join(self.path, 'ice_text.model')
        try:
            import sentencepiece as spm
            if os.path.exists(tokenizer_model):
                self.sp_model = spm.SentencePieceProcessor(tokenizer_model)
            elif os.path.exists(ice_text_model):
                self.sp_model = spm.SentencePieceProcessor(ice_text_model)
            else:
                self.sp_model = None
        except:
            self.sp_model = None
        merge_file = os.path.join(self.path, 'merges.txt')
        if os.path.exists(merge_file):
            self.merge_txt = merge_file
        else:
            self.merge_txt = None
        # TOKENIZER MAGIC NUMBER
        MAGIC_NUMBER = 430
        # TOKENIZER TYPE
        SENTENCEPIECE = 0; TIKTOIKEN = 1; BERT = 2; HUGGINGFACE = 3
        def write_line(fp, *args):
            for arg in args:
                for token in arg:
                    fp.write(str(token) + ' ')
            fp.write('\n')
        def write_header(fp, type, speicals, prefix = []):
            fp.write(f'{MAGIC_NUMBER} {type}\n')
            fp.write(f'{len(speicals)} {len(self.stop_ids)} {len(prefix)}\n')
            write_line(fp, speicals, self.stop_ids, prefix)

        file_path = os.path.join(self.dst_path, "tokenizer.txt")
        special_list = list(self.tokenizer.added_tokens_decoder.keys())
        if hasattr(self.tokenizer, 'special_tokens'):
            for k, v in self.tokenizer.special_tokens.items():
                special_list.append(v)
        if hasattr(self.tokenizer, 'gmask_token_id'):
            special_list.append(self.tokenizer.gmask_token_id)
        vocab_list = []
        prefix_list = []
        if hasattr(self.tokenizer, 'get_prefix_tokens'):
            prefix_list = self.tokenizer.get_prefix_tokens()
        if self.sp_model is not None:
            # senetencepiece
            NORMAL = 1; UNKNOWN = 2; CONTROL = 3
            USER_DEFINED = 4; UNUSED = 5; BYTE = 6
            for i in range(self.sp_model.GetPieceSize()):
                token = self.sp_model.IdToPiece(i)
                score = self.sp_model.GetScore(i)
                type = NORMAL
                if self.sp_model.IsUnknown(i):
                    type = UNKNOWN
                elif self.sp_model.IsControl(i):
                    type = CONTROL
                elif self.sp_model.IsUnused(i):
                    type = UNUSED
                elif self.sp_model.IsByte(i):
                    type = BYTE
                if self.path == 'Chatglm_6b':
                    if '<n>' in token: token = '\n'
                    if '<|tab|>' in token: token = '\t'
                    if '<|blank_' in token: token = ' ' * int(token[8:token.find('|>')])
                if '▁' in token: token = token.replace('▁', ' ')
                token_encode = base64.b64encode(token.encode("utf-8")).decode("utf8")
                vocab_list.append(f'{token_encode} {score} {type}\n')
            with open(file_path, "w", encoding="utf8") as fp:
                write_header(fp, SENTENCEPIECE, special_list, prefix_list)
                fp.write(f'{len(vocab_list)}\n')
                for vocab in vocab_list:
                    fp.write(vocab)
        elif hasattr(self.tokenizer, 'mergeable_ranks'):
            # tikton
            vocab_list = []
            for k, v in self.tokenizer.mergeable_ranks.items():
                line = base64.b64encode(k).decode("utf8") + "\n"
                vocab_list.append(line)
            if hasattr(self.tokenizer, 'special_tokens'):
                for k, v in self.tokenizer.special_tokens.items():
                    line = base64.b64encode(k.encode("utf-8")).decode("utf8") + "\n"
                    vocab_list.append(line)
            if hasattr(self.tokenizer, 'added_tokens_decoder'):
                for k, v in self.tokenizer.added_tokens_decoder.items():
                    line = base64.b64encode(v.__str__().encode("utf-8")).decode("utf8") + "\n"
                    vocab_list.append(line)
            with open(file_path, "w", encoding="utf8") as fp:
                write_header(fp, TIKTOIKEN, special_list, prefix_list)
                fp.write(f'{len(vocab_list)}\n')
                for vocab in vocab_list:
                    fp.write(vocab)
        elif self.merge_txt is not None:
            # huggingface tokenizer
            merge_list = []
            vocab = self.tokenizer.get_vocab()
            special_list = list(self.tokenizer.added_tokens_decoder.keys())
            vocab_list = ['<unk>' for i in range(len(vocab))]
            # load vocab
            for k, v in vocab.items():
                vocab_list[int(v)] = k
            # load merge
            with open(self.merge_txt, 'rt') as merge:
                for line in merge.readlines():
                    merge_list.append(line)
            # write to tokenizer.txt
            with open(file_path, "w", encoding="utf8") as fp:
                write_header(fp, HUGGINGFACE, special_list)
                fp.write(f'{len(vocab_list)} {len(merge_list)}\n')
                for v in vocab_list:
                    fp.write(v + '\n')
                for m in merge_list:
                    fp.write(m)
        else:
            # other tikton
            def unicode_to_byte(u: int):
                if u >= 256 and u <= 288:
                    return u - 256
                if u >= 289 and u <= 322:
                    return u - 162
                if u == 323:
                    return 173
                if u == 65372: # |
                    return 124
                if u == 9601:  # _
                    return 95
                return u
            vocab = self.tokenizer.get_vocab()
            vocab_list = ['<unk>' for i in range(len(vocab))]
            for k, v in vocab.items():
                try:
                    vocab_list[int(v)] = bytes([unicode_to_byte(ord(c)) for c in k]).decode('utf-8', errors='ignore')
                except:
                    vocab_list[int(v)] = k
            special_list = list(self.tokenizer.added_tokens_decoder.keys())
            with open(file_path, "w", encoding="utf8") as fp:
                write_header(fp, TIKTOIKEN, special_list)
                fp.write(f'{len(vocab_list)}\n')
                for v in vocab_list:
                    line = base64.b64encode(v.encode('utf-8')).decode("utf8") + "\n"
                    fp.write(line)
        return file_path


class EmbeddingExporter(LlmExporter):
    def __init__(self, args):
        super().__init__(args)

    def forward(self, input_ids, position_ids, attention_mask):
        input_ids = input_ids.view(1, -1)
        token_type_ids = (1 - attention_mask).view(1, -1)
        hidden_states = self.embed(input_ids, token_type_ids, position_ids)[0].unsqueeze(0)
        for i in range(self.num_hidden_layers):
            hidden_states = self.blocks[i](hidden_states, attention_mask)[0]
        sentence_embeddings = hidden_states[:, 0]
        sentence_embeddings = torch.nn.functional.normalize(sentence_embeddings, p=2, dim=1)
        return sentence_embeddings

    def response(self, query):
        self.eval()
        input_ids = self.tokenizer(query)['input_ids']
        self.seq_len = len(input_ids)
        input_ids = torch.tensor(input_ids)
        position_ids = self.get_position_ids()
        attention_mask = self.get_attention_mask()
        res = self.forward(input_ids, position_ids, attention_mask)
        print(res)
        return res

    @spinner_run(f'load pretrained model ')
    def load_model(self, model_path):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True).float().eval()
        transformer = self.model.encoder
        self.lm_ = self.model.pooler
        self.embed_ = self.model.embeddings
        self.hidden_size = self.embed_.word_embeddings.weight.shape[-1]
        self.blocks = transformer.layer
        # some wrapper
        self.stop_ids = []
        self.num_hidden_layers = len(self.blocks)
        self.embed = self.embed_
        self.lm = self.lm_
        # some config for export
        self.model_dynamic_axes = {
            "input_ids" : { 0: "seq_len" },
            "position_ids" : { 1: "seq_len" },
            "attention_mask" : { 3: "seq_len" }
        }
        self.attention_mask_type = 'int'
        self.llm_config = {
            'hidden_size' : self.hidden_size,
            'layer_nums' : self.num_hidden_layers,
            'attention_mask': self.attention_mask_type,
            'key_value_shape': [],
            "prompt_template": self.build_prompt('%s'),
            'is_visual': False
        }
        return model_path

    @spinner_run(f'export onnx model to ')
    def export_onnx(self):
        model = self.eval()
        self.seq_len = 3
        input_ids = torch.arange(3, dtype=torch.long)
        position_ids = self.get_position_ids()
        attention_mask = self.get_attention_mask()
        onnx_model = f'{self.dst_path}/bge.onnx'
        torch.onnx.export(
            model, (input_ids, position_ids, attention_mask),
            onnx_model,
            input_names=[
                'input_ids',
                'position_ids',
                'attention_mask'
            ],
            output_names=['sentence_embeddings'],
            dynamic_axes=self.model_dynamic_axes,
            do_constant_folding=True,
            opset_version=15)
        return onnx_model

    def export(self, export_type):
        self.export_tokenizer()
        self.export_config()
        onnx_model = self.export_onnx()
        if not self.skip_slim:
            self.onnx_slim(onnx_model)
        if 'mnn' in export_type:
            MNNConveter(onnx_model, None, self).export()

    def build_prompt(self, query):
            return f'[CLS]{query}[SEP]'

    def get_position_ids(self) -> torch.Tensor:
        return torch.arange(self.seq_len, dtype=torch.long).unsqueeze(0)

    def get_attention_mask(self) -> torch.Tensor:
        return torch.ones([1, 1, 1, self.seq_len], dtype=torch.long)

def export(path,
           type = None,
           lora_path = None,
           dst_path = './model',
           export = 'onnx',
           skip_slim = False,
           quant_bit = 4,
           quant_block = 128,
           lm_quant_bit = None):
    args = argparse.Namespace()
    for k, v in {
        'path': path,
        'type': type,
        'lora_path': lora_path,
        'dst_path': dst_path,
        'export': export,
        'skip_slim': skip_slim,
        'quant_bit': quant_bit,
        'quant_block': quant_block,
        'lm_quant_bit': lm_quant_bit
    }.items():
        setattr(args, k, v)
    if 'bge' in path:
        llm_exporter = EmbeddingExporter(args)
    else:
        llm_exporter = LlmExporter(args)
    # export
    llm_exporter.export(export)

def main():
    parser = argparse.ArgumentParser(description='llm_exporter', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--path', type=str, required=True,
                        help='path(`str` or `os.PathLike`):\nCan be either:'
                        '\n\t- A string, the *model id* of a pretrained model like `THUDM/chatglm-6b`. [TODO]'
                        '\n\t- A path to a *directory* clone from repo like `../chatglm-6b`.')
    parser.add_argument('--type', type=str, default=None,
                        help='type(`str`, *optional*):'
                        '\n\tThe pretrain llm model type.'
                        )
    parser.add_argument('--lora_path', type=str, default=None, help='lora path, defaut is `None` mean not apply lora.')
    parser.add_argument('--dst_path', type=str, default='./model', help='export onnx/mnn model to path, defaut is `./model`.')
    parser.add_argument('--test', type=str, help='test model inference with query `TEST`.')
    parser.add_argument('--export', type=str, default=None, help='export model to an onnx/mnn model.')
    parser.add_argument('--skip_slim', action='store_true', help='Whether or not to skip onnx-slim.')
    parser.add_argument('--quant_bit', type=int, default=4, help='mnn quant bit, 4 or 8, default is 4.')
    parser.add_argument('--quant_block', type=int, default=128, help='mnn quant block, default is 0 mean channle-wise.')
    parser.add_argument('--lm_quant_bit', type=int, default=None, help='mnn lm_head quant bit, 4 or 8, default is `quant_bit`.')

    args = parser.parse_args()

    model_path = args.path
    model_type = args.type

    if 'bge' in model_path:
        llm_exporter = EmbeddingExporter(args)
    else:
        llm_exporter = LlmExporter(args)

    # some actions
    if args.test is not None:
        llm_exporter.response(args.test)

    if args.export is not None:
        llm_exporter.export(args.export)

if __name__ == '__main__':
    main()