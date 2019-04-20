# 拼音输入法

清华大学计算机系 2018-2019 学年人工智能导论课程第一次大作业

## 简介

这是一个基于 HMM（Hidden Markov Model，隐马尔可夫模型），并使用 python3 实现的拼音输入法。

除课程要求实现的内容外，本项目额外实现“分字”功能，即支持**不用空格隔开**各字的拼音。比如：若输入 `pinyinshurufa`，将预期得到 `拼音输入法`。

git 仓库地址：[https://github.com/wangyurzee7/pinyin](https://github.com/wangyurzee7/pinyin)

## 目录结构及文件

* `main.py`：main 文件，可以直接运行

* `getacc.py`：用于计算准确率

* `src/`：其他源代码及所需数据存放的位置

    * `src/utils.py`：一些工具
    
    * `src/pre.py`：用于预处理（训练模型）
    
    * `src/hmmpinyin.py`：包装 HMM 拼音输入法的类
    
    * `src/yazidhmm.py`：手动实现的 HMM 模型
    
    * `src/pinyinseg.py`：分字模型
    
    * `src/__test.py`：一个小测试

* `data/`：存放测试数据文件（其中后缀名 `in`/`ans`/`out`/`out.segres` 分别代表输入、答案、输出、进行分字的输出）

## 依赖

本项目依赖 Python 库 `numpy`、`progressbar`，如果你安装了 `pip`，你可以执行下列指令来安装它们：

```
$ pip install numpy
$ pip install progressbar
```

此外，我们的输入法还实现了基于 `hmmlearn` 库的版本，如果你想使用它（使用方法将在后面提到，但请注意它很慢），你可以执行 `pip install hmmlearn` 来安装这个库及相关依赖库，但这并不是必须的。

## 使用

### 训练模型

执行下列指令可以运行 `pre.py` 即可进行模型训练：

```
$ python3 pre.py [char_file] [map_file] [doc_list] [result_path] [ignore_threshold=1.0] [add=0]
```

参数含义如下：

* `char_file`：字表文件（下发）

* `map_file`：拼音对照表文件（下发）

* `doc_list`：语料库文件表：这是一个 `json` 文件，其中存放一个列表，列表中的每个元素是一个 `json` 对象，其字段及意义分别为

    * `file`：文件名
    
    * `rate`：学习系数，表示权重
    
    * 这是一个例子：`{"file": "./yaziddoc.txt", "rate": 1}`

* `result_path`：模型存放位置（训练过程中会进行不定期保存，也将存放到这里）

* `ignore_threshold`：一个系数，将决定被忽略的低频词的频率。这个值越大，模型文件将越轻量级，但准确率也将更低。这个值**缺省为 1**，但经过实（nao）验（bu），我们建议的取值为 0.1

* `add`：是否为在现有模型基础上继续训练，0 表示不补训；1 表示补训，将在目标位置现有模型的基础上进行继续训练，**缺省为 0**。

训练将得到 `mat.json` 文件及 `maps.json` 文件。

### 模型使用

通过引用 `src/hmmpinyin.py` 中的 `HmmPinyin` 类来调用模型

其构造函数包含参数：

* `model_path="data/model/"`：模型所在目录

* `mat_file=None`：单独指定 `mat.json` 文件，默认为 `None` 时即在 `model_path` 中寻找

* `maps_file=None`：单独指定 `maps.json` 文件，默认为 `None` 时即在 `model_path` 中寻找

* `predictor="yazidhmm"`：使用的 HMM 模型，合法取值包括 `yazidhmm` 或 `hmmlearn`，其中前者为手动实现的 HMM 模型，后者为调用 `hmmlearn` 库中现有模型

**该类成员函数 `predict(st)` 将返回对拼音串 `st` 的汉字结果预测。**

### main.py

执行下列指令来运行 main：

```
$ python3 main.py [input] [output]
```

按照要求、并顾名思义地，`input` 与 `output` 分别对应输入输出文件。特别地：

* 当两者均缺省时，使用标准输入输出来交互。输入空行可退出程序。

* 当输出文件缺省时，从文件输入，并输出到标准输出。

* 当两者均不缺省时，会在输出文件的文件夹下，输出一个以 `[output].segres` 为文件名的输出文件，其对应**忽略输入中的空格**，并调用分字模块后的输出结果。

### getacc.py

执行下列指令来得到准确率：

```
$ python3 getacc.py [file1] [file2]
```

这个程序可以统计你的**单字准确率**（将忽略字数与答案不匹配的句子）及**句子准确率。输出格式如下：

```
acc of sentences = 139/797 = 17.44040150564617% ;  acc of chars = 4613/6342 = 72.7373068432671%
```

## 环境

本实验在以下二环境中均能正常运行（其中前者是一个 WSL（Windows Subsystem of Linux））：

```
$ lsb_release -a
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 18.04.2 LTS
Release:        18.04
Codename:       bionic
$ python3 --version
Python 3.6.7
```

```
$ lsb_release -a
LSB Version:    core-9.20160110ubuntu0.2-amd64:core-9.20160110ubuntu0.2-noarch:security-9.20160110ubuntu0.2-amd64:security-9.20160110ubuntu0.2-noarch
Distributor ID: Ubuntu
Description:    Ubuntu 16.04.6 LTS
Release:        16.04
Codename:       xenial
$ python3 --version
Python 3.5.2
```

## 一些例子

```
pin yin shu ru fa
拼音输入法
qing hua da xue ji suan ji xi
清华大学计算机系
wo jue de skr
我觉得skr
xi huan chang tiao rap lan qiu
喜欢唱跳rap篮球
pinyinshurufa
拼音输入法
zhongguoxian
中国西安
zhongguoxianzaizhengzaigaosufazhan
中国现在正在高速发展
zhong guo xian
中国现
wojuedeskr
我觉得skr
xihuanchangtiaoraplanqiu
喜欢唱跳rap篮球
```
