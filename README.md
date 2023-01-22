# -GIZA-
## 项目介绍
汉英词语自动对齐系统。
核心思想：在分词算法中较为流行的 GIZA++ 的源码作为模版，
进行进一步的改写与移植来实现我们的平台。然后在 GUI 中实现用户与程
序的交互。
下面简要介绍 GIZA++ 算法：GIZA++ 完整的实现了（Brown）描述
的独立与词集的 IBM-4 对齐模型；实现了 IBM-5. 实现了 HMM 对齐模型，
并且改进了 IBM-1，IBM-2，和 HMM 模型的概率计算算法。
GIZA++ 属于开源代码：已在 Github 中开源：https://github.com/moses-smt/giza-pp，codechina 中也有加速镜像的项目：https://codechina.csdn.net/mirrors/mosessmt/giza-pp.git
### GIZA++介绍
GIZA++ 主要包含了一下几个程序：

1.GIZA++ 本身
2.Plain2snt.out 将普通文本转换成 GIZA 格式
3.Snt2plain.out 将 GIZA 格式文本转换成普通文本
4.Snt2cooc.out 用 GIZA 格式文本生成共线文件
GIZA 的主要使用流程是：

首先 git 下来项目，cd 到 giza-pp 目录下进行 make 编译。
编译完后生成 plain2snt.out、snt2cooc.out、GIZA++、mkcls 四个可执行文
件。

首先将准备好的训练的双语语料库分别存放到文件中，也就是 en.txt 和
zh.txt 文件。
然后运行命令进行词对齐。
~~~linux
 ./plain2snt.out zh.txt en.txt
 ~~~
 得到 en.vcb、zh.vcb、en_zh.snt、zh_en.snt 四个文件。en.vcb / zh.vcb 都
是字典文件，en_zh.snt / zh_en.snt 中编号表示句对，第一行表示句对出现
次数，

接下来执行命令生成共现文件：
~~~
./snt2cooc.out zh.vcb en.vcb zh_en.snt > zh_en.cooc
./snt2cooc.out en.vcb zh.vcb en_zh.snt > en_zh.cooc
~~~
接下来执行命令生成词类：
~~~
./mkcls -pzh.txt -Vzh.vcb.classes opt
./mkcls -pen.txt -Ven.vcb.classes opt
~~~

en.vcb.classes / zh.vcb.classes 是单词所属类别编号，en.vcb.classes.cats /
zh.vcb.classes.cats 是类别所拥有的一组单词。执行 GIZA++，先在当前目
录新建两个输出文件夹 z2e、e2z，我们会将文件输出到这两个文件夹中。

~~~
./GIZA++ -S zh.vcb -T en.vcb -C zh_en.snt -CoocurrenceFile
zh_en.cooc -o z2e -OutputPath z2e
2 ./GIZA++ -S en.vcb -T zh.vcb -C en_zh.snt -CoocurrenceFile
en_zh.cooc -o e2z -OutputPath e2z
~~~
输出的文件中，z2e.perp 是困惑度。
z2e.a3.final 文件里有 i j l m p(i/j, l, m)，其中 i 代表源语言 Token 位
置；j 代表目标语言 Token 位置；l 代表源语言句子长度；m 代表目标语言
句子长度。
z2e.d3.final 类似于 z2e.a3.final 文件，只是交换了 i 和 j 的位置。
z2e.n3.final 中 source_id p0p1p2 . . . pn；源语言 Token 的 Fertility 分别
为 0,1,…,n 时的概率表，比如 p0 是 Fertility 为 0 时的概率。
z2e.t3.final：s_id t_id p(t_id/s_id)；IBM Model 3 训练后的翻译表；
p(t_id/s_id) 表示源语言 Token 翻译为目标语言 Token 的概率。
z2e.A3.final 是单向对齐文件，数字代表 Token 所在句子位置（1 为起
点）。
z2e.d4.final 是 IBM Model 4 翻译表。
z2e.D4.final 是 IBM Model 4 的 Distortion 表。

其中的单向对齐文件就是我们所需要的结果，很显然并不直观，并且
GIZA++ 程序只能运行 Linux 中并且全部需要命令行操作非常的繁琐，而
且还需要用户自己准备语料库，使用起来也不是很轻松。
以上便是 GIZA++ 的源码解读和正确使用方法，接
下来便是系统主要模块流程。

### 初始化-exchange.py
exchange.py 的作用是将从网上下载的 LDC 语料库转化成便于读取的
txt 文件。从开放数据平台 LDC-宾夕法尼亚大学官网下载的 LDC2019T13
数据集，这个数据集大多为日常口语交流和一些非正式的场合使用的语句，
有中文和英文平行的译本大约 10 万句。该语料库下载之后会提供两个文
件夹，里面对应存储的是中文语句和对应翻译的英文语句，我们的 exhcnage.py 程序便是将文件夹中的中英文翻译读取，排好序后写入 enfile.txt
和 cnfile.txt 两个文件。

首先需要将存储在 cn，en 文件夹中的中英文语句的文件名列表，并排
好序，以保证中文和英文是句句对应的。
接下来，我们将列表中的文件信息都读取出来，并写入我们准备好的
cnfile.txt 和 enfile.txt。

### 调用可执行文件-diaoyong.py
diaoyong.py 的主要功能为调用编译 GIZA 原码获得的四个可执行文
件：mkcls、plain2snt.out、snt2cooc.out、GIZA++，将获得的最终结果输
出到 z2e 和 e2z 两个文件夹中并且删除中间文件。
首先，我们接受用户输入的中文语句和对应的英文翻译。当然，用户输
入的中文语句一般不会进行分词。所以，我们选择写一个基于统计的分词程
序，该分词程序采取的语料库为人民日报语料库。核心
的是 Viterbi 算法。
准备好训练集之后，我们通过 python 中的 os.system() 方法来调用
GIZA 的可执行文件。首先，我们调用命令进行词对齐。
在进行词对齐之后，我们会得到对应的中间文件。在之后，我们生成共
现文件，生成共现文件之后，我们进一步调用可执行文件，构建词类。
在构建词类之后，我们需要创建两个文件夹 z2e 和 e2z 用来存放输出
结果。
### 分析结果-fenxi.py
fenxi.py 的功能是将 z2e 中的单向对齐文件结果 z2e.A3.final 读取出来，
并且根据其结果将最后的图绘制出来并保存在当前目录下的 out.jpg。
### GUI.py 
GUI.py是基于 Tkinter 库编写的 GUI 可视化代码。
### 实验结果
![image](https://user-images.githubusercontent.com/98015436/213904372-f42fc9fe-acdb-4c53-92f9-6d171a9284ad.png)
![image](https://user-images.githubusercontent.com/98015436/213904387-3033598a-02ec-4e0f-9334-ee4955622ae0.png)
