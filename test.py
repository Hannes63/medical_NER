import sys

from utils import load_model, extend_maps, prepocess_data_for_lstmcrf
from data import build_corpus
from evaluating import Metrics
from evaluate import ensemble_evaluate

HMM_MODEL_PATH = './ckpts/hmm.pkl'
CRF_MODEL_PATH = './ckpts/crf.pkl'
BiLSTM_MODEL_PATH = './ckpts/bilstm.pkl'
BiLSTMCRF_MODEL_PATH = './ckpts/bilstm_crf.pkl'

REMOVE_O = False  # 在评估的时候是否去除O标记


def main(output_to_file):
    if output_to_file:
        print('正在生成测试结果...')
        __stdout__ = sys.stdout
        sys.stdout = open('./test/test_log.txt', 'a', encoding='utf-8')

    print("读取数据...")
    train_word_lists, train_tag_lists, word2id, tag2id = \
        build_corpus("train")
    # dev_word_lists, dev_tag_lists = build_corpus("dev", make_vocab=False)
    test_word_lists, test_tag_lists = build_corpus("test", make_vocab=False)

    print("加载并评估hmm模型...")
    hmm_model = load_model(HMM_MODEL_PATH)
    hmm_pred = hmm_model.test(test_word_lists)
    metrics = Metrics(test_tag_lists, hmm_pred, remove_O=REMOVE_O)
    metrics.report_scores()  # 打印每个标记的精确度、召回率、f1分数
    metrics.report_confusion_matrix()  # 打印混淆矩阵

    # 加载并评估CRF模型
    print("加载并评估crf模型...")
    crf_model = load_model(CRF_MODEL_PATH)
    crf_pred = crf_model.test(test_word_lists)
    metrics = Metrics(test_tag_lists, crf_pred, remove_O=REMOVE_O)
    metrics.report_scores()
    metrics.report_confusion_matrix()

    # bilstm模型
    print("加载并评估bilstm模型...")
    bilstm_model = load_model(BiLSTM_MODEL_PATH)
    bilstm_model.model.bilstm.flatten_parameters()  # remove warning
    lstm_pred, target_tag_list = bilstm_model.test(test_word_lists, test_tag_lists)
    metrics = Metrics(target_tag_list, lstm_pred, remove_O=REMOVE_O)
    metrics.report_scores()
    metrics.report_confusion_matrix()

    print("加载并评估bilstm+crf模型...")
    bilstm_model = load_model(BiLSTMCRF_MODEL_PATH)
    bilstm_model.model.bilstm.bilstm.flatten_parameters()  # remove warning
    test_word_lists, test_tag_lists = prepocess_data_for_lstmcrf(
        test_word_lists, test_tag_lists, test=True
    )
    lstmcrf_pred, target_tag_list = bilstm_model.test(test_word_lists, test_tag_lists)
    metrics = Metrics(target_tag_list, lstmcrf_pred, remove_O=REMOVE_O)
    metrics.report_scores()
    metrics.report_confusion_matrix()

    print("加载并评估vote模型...")
    ensemble_evaluate(
        [hmm_pred, crf_pred, lstm_pred, lstmcrf_pred],
        test_tag_lists
    )

    print("加载并评估dictionary+vote模型...")
    dict_pred = []
    metrics = Metrics(target_tag_list, dict_pred, remove_O=REMOVE_O)
    metrics.report_scores()
    metrics.report_confusion_matrix()

    if output_to_file:
        sys.stdout.close()
        sys.stdout = __stdout__
        print('已生成测试结果到\'./test/test_log.txt\'')
        
        
if __name__ == "__main__":
    output = True
    main(output)
