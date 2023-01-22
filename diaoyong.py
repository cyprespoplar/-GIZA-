import os
import fenci

def main(enfiles, cnfiles):
    '''
    此处为读取文字信息，将文本格式进行处理，得到双语语料，之后调用GIZA++程序，实现中英文的文本对齐
    GIZA++程序为四个可执行文件，在本处使用linux命令耐用执行，分别为plain2snt.out，snt2cooc.out、GIZA++、mkcls
    调用main函数来启动程序
    '''

    enfilepath = "enfile.txt"
    cnfilepath = "cnfile.txt"
    # 调用fenxi模块，进行词性标注
    cnfiles = fenci.main(cnfiles)

    # 读取英文文件到txten中
    with open(enfilepath, "r") as f:
        txten = f.readlines()
        f.close()

    # 将读出的英文末尾加换行，同时将其反转并组装成新的txtens写入源文件
    with open(enfilepath, "w") as f:
        enfiles += "\n"
        txten.append(enfiles)
        txten.reverse()
        txtens = ""
        for item in txten:
            txtens += item
        f.write(txtens)
        f.close()

    # 读取中文文件到txtcn中
    with open(cnfilepath, "r") as f:
        txtcn = f.readlines()
        f.close()

    # 将读出的中文末尾加换行，同时将其反转并组装成新的txtcns写入源文件
    with open(cnfilepath, "w") as f:
        cnfiles += "\n"
        txtcn.append(cnfiles)
        txtcn.reverse()
        txtcns = ""
        for item in txtcn:
            txtcns += item
        f.write(txtcns)
        f.close()
    # 下面为linux命令，在os模块中通过调用system执行

    # 执行plain2snt.out程序，参数为中英文文本所在路径，作用为为中英文词编号
    # 得到enfile.vcb、cnfile.vcb、cnfile_enfile.snt、enfile_cnfile.snt四个文件
    os.system("./plain2snt.out " + cnfilepath + " " + enfilepath)

    # 执行snt2cooc.out程序，生成中英文共现文件
    # 输入为cnfile.vcb enfile.vcb cnfile_enfile.snt，输出到cnfile_enfile.cooc文件中，下行同理
    os.system("./snt2cooc.out cnfile.vcb enfile.vcb cnfile_enfile.snt > cnfile_enfile.cooc")
    os.system("./snt2cooc.out enfile.vcb cnfile.vcb enfile_cnfile.snt > enfile_cnfile.cooc")

    # 生成中英文词类 opt为优化输出的命令
    # .vcb.classes文件表示单词所属类别编号
    os.system("./mkcls -pcnfile.txt -Vcnfile.vcb.classes opt")
    os.system("./mkcls -penfile.txt -Venfile.vcb.classes opt")

    # 建立中英文对应的输出文件夹，否则没有输出文件夹GIZA++会报错
    if not os.path.exists("z2e"):
        os.mkdir("z2e")
    if not os.path.exists("e2z"):
        os.mkdir("e2z")

    # 执行GIZA++的执行文件，使中英文本对齐
    # 参数：
    # -o 文件前缀
    # -OutputPath 输出所有文件到文件夹
    # 最终的输出文件存储在e2z和z2e两个文件夹中
    os.system(
        "./GIZA++ -S cnfile.vcb -T enfile.vcb -C cnfile_enfile.snt -CoocurrenceFile cnfile_enfile.cooc -o z2e -OutputPath z2e")
    os.system(
        "./GIZA++ -S enfile.vcb -T cnfile.vcb -C enfile_cnfile.snt -CoocurrenceFile enfile_cnfile.cooc -o e2z -OutputPath e2z")

    # 此处为删除程序执行过程文件
    os.system("rm enfile.vcb")
    os.system("rm cnfile.vcb")
    os.system("rm enfile.vcb.classes")
    os.system("rm enfile.vcb.classes.cats")
    os.system("rm cnfile.vcb.classes")
    os.system("rm cnfile.vcb.classes.cats")
    os.system("rm enfile_cnfile.cooc")
    os.system("rm enfile_cnfile.snt")
    os.system("rm cnfile_enfile.cooc")
    os.system("rm cnfile_enfile.snt")