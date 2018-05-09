#!/usr/bin/pyhton3
#-*- coding:utf-8 -*-


"""
    目的：
        实现制作脚本简单化
        如果失控了，需要中断PyAutoGUI函数，就把鼠标光标在屏幕左上角。
"""
import os
import time
import random
import time
import cv2
import numpy
import image
import pyautogui
# import win32api,win32gui,win32con
import win32com.client
import numpy as np
from matplotlib import pyplot as plt


DEBUG = False
bulefont='\033[34;1m'
fontend='\033[0m'
redfont="\033[1;31m"

def log(text,show=0):
    def decorator(func):
        def wrapper(*args, **kw):
            if show:
                for x in args:
                    for j in kw :
                        print('%s[%s]%s[%s] %s(%s,%s)' % (bulefont,text,fontend,time.asctime( time.localtime(time.time()) ), func.__name__,x,j))
            elif show==0:
                print('%s[%s]%s[%s] %s' % (bulefont, text, fontend, time.asctime(time.localtime(time.time())), func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator


dm = win32com.client.Dispatch('dm.dmsoft')
# hwnd = dm.FindWindow("Win32Window0", "阴阳师-网易游戏")
hwnd = dm.FindWindow("LDPlayerMainFrame", "雷电模拟器")
dm.MoveWindow(hwnd,0, 0)
scereen=dm.GetWindowRect(hwnd)
if scereen[0]==0:
    scereen=[1,0,0,2000,2000]
#鼠标后台，截图后台
# dm.BindWindow(hwnd, "dx2", "dx2", "normal", 0)

#如果失控了，需要中断PyAutoGUI函数，就把鼠标光标在屏幕左上角。
pyautogui.FAILSAFE = True
#可以为所有的PyAutoGUI函数增加延迟。默认延迟时间是0.1秒。在函数循环执行的时候，这样做可以让PyAutoGUI运行的慢一点，非常有用。
pyautogui.PAUSE = 0

def tap(x,y,clicks=1,button="left",delay=0.2,xOffset=0,yOffset=0,delay2=0,delay3=0.03,delay4=0.02,click_type=1):
    """
    用鼠标点击
    :param delay: 方式一鼠标移动到 x,y 时经过的延时
    :param x: 点击处的x数值
    :param y: 点击处的y数值
    :param xoffset: x的偏移（或补偿） 正数为增加
    :param yoffset: y的偏移（或补偿） 正数为增加
    :param delay2: 进行偏移移动的延时
    :param delay3: 点击次数之间的延时
    :param delay4: 方式二移动到目标之间的延时
    :param clicks: 点击次数
    :param button: 按键 可以设置成left，middle和right
    :click_type: 方式1：模拟细致 ，方式二：不细致
    :return:
    """
    if click_type==1:
        pyautogui.moveTo(x,y,duration=delay,tween=pyautogui.easeInQuad)
        pyautogui.moveRel(xOffset, yOffset, duration=delay2)
        pyautogui.click()
    elif click_type==2:
        pyautogui.click(x,y,clicks=clicks,interval=delay3,duration=delay4,button=button,tween=pyautogui.easeInQuad)#
def swipe(x1,y1,x2,y2,delay=0.5,x1Offset=0, y1Offset=0,delay2=0,delay3=0.5,button='left'):
    """
    用鼠标，从x1,y1 拖动到 x2,y2
    :param x1: 起点x坐标
    :param y1: 起点y坐标
    :param delay: 鼠标移动到起始坐标的时间延时
    :param x1Offset: 起始坐标的x偏移
    :param y1Offset: 起始坐标的y偏移
    :param delay2:  进行偏移移动的时间延时
    :param x2: 终点坐标
    :param y2: 终点y坐标
    :param delay3: 拖动过程中的延时
    :param button: 用鼠标哪个键 可以设置成left，middle和right三个键
    :return:
    tween:
        pyautogui.easeInQuad光标移动呈现先慢后快的效果，整个过程的时间还是和原来一样。
        pyautogui.easeOutQuad函数的效果相反：光标开始移动很快，然后慢慢减速。
        pyautogui.easeOutElastic是弹簧效果，首先越过终点，然后再反弹回来
    """
    pyautogui.moveTo(x1, y1, duration=delay,tween=pyautogui.easeInQuad)
    pyautogui.moveRel(x1Offset, y1Offset, duration=delay2)
    pyautogui.dragTo(x2, y2,duration=delay3,button=button)

class PartOfTheScreen(object):
    #             屏幕上一块区域名字 此区域的中心坐标 此区域的半径 操作此区域的条件 操作此区域的方法  区域图片的路径位置
    #             name,               center_xy,         r,      condition,     cmd          path
    def __init__(self,name,path,r=0):
        self.name=name
        self.path=path
        # self.center_xy=center_xy
        self.r=r
        # self.condition=condition
        # self.cmd=cmd
    def get_ALLcenterxy(self,condition,n):
        if condition:
            #n 为第几个的位置
            #区域在屏幕上的位置，若有多个[(最左x坐标，最顶y坐标，宽度，高度)，(最左x坐标，最顶y坐标，宽度，高度)]
            self.list=list(pyautogui.locateAllOnScreen(self.path))
            if len(self.list)>=1 and len(self.list)>n:
                #区域中心 在屏幕上的位置
                self.x, self.y =self.list[n][0] + self.list[n][2] / 2,self.list[n][1] +self.list[n][3] / 2
                # 区域的半径
                self.r = [self.list[0][3] / 2 if self.list[0][2] >= self.list[0][3] else self.list[0][2] / 2][0]
                return 1

            # elif len(self.list)>=n:
            #     self.x, self.y = self.list[0][0] + self.list[0][2] / 2, self.list[0][1] + self.list[0][3] / 2
            #     # 区域的半径
            #     self.r = [self.list[0][3] / 2 if self.list[0][2] >= self.list[0][3] else self.list[0][2] / 2][0]
            #     return 1
            elif len(self.list)==0:
                return 0
    def get_centerxy(self,condition,xiangsi=0.9):
        if condition:
            list = dm.FindPic( scereen[1], scereen[2],scereen[3], scereen[4], self.path, "000000", xiangsi, 0)
            if list[1]>=0 and list[2]>=0 and list[0]>=0:
                #区域中心 在屏幕上的位置
                self.x, self.y =list[1],list[2]
                # 区域的半径
                # self.r = 0
                print("发现"+self.name)
                return 1
            else :
                return 0
    @log("正在点击....",1)
    def tap(self,condition):
        if condition:
            if self.get_centerxy(condition):
                ranr = random.randint(1, self.r)
                rantime=random.randint(1,100)
                tap(self.x+ranr,self.y+ranr,delay4=(0.2+rantime/100))
                print("点击%s"%(self.name))
                return 1
            else :
                return 0
                #点击此区域
    def doubletap(self,condition,delay=0.06):
        if condition:
            #双击击此区域
            if self.get_centerxy(condition):
                ranr = random.randint(1, self.r)
                rantime = random.randint(1, 100)
                tap(self.x+ranr,self.y+ranr,clicks=2,delay3=(delay+rantime/100),delay4=0.3)
    def longtap(self,condition,delay=0.1):
        if condition:
            #长按此区域
            if self.get_centerxy(condition):
                swipe(self.x,self.y,self.x,self.y,delay=0.2,delay3=delay)
    def delaytap(self,condition,beforetap=0.1,taping=0.1,aftertap=0.1,):
        if condition:
            #延迟点击此区域   延时区有 1、点击前延时 2、点击后延时  3、点击按的时候延时
            if self.get_centerxy(condition):
                time.sleep(beforetap)
                swipe(self.x, self.y, self.x, self.y, delay=0.2, delay3=taping)
                time.sleep(aftertap)
    def swipe(self,condition,endx,endy,delay=0.5):
        if condition:
            #拖动此区域到哪 1、拖动过程的延时 2、拖动轨迹（到目的地的过程,为实现）
            if self.get_centerxy(condition):
                rantime = random.randint(1, 100)
                swipe(self.x,self.y,endx,endy,delay=0.3,delay3=(delay+rantime/100))

def getScreen():
    pyautogui.screenshot("hello.bmp",region=scereen)

def hunshi():

    tiaozhan=PartOfTheScreen("挑战","tmp/挑战.bmp",20)
    shengli = PartOfTheScreen("胜利", "tmp/胜利.bmp", 50)
    shengli2=PartOfTheScreen("胜利2","tmp/胜利2.bmp",50)
    while True:
        # dm.MoveWindow(hwnd, 10, 10)
        # a=dm.GetWindowRect(hwnd)
        # print(a)
        tiaozhan.tap(1)
        shengli.tap(1)
        shengli2.tap(1)

        # tap(tiaozhan.x,tiaozhan.y,clicks=3,xOffset=20,yOffset=20,delay3=0.2)
        time.sleep(2)
@log("开始副本")
def fuben():
    ##############
    #状态标志设置区
    manji=0

    #############
    ############
    # 设置图片区
    zhaoguai=PartOfTheScreen("找怪中","tmp/找怪中.bmp",10)
    tansuo=PartOfTheScreen("探索","tmp/探索.bmp",40)
    zhang =PartOfTheScreen("二十五章","tmp/二十五章.bmp",10)
    shengli = PartOfTheScreen("胜利", "tmp/胜利.bmp", 50)
    shengli2 = PartOfTheScreen("胜利2", "tmp/胜利2.bmp", 50)
    guai = PartOfTheScreen("小怪", "tmp/小怪.bmp", 5)
    boss = PartOfTheScreen("boss", "tmp/boss.bmp", 5)
    zhunben = PartOfTheScreen("准备", "tmp/准备.bmp", 30)
    zhiren = PartOfTheScreen("纸人", "tmp/纸人.bmp", 5)
    dangtian=PartOfTheScreen("当天不用提醒", "tmp/当天不用提醒.bmp", 3)
    quxiao = PartOfTheScreen("取消", "tmp/取消.bmp", 10)
    kuang= PartOfTheScreen("奖励框", "tmp/奖励框.bmp", 10)
    find_manji=PartOfTheScreen("狗粮满级1","tmp/满级.bmp",5)
    find_manji2 = PartOfTheScreen("狗粮满级2", "tmp/满级2.bmp", 5)
    all = PartOfTheScreen("全部", "tmp/全部.bmp", 5)
    nka= PartOfTheScreen("N卡", "tmp/N.bmp", 5)
    ji = PartOfTheScreen("1级", "tmp/级1.bmp", 5)
    ###############
    while True:
        if find_manji.get_centerxy(1): manji=1
        if find_manji2.tap(1): manji=1
        dangtian.tap(1)
        quxiao.tap(1)
        tansuo.tap(1)
        zhang.tap(1)
        shengli2.tap(1)
        # shengli.tap(1)
        boss.tap(1)
        guai.tap(1)
        zhiren.tap(1)
        kuang.tap(1)
        if zhaoguai.tap(guai.get_centerxy(1) == 0 ):time.sleep(1.5)
        zhunben.tap(manji==0)
        ji.swipe(1,155,316)
        ji.swipe(1, 655, 342)
        nka.tap(manji)
        all.tap(manji)
        # time.sleep(2)

@log("开始读取配置文件")
def readini():
    CMD={}
    while True:
        with open("cmd.txt", "r", encoding="utf-8") as fp:
            lines = [x for x in fp.readlines() if x.split(" ")[0] != "#"]
        fp.close()
        for tmp in lines :
            CMD_list=tmp.split(" ")
            CMD[CMD_list[0]]=PartOfTheScreen(CMD_list[0], "tmp/"+CMD_list[0]+".bmp", int(CMD_list[2]))
            if CMD_list[1]=="点击":
                if CMD_list[3].split(":")[0] == "{始终":
                    CMD[CMD_list[0]].tap(1)
                elif CMD_list[3].split(":")[0]=="{未发现":
                    CMD[CMD_list[0]].tap(CMD[CMD_list[3].split(":")[1].split("}")[0]].get_centerxy(1)==0)
                elif CMD_list[3].split(":")[0]=="{发现":
                    CMD[CMD_list[0]].tap(CMD[CMD_list[3].split(":")[1].split("}")[0]].get_centerxy(1)==1)

                if CMD_list[4].split(":")[0]=="{延时":
                    time.sleep(int(CMD_list[4].split(":")[1].split("}")[0]))
def main():
    # print(scereen)
    fuben()
if __name__== '__main__':
    # pyautogui.alert('开始吧')
    readini()
    # main()
    # dm.SetWindowState(hwnd, 8)
    # dm.SetWindowState(hwnd, 1)
    # dm.MoveWindow(hwnd, 0, 0)
    # print(dm.BindWindow(hwnd, "normal", "dx2", "normal", 0))
    # print(a)
    # main()


def test():

    a=PartOfTheScreen("file","tmp/file.bmp")
    start =time.clock()
    # x,y=pyautogui.locateCenterOnScreen("tmp/file.bmp",grayscale=True)
    # x=dm.FindPic(0, 0, 2000, 2000, "tmp/file.bmp", "000000", 0.9, 0)
    a.get_centerxy(1)
    end =time.clock()
    print("找图花费%sS"%(end-start),a.x,a.y)
    # pyautogui.screenshot("hello.bmp")