# coding: UTF-8
import random
import time
import warnings

import torch
import numpy as np
from train_eval import train, init_network
from importlib import import_module
import argparse
from utils import build_dataset, build_iterator, get_time_dif

parser = argparse.ArgumentParser(description='Chinese Text Classification')
# 此处修改模型
parser.add_argument('--model_name', default='bert_LSTM ATT_CNN', type=str, required=False, help='choose a model')

parser.add_argument('--embedding', default='pre_trained', type=str, help='random or pre_trained')
parser.add_argument('--word', default=True, type=bool, help='True for word, False for char')
args = parser.parse_args()

# 忽略特定的UserWarning
warnings.filterwarnings('ignore', category=UserWarning, message=".*This overload of add_ is deprecated.*")


# 运行一个训练模型的流程，根据给定的种子值、数据集和模型配置
def run(seed, dataset):
    # 初始化数据集
    dataset = dataset  # 数据集变量，用于接下来的配置和模型训练

    use_saved = False  # 默认不使用已保存的模型

    # 设置随机种子
    np.random.seed(seed)
    torch.manual_seed(seed)
    random.seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True

    # 根据输入参数选择模型配置，'args.model_name' 应该是外部传入的参数
    model_name = args.model_name  # bert  # 假设是BERT模型
    x = import_module('models.' + model_name)
    # 使用选择的模型名称导入对应的模块，并创建配置对象
    config = x.Config(dataset)

    # 记录开始时间
    start_time = time.time()

    # 实例化模型，并将模型移到定义的设备上（如GPU）
    model = x.Model(config).to(config.device)
    # 如果选择使用已保存的模型权重
    if use_saved:
        # 获取模型权重的保存路径
        weight_path = config.save_path
        # 加载模型权重
        pretrained_dict = torch.load(weight_path)
        # 更新当前模型的权重
        model.load_state_dict(pretrained_dict, strict=False)
        # 释放预训练权重变量的内存
        pretrained_dict = 0

    train_data, dev_data, test_data = build_dataset(config)
    train_iter = build_iterator(train_data, config)
    dev_iter = build_iterator(dev_data, config)
    test_iter = build_iterator(test_data, config)

    train(config, model, train_iter, dev_iter, test_iter)

if __name__ == '__main__':

    # 选择数据集
    dataset = 'corona_fake'
    for i in range(2, 3):

        run(i, dataset)
