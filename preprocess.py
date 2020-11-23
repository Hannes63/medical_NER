# -*- coding:utf-8 -*-
from random import shuffle


def preprocess(files, data_dir='./data_set/'):
    print('开始对数据集分组处理...')
    data = []
    for file in files:
        with open(data_dir + file, 'r', encoding='utf-8') as f:
            for line in f:
                data.append(eval(line))

    shuffle(data)
    data_size = len(data)
    make_set(data[: data_size * 3 // 5], './data_set/train.char.bmes')
    make_set(data[data_size * 3 // 5: data_size * 4 // 5], './data_set/dev.char.bmes')
    make_set(data[data_size * 4 // 5:], './data_set/test.char.bmes')
    print('生成数据集完成，共%d项' % data_size)


def make_set(data, file_name):
    acronym = {'解剖部位': 'SITE', '疾病和诊断': 'ILL_DIAG', '检验': 'CHECK',
               '手术': 'OPS', '药物': 'DRUG', '检查': 'EXAM', '影像检查': 'IMAGE',
               '实验室检验': 'LAB'}
    with open(file_name, 'w', encoding='utf-8') as f:
        for item in data:
            index = 0
            for entity in item['entities']:
                while index < entity['start_pos']:
                    # 去除空白字符
                    if item['originalText'][index] == ''.join(item['originalText'][index].split()):
                        f.write(item['originalText'][index] + ' O\n')
                    index += 1

                while item['originalText'][index] != ''.join(item['originalText'][index].split()):
                    index += 1
                    entity['start_pos'] += 1

                # 避免结尾几个字符为空白字符
                j = entity['end_pos'] - 1
                while item['originalText'][j] != ''.join(item['originalText'][j].split()):
                    j -= 1
                entity['end_pos'] = j + 1
                if entity['start_pos'] == entity['end_pos'] - 1:
                    f.write(item['originalText'][index] + ' S-' + acronym[entity['label_type']] + '\n')
                    index += 1
                    continue
                f.write(item['originalText'][index] + ' B-' + acronym[entity['label_type']] + '\n')
                index += 1
                while index < entity['end_pos'] - 1:
                    if item['originalText'][index] == ''.join(item['originalText'][index].split()):
                        f.write(item['originalText'][index] + ' M-' + acronym[entity['label_type']] + '\n')
                    index += 1
                assert item['originalText'][index] == ''.join(item['originalText'][index].split())
                f.write(item['originalText'][index] + ' E-' + acronym[entity['label_type']] + '\n')
                index += 1
            while index < len(item['originalText']):
                if item['originalText'][index] == ''.join(item['originalText'][index].split()):
                    f.write(item['originalText'][index] + ' O\n')
                index += 1
            f.write('\n')

