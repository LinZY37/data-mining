import os
import random

import random
import re

import jieba

txts = []
labels = set()
data_dict={}
# stop_words = [x.strip() for x in open('../../stopword/stopword.txt', encoding='gbk').readlines()]
path  = './DF-NEWS'
import pandas as pd
# def clean_text(text):
#     pattern = re.compile("[^\u4e00-\u9fa5^,^.^!^a-z^A-Z^0-9]")  # 只保留中英文、数字和符号，去掉其他东西
#     # 若只保留中英文和数字，则替换为[^\u4e00-\u9fa5^a-z^A-Z^0-9]
#     text = re.sub(pattern, '', text)  # 把文本中匹配到的字符替换成空字符
#     text = ''.join(text.split())  # 去除空白
#     text = text.replace("\n","").replace("\r","")
#     text = text.lower()
#     words = list(jieba.lcut(text))
#     words = [word for word in words if word not in stop_words]
#     text = ' '.join(words)
#     return text
for filename in os.listdir(path):
    file_path = os.path.join(path, filename)

    data = pd.read_csv(file_path,encoding='utf-8',encoding_errors='ignore')  # 直接使用 read_excel() 方法读取
    clazz = set()
    for index, row in data.iterrows():
        column_value =data.iloc[index, :].tolist()
        # column_value = clean_text(column_value)
        column_value = '.'.join(column_value).replace('\n','').replace('\r','')
        label = filename.replace('.csv','')
        if column_value not in ["nan",''] and  label != "nan":

            txts.append(str(column_value) + " __!__ " + str(label))
            labels.add(str(label))
            if label not in data_dict.keys():
                data_dict[label]=[]
            data_dict[label].append(str(column_value) + " __!__ " + str(label))
for k,v in data_dict.items():
    print(k,len(v))
    # 处理列的值
# txts= data_dict['积极']+data_dict['消极']*3
print(len(txts))
print(labels)
random.shuffle(txts)
with open('train.txt', 'w', encoding='utf-8', errors="ignore") as f:
    # for index, data in enumerate(train):
    for index, data in enumerate(txts[:-10000]):
        f.write(str(data) + '\n')
f.close()

with open('dev.txt', 'w', encoding='utf-8', errors="ignore") as f:
    # for index, data in enumerate(dev):
    for index, data in enumerate(txts[-10000:-5000]):
        f.write(str(data) + '\n')
f.close()

with open('test.txt', 'w', encoding='utf-8', errors="ignore") as f:
    # for index, data in enumerate(test):
    for index, data in enumerate(txts[-5000:]):
        f.write(str(data) + '\n')
f.close()

with open('class.txt', 'w', encoding='utf-8', errors="ignore") as f:
    for index, data in enumerate(labels):
        f.write(str(data) + '\n')
f.close()

