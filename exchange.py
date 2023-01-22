import os

def main():
    '''
    处理中文英文语料库，读入以进行后续处理
    :return:两个文件
    '''
    fileenlist = os.listdir("./en")
    fileenlist = sorted(fileenlist)

    filezhlist = os.listdir("./cn")
    filezhlist = sorted(filezhlist)

    #print(len(filezhlist),len(fileenlist))
    zhfile = ""
    '''
    读取语料库并写入文件
    '''
    for filepath in filezhlist:
        filetruepath = str('./cn/' + filepath)
        with open(filetruepath) as f:
            for line in f:
                zhfile += line
    with open("cnfile.txt", "w") as f:
        f.write(zhfile)

    enfile = ""
    for filepath in fileenlist:
        filetruepath = str('./en/' + filepath)
        with open(filetruepath) as f:
            for line in f:
                enfile += line
    with open("enfile.txt", "w") as f:
        f.write(enfile)