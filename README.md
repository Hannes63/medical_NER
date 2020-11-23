# 中文命名实体识别



本项目参考的是https://github.com/luopeixiang/named_entity_recognition

## 数据集

本项目尝试使用了多种不同的模型（包括HMM，CRF，Bi-LSTM，Bi-LSTM+CRF）来解决中文命名实体识别问题，数据集用的是CCKS2019中医疗文本数据，数据的格式如下，它的每一行由一个字及其对应的标注组成，标注集采用BMOES，句子之间用一个空行隔开。

```
美	B-LOC
国	E-LOC
的	O
华	B-PER
莱	M-PER
士	E-PER

我	O
跟	O
他	O
谈	O
笑	O
风	O
生	O 
```

该数据集位于项目目录下的`data_set`文件夹里。

##快速开始

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
设置main.py中的train_model可选择训练的模型，设置preprocess_data=True可重新随机生成一次数据集（train，dev，test.char.bmes），在`./models/config.py`中可设置参数。

训练完毕之后，如果想要加载并评估模型，运行如下命令：

```shell
python3 test.py
```


可开始训练评估模型，




















