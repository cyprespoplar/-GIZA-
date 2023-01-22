import os
import matplotlib.pyplot as plt
from matplotlib import font_manager

def main():
    # 打开单向对齐文件，数字代表Token所在句子位置（1为起点）
    with open("z2e/z2e.A3.final") as f:
        txt = f.readlines()
        f.close()
    # print(txt)

    # 获取英文数据
    # I like natural language classes \n
    endata = txt[1].split()
    # 获取中文数据
    # NULL ({ }) 我 ({ 1 }) 喜欢 ({ 2 }) 自然 ({ 3 }) 语言 ({ 4 }) 课程 ({ 5 }) \n
    dqdata = txt[2].split(")")
    for item in range(len(dqdata)):
        dqdata[item] = dqdata[item].split("(")

    # 存放对齐结果的字典，键是中文，值对应的位置
    dqdatas = {}

    # 截取对齐数据
    dqdata = dqdata[:-1]

    # 将对齐数据转换为字典
    for item in dqdata:
        item[1] = item[1][1:-1].strip()
        item[1] = item[1].split()
        item[0] = item[0].strip()
        dqdatas[item[0]] = item[1]

    # 截取中文分词结果
    cndata = list(dqdatas.keys())[1:]

    # 存放坐标
    tu = list()
    # 点的横坐标
    tx = []
    # 点的纵坐标
    ty = []

    # 获取点即中英文位置对应关系
    for i in range(len(cndata)):
        cndatas = list(dqdatas[cndata[i]])
        for item in cndatas:
            tu.append((i + 1, eval(item)))
            tx.append(i + 1)
            ty.append(eval(item))

    cnstr = ""      # 中文分词结果
    for item in cndata:
        cnstr += item
        cnstr += " "

    # 插入两坐标轴原点
    endata.insert(0, "英文")
    cndata.insert(0, "中文")

    # 设置图片字体
    my_font = font_manager.FontProperties(fname=(r'微软雅黑.ttf'))

    # 设置横纵坐标，设置图片标题
    plt.scatter(tx, ty)
    plt.xticks(range(len(cndata)), cndata, fontproperties=my_font)
    plt.yticks(range(len(endata)), endata, fontproperties=my_font)
    plt.title("最终结果", fontproperties=my_font)

    # 保存图片
    plt.savefig("./out.jpg")

    fcstr = ""    # 对齐结果
    for item in tu:
        fcstr += str(item)
        fcstr += " "
    # print("对齐结果为：", fcstr)

    # 删除z2e和e2z两个文件夹
    os.system("rm -rf z2e")
    os.system("rm -rf e2z")

    # 返回中文分词结果和对齐结果
    return cnstr, fcstr