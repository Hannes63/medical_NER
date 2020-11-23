from os.path import join
from codecs import open


def text_transform():
    with open('./data_set/training_set1.txt') as f1:
        data = []
        with open('./data_set/training_set1.txt', 'r', encoding='utf-8') as f1:
            for line in f1:
                data.append(eval(line))
        with open('./data_set/training_set2.txt', 'r', encoding='utf-8') as f2:
            for line in f2:
                data.append(eval(line))
        with open('./data_set/test_set.json', 'r', encoding='utf-8') as f3:
            for line in f3:
                data.append(eval(line))
        print(len(data))
        ...


def build_corpus(split, make_vocab=True, data_dir="./data_set"):
    """读取数据"""
    assert split in ['train', 'dev', 'test']

    word_lists = []
    tag_lists = []
    with open(join(data_dir, split+".char.bmes"), 'r', encoding='utf-8') as f:
        word_list = []
        tag_list = []
        for line in f:
            if line[0] != '\r':
                try:
                    word, tag = line.strip('\n').split()
                    word_list.append(word)
                    tag_list.append(tag)
                except ValueError:
                    pass
            else:
                if not word_list:
                    continue
                assert(tag_list != [])
                word_lists.append(word_list)
                tag_lists.append(tag_list)
                word_list = []
                tag_list = []

    # 如果make_vocab为True，还需要返回word2id和tag2id
    if make_vocab:
        word2id = build_map(word_lists)
        tag2id = build_map(tag_lists)
        # print(split, len(word_lists), len(tag_lists))
        return word_lists, tag_lists, word2id, tag2id
    else:
        # print(split, len(word_lists), len(tag_lists))
        return word_lists, tag_lists


def build_map(lists):
    maps = {}
    for list_ in lists:
        for e in list_:
            if e not in maps:
                maps[e] = len(maps)

    return maps
