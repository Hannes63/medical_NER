# 中文命名实体识别



本项目参考的是https://github.com/luopeixiang/named_entity_recognition

## 数据集

本项目尝试使用了多种不同的模型（包括HMM，CRF，Bi-LSTM，Bi-LSTM+CRF）来解决中文命名实体识别问题，数据集用的是CCKS2019中医疗文本数据(.txt, .json)，通过`./preprocess.py`的预处理后得到三个大小为6:2:2的数据集（`train.char.bmes, dev.char.bmes, val.char.bmes`），数据的格式如下，它的每一行由一个字及其对应的标注组成，标注集采用BMOES，每条数据之间用一个空行隔开。

```
患 O
者 O
因 O
食 B-ILL_DIAG
管 M-ILL_DIAG
癌 E-ILL_DIAG
来 O
我 O
院 O
诊 O
治 O
， O
腹 S-SITE
部 O
无 O
异 O
样 O
```

该数据集位于项目目录下的`data_set`文件夹里。

## 快速开始

首先安装依赖项：
```
pip3 install -r requirement.txt
```
安装完毕之后，直接使用
```
python main.py
```
即可训练以及评估模型，评估模型将会打印出模型的精确率、召回率、F1分数值以及混淆矩阵，如果想要修改相关模型参数或者是训练参数，可以在`./models/config.py`文件中进行设置。
训练好的模型会保存至`./ckpts`，调用utils.load_model()可使用。
设置main.py中的train_model可选择训练的模型，设置preprocess_data=True可重新随机生成一次数据集（train，dev，test.char.bmes）

训练完毕之后，如果想要加载并评估模型，运行如下命令：

```shell
python3 test.py
```


可开始训练评估模型。


## 待完成任务
大致阅读代码结构，任务详情见`./predict.py`
### 1. 投票机制
1.首先进行各个模型的误差分析（精确率、召回率、F1值等）；

2.其次尝试设计一个线性模型$a_1$：
$y(s) = a1*y1(s) + a2*y2(s) + a3*y3(s) + a4*y4(s)$

$y1(s)...y4(s)\in \{0,1\}$为四个模型识别某个待确认命名实体s的结果,
$a1,a2,a3,a4\in \[0,1\]$为需要认为设置的参数（各个模型的权重）；
$z(s) = int(y(s) > 0.5)$为投票结果。

3.考虑是否存在$s1$为$s2$的字串，且$s1$和$s2$被不同模型识别出来的情况；

4.最后再对这个模型进行误差分析。综合以上得到误差分析报告。

**任务截止时间**：`12月7日`前上传至github

### 2. 建立字典
1.设计`make_dictionary`程序，将所有的未识别出来的实体加入字典（训练集，验证集，测试集），然后保存（如保存至`dictionary.txt`）；

2.在`look_up_dict`中对`vote`之后的文本进行匹配（最大匹配等）；

3.进行误差分析。

**任务截止时间**：`12月14日`前上传至github

### 3.设计客户端
要求见需求报告；调用`./predict.py`中的`synthetical_predict(sentence)`，即可返回sentence中的命名实体。如最上面的文本返回`[[3,6,'疾病和诊断'], [12,13,'解剖部位']]`。







