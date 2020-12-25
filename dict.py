from data import build_corpus

tag2cn = {'SITE': '解剖部位', 'ILL_DIAG': '疾病和诊断', 'CHECK': '检验',
               'OPS': '手术', 'DRUG': '药物', 'EXAM': '检查', 'IMAGE': '影像检查',
               'LAB': '实验室检验'}

def make_dictionary():
    """
    建立字典
    """
    train_word_lists, train_tag_lists = build_corpus("train",make_vocab=False)
    dev_word_lists, dev_tag_lists = build_corpus("dev", make_vocab=False)
    test_word_lists, test_tag_lists = build_corpus("test", make_vocab=False)
    word_lists=train_word_lists+dev_word_lists+test_word_lists
    tag_lists=train_tag_lists+dev_tag_lists+test_tag_lists
    dict={}
    for i in range(len(tag_lists)):
        begin_index=0
        w_list=word_lists[i]
        t_list=tag_lists[i]
        for j in range(len(t_list)):
            if t_list[j][0] == 'S':
                if(w_list[j] not in dict):
                    dict[w_list[j]]=t_list[j][2:]
            elif t_list[j][0] == 'B':
                begin_index = j
            elif t_list[j][0] == 'E':
                if("".join(w_list[begin_index:j+1]) not in dict):
                    dict["".join(w_list[begin_index:j+1])]=t_list[j][2:]
    with open('data_set/dict.txt', 'w') as f:
        for k,v in dict.items():
            #仅考虑长度大于1的实体
            if(len(k)>1):
                f.write(str(k)+' '+str(v)+'\n')

def FMM_func(user_dict, sentence):
    """
    正向最大匹配（FMM）
    :param user_dict: 词典
    :param sentence: 句子
    """
    # 词典中最长词长度
    max_len = max([len(item) for item in user_dict])
    start = 0
    res=[]
    while start != len(sentence):
        index = start+max_len
        if index>len(sentence):
            index = len(sentence)
        for i in range(max_len):
            if (sentence[start:index] in user_dict):
                res.append([start,index,tag2cn[user_dict[sentence[start:index]]]])
                start = index
                break
            if(len(sentence[start:index])==1):
                start = index
                break
            index += -1      
    return res

def BMM_func(user_dict, sentence):
    """
    反向最大匹配（BMM）
    :param user_dict:词典
    :param sentence:句子
    """
    # 词典中最长词长度
    max_len = max([len(item) for item in user_dict])
    start = len(sentence)
    res=[]
    while start != 0:
        index = start - max_len
        if index < 0:
            index = 0
        for i in range(max_len):
            if (sentence[index:start] in user_dict):
                res.append([index,start,tag2cn[user_dict[sentence[index:start]]]])
                start = index
                break
            if(len(sentence[index:start])==1):
                start = index
                break
            index += 1
    return res

def match(sentence, offset):
    dict={}
    with open('data_set/dict.txt', 'r') as f:
        for line in f.readlines():
            line = line.strip()
            k = line.split(' ')[0]
            v = line.split(' ')[1]
            dict[k] = v
    fmm=FMM_func(dict,sentence)
    bmm=BMM_func(dict,sentence)
    res=[]
    if(len(fmm)>len(bmm)):
        res=fmm
    else:
        res=bmm
    for list in res:
        list[0]+=offset
        list[1]+=offset
    return res

