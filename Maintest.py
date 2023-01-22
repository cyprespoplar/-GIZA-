import fenxi
import exchange
import diaoyong
import os
'''
导入执行test文件需要的包
'''

def main(enfile, cnfile):
    '''
    调用函数，执行测试检测执行效果
    :param enfile:英文语料库
    :param cnfile:中文语料库
    :return:fcstr，dqstr
    '''
    if os.path.exists("z2e") and os.path.exists("e2z"):
        os.system("rm -rf z2e")
        os.system("rm -rf e2z")

    if not os.path.exists("cnfile.txt") or not os.path.exists("enfile.txt"):
        exchange.main()

    diaoyong.main(enfile, cnfile)

    [fcstr, dqstr] = fenxi.main()
    return fcstr, dqstr
