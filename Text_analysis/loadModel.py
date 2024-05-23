# coding=utf-8

import time
from importlib import import_module

import torch


from utils import build_String, get_time_dif, build_iterator


def _to_tensor(config, datas):
    x = torch.LongTensor([_[0] for _ in datas]).to(config.device)
    y = torch.LongTensor([_[1] for _ in datas]).to(config.device)

    seq_len = torch.LongTensor([_[2] for _ in datas]).to(config.device)
    mask = torch.LongTensor([_[3] for _ in datas]).to(config.device)
    return (x, seq_len, mask), y


model_name = 'bert_LSTM ATT_CNN'
dataset = 'corona_fake'
x = import_module("models." + model_name)
config = x.Config(dataset)


start_time = time.time()
print("Loading data...")

model = x.Model(config).to(config.device)

weight_path = config.save_path
pretrained_dict = torch.load(weight_path)
model.load_state_dict(pretrained_dict, strict=False)

def predict_str_lable(strs):
    predic_text = []
    run_data = build_String(config, strs)
    iter_data = _to_tensor(config, run_data)
    outputs = model(iter_data[0])
    predic = torch.max(outputs.data, 1)[1].cpu().numpy()
    class_list = [x.strip() for x in open(
        'Datas/' + dataset + '/data/class.txt', encoding='utf-8').readlines()]  # 类别名单
    probabilities = torch.nn.functional.softmax(outputs, dim=1)

    predicted_probs = probabilities[range(probabilities.shape[0]), predic]
    mapped_values = predicted_probs * 10 - 5
    mapped_values[ predic == 1] = -mapped_values[ predic == 1]
    mapped_values = mapped_values.cpu().detach().numpy()
    predic_text = [class_list[i] for i in predic]
    print(predic_text)
    time_dif = get_time_dif(start_time)
    print("Time usage:", time_dif)
    return predic_text, mapped_values


if __name__ == '__main__':
    texts = ['test']
    print(texts)
    lables,_ = predict_str_lable(texts)
    print(lables)