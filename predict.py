# -*- coding:utf-8 -*-
from dict import match
from utils import load_model, prepocess_data_for_lstmcrf, flatten_lists


def predict(model_name, sentence):
    """
    :param model_name: one of four trained model
    :param sentence: a string to be predicted
    :return: [[b_pos_1, e_pos_1, tag_1], ..., [b_pos_n, e_pos_n, tag_n]]
    left closed, right open
    """
    assert model_name in ['bilstm', 'bilstm_crf', 'crf', 'hmm', 'vote4']
    tag2cn = {'SITE': '解剖部位', 'ILL_DIAG': '疾病和诊断', 'CHECK': '检验',
              'OPS': '手术', 'DRUG': '药物', 'EXAM': '检查', 'IMAGE': '影像检查',
              'LAB': '实验室检验'}
    pred_tag_list = []
    test_word_list = list(sentence)
    if model_name != 'vote4':
        model = load_model('./ckpts/' + model_name + '.pkl')
        if model_name == 'bilstm':
            pred_tag_list = model.test([test_word_list], [0])[0][0]
        elif model_name == 'bilstm_crf':
            test_word_list, _ = prepocess_data_for_lstmcrf([test_word_list], [[0]], test=True)
            pred_tag_list = model.test(test_word_list, [0])[0][0]
        elif model_name in ['hmm', 'crf']:
            pred_tag_list = model.test([test_word_list])[0]
    else:
        model1 = load_model('./ckpts/hmm.pkl')
        pred1 = flatten_lists(model1.test([test_word_list])[0])
        model2 = load_model('./ckpts/crf.pkl')
        pred2 = flatten_lists(model2.test([test_word_list])[0])
        model3 = load_model('./ckpts/bilstm.pkl')
        pred3 = flatten_lists(model3.test([test_word_list], [0])[0][0])
        model4 = load_model('./ckpts/bilstm_crf.pkl')
        test_word_list, _ = prepocess_data_for_lstmcrf([test_word_list], [[0]], test=True)
        pred4 = flatten_lists(model4.test(test_word_list, [0])[0][0])
        results = [pred1, pred2, pred3, pred4]

        for result in zip(*results):
            # ensemble_tag = Counter(result).most_common(1)[0][0]
            weight_result = {tag: 0 for tag in result}
            weight_result[result[0]] += 0.9133
            weight_result[result[1]] += 0.9620
            weight_result[result[2]] += 0.9559
            weight_result[result[3]] += 0.9585
            ensemble_tag = max(weight_result, key=weight_result.get)
            pred_tag_list.append(ensemble_tag)

    result = []
    begin_index = 0
    for i in range(len(pred_tag_list)):
        if pred_tag_list[i][0] == 'S':
            result.append([i, i + 1, tag2cn[pred_tag_list[i][2:]]])
        elif pred_tag_list[i][0] == 'B':
            begin_index = i
        elif pred_tag_list[i][0] == 'E':
            result.append([begin_index, i + 1, tag2cn[pred_tag_list[i][2:]]])
    return result


def vote(sentence):
    """
    同时用四个训练好的模型进行预测，将各自结果进行综合后得到最终结果。
    TODO:
        1.首先进行各个模型的误差分析（精确率、召回率、F1值等）；
        2.其次尝试设计一个线性模型：
        y(s) = a1*y1(s) + a2*y2(s) + a3*y3(s) + a4*y4(s)
        y1(s)...y4(s)\in {0,1}为四个模型识别某个待确认命名实体s的结果,
        a1,a2,a3,a4\in [0,1]为需要认为设置的参数（各个模型的权重）；
        z(s) = int(y(s) > 0.5)为投票结果。
        3.考虑是否存在s1为s2的字串，且s1和s2被不同模型识别出来的情况；
        4.最后再对这个模型进行误差分析。综合以上得到误差分析报告。
    :param sentence: a string to be predicted
    :return: the same as 'predict' function above
    """
    result = predict('vote4', sentence)

    return result


def look_up_dict(sentence):
    """
    在进行过投票预测后，再在剩余文本中在预先建立好的字典里进行匹配，尝试识别更多命名实体；
    要求最终synthetical_predict返回的结果的召回率为（尽可能等于）100%（即识别出上一步中的true negtive），
    不必要求精确率为100%（即vote步骤中允许存在false positive）。
    TODO:
        1.设计make_dictionary程序，将所有的未识别出来的实体加入字典（训练集，验证集，测试集），
        然后保存（如保存至dictionary.txt）；
        2.在look_up_dict中对vote之后的文本进行匹配（最大匹配等）；
        3.进行误差分析。
    :param sentence: a string to be predicted
    :return: the same as 'predict' function above
    """
    pred = vote(sentence)
    begin_index = 0
    result = []
    for entity in pred:
        if begin_index < entity[0]:
            result += match(sentence[begin_index:entity[0]], begin_index)
        begin_index = entity[1]
    if len(sentence[begin_index:]):
        result += match(sentence[begin_index:], begin_index)
    return result


def synthetical_predict(sentence):
    return vote(sentence) + look_up_dict(sentence)


def tag_predict(sentence):
    acronym = {'解剖部位': 'SITE', '疾病和诊断': 'ILL_DIAG', '检验': 'CHECK',
               '手术': 'OPS', '药物': 'DRUG', '检查': 'EXAM', '影像检查': 'IMAGE',
               '实验室检验': 'LAB'}
    ans = synthetical_predict(sentence)
    tag_list = ['O'] * len(sentence)
    for item in ans:
        tag_suffix = acronym[item[2]]
        if item[0] == item[1] - 1:
            tag_list[item[0]] = 'S-' + tag_suffix
        else:
            tag_list[item[0]] = 'B-' + tag_suffix
            for i in range(item[0] + 1, item[1] - 1):
                tag_list[i] = 'M-' + tag_suffix
            tag_list[item[1] - 1] = 'E-' + tag_suffix
    return tag_list

