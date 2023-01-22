# -GIZA-
## 项目介绍
我们实现的是汉英词语自动对齐系统。
核心思想：参照了在分词算法中较为流行的 GIZA++ 的源码作为蒙版，
进行进一步的改写与移植来实现我们的平台。然后在 GUI 中实现用户与程
序的交互。
下面简要介绍 GIZA++ 算法：GIZA++ 完整的实现了（Brown）描述
的独立与词集的 IBM-4 对齐模型；实现了 IBM-5. 实现了 HMM 对齐模型，
并且改进了 IBM-1，IBM-2，和 HMM 模型的概率计算算法。
GIZA++ 属于开源代码：已在 Github 中开源：https://github.com/mosessmt/giza-pp，codechina 中也有加速镜像的项目：https://codechina.csdn.net/mirrors/mosessmt/giza-pp.git
GIZA++ 主要包含了一下几个程序：
1.GIZA++ 本身
2.Plain2snt.out 将普通文本转换成 GIZA 格式
3.Snt2plain.out 将 GIZA 格式文本转换成普通文本
4.Snt2cooc.out 用 GIZA 格式文本生成共线文件
GIZA 的主要使用流程是：
首先 git 下来项目，cd 到 giza-pp 目录下进行 make 编译。
编译完后生成 plain2snt.out、snt2cooc.out、GIZA++、mkcls 四个可执行文
件。
