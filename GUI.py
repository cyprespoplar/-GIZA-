import tkinter as tk
import Maintest
import threading
from PIL import Image, ImageTk


class GUI:

    def __init__(self):
        '''
        规定窗口基本格式：大小650×600，题目为“汉英文本对齐系统”
        '''
        self.root = tk.Tk()
        self.root.title('汉英文本对齐系统')
        self.root.geometry("650x600")
        self.root.resizable(width=False, height=False)
        self.interface()

    def interface(self):
        '''
        本段规定gui界面类的各个属性，包括操作标签，介绍，输入框以及提示
        :return:
        '''
        self.btn = tk.Button(self.root, text="对齐", font=("fangsong ti", 12), command=self.event)
        self.btn.place(x=0, y=500, width=100, height=30)

        self.ZTLabel = tk.Label(self.root, font=("song ti", 12), anchor='w')
        self.ZTLabel["text"] = "本程序由顾桉丞，李锦宇，刘勇奇，宋奕骁四人小组开发，用于进行汉英文本自动对齐。\n本程序内核调用GIZA++程序，最终输出结果为out.jpg图片，自动保存在该目录下"
        self.ZTLabel.place(x=0, y=0)

        self.cnLabel = tk.Label(self.root, font=("song ti", 12), anchor='w')
        self.cnLabel["text"] = "请输入中文语句"
        self.cnLabel.place(x=0, y=70)

        self.cnet = tk.StringVar()
        self.cnentry = tk.Entry(self.root, font=("fangsong ti", 18), textvariable=self.cnet)
        self.cnentry.place(x=0, y=100, width=300)

        self.enLabel = tk.Label(self.root, font=("song ti", 12), anchor='w')
        self.enLabel["text"] = "请输入英文语句"
        self.enLabel.place(x=0, y=170)

        self.enet = tk.StringVar()
        self.enentry = tk.Entry(self.root, font=("fangsong ti", 18), textvariable=self.enet)
        self.enentry.place(x=0, y=200, width=300)

        self.fcLabel = tk.Label(self.root, font=("song ti", 12), anchor='w')
        self.fcLabel["text"] = "中文分词结果"
        self.fcLabel.place(x=0, y=270)

        self.fcjgLabel = tk.Label(self.root, font=("fangsong ti", 18), anchor='w')
        self.fcjgLabel["text"] = ""
        self.fcjgLabel.place(x=0, y=300)

        self.dqLabel = tk.Label(self.root, font=("song ti", 12), anchor='w')
        self.dqLabel["text"] = "汉英对齐结果"
        self.dqLabel.place(x=0, y=370)

        self.dqjgLabel = tk.Label(self.root, font=("fangsong ti", 18), anchor='w')
        self.dqjgLabel["text"] = ""
        self.dqjgLabel.place(x=0, y=400)

        self.YXZTLabel = tk.Label(self.root, font=("fangsong ti", 18), anchor='w')
        self.YXZTLabel["text"] = ""
        self.YXZTLabel.place(x=150, y=500)

        self.ZTendLabel = tk.Label(self.root, font=("song ti", 12), anchor='w')
        self.ZTendLabel["text"] = "本程序执行时间大概在30s左右，请耐心等待!"
        self.ZTendLabel.place(x=0, y=550)

    def event(self):
        if not self.YXZTLabel["text"] == "正在运行中……":
            self.YXZTLabel["text"] = "正在运行中……"

        eninput = self.enet.get()
        cninput = self.cnet.get()
        try:
            [fcstr, dqstr] = Maintest.main(eninput, cninput)
            self.fcjgLabel["text"] = fcstr
            self.dqjgLabel["text"] = dqstr
            photo = ImageTk.PhotoImage(Image.open('out.jpg').resize((320, 240)))
            self.ImageLabel = tk.Label(self.root, image=photo)
            self.ImageLabel.image = photo
            self.ImageLabel.place(x=350, y=80)
        except:
            self.YXZTLabel["text"] = "运行错误！"
        else:
            self.YXZTLabel["text"] = "运行结束"

    def start(self):
        self.T = threading.Thread(target=self.event)
        self.T.setDaemon(True)
        self.T.start()


if __name__ == '__main__':
    a = GUI()
    a.root.mainloop()
