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
import win32com.client
import numpy as np
from matplotlib import pyplot as plt

dm = win32com.client.Dispatch('dm.dmsoft')
#如果失控了，需要中断PyAutoGUI函数，就把鼠标光标在屏幕左上角。
pyautogui.FAILSAFE = True
#可以为所有的PyAutoGUI函数增加延迟。默认延迟时间是0.1秒。在函数循环执行的时候，这样做可以让PyAutoGUI运行的慢一点，非常有用。
pyautogui.PAUSE = 0.1

def tap(x,y,clicks=1,button="left",delay=0.3,xOffset=0,yOffset=0,delay2=0,delay3=0.03,delay4=1.0,click_type=2):
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
        pyautogui.click(x,y,clicks=clicks,interval=delay3,duration=delay4,button=button,tween=pyautogui.easeInQuad)
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
    def __init__(self,name,path,r):
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
            list = dm.FindPic(0, 0, 2000, 2000, self.path, "000000", xiangsi, 0)
            if list[1]>=0 and list[2]>=0 and list[0]>=0:
                #区域中心 在屏幕上的位置
                self.x, self.y =list[1],list[2]
                # 区域的半径
                # self.r = 0
                return 1
            else :
                return 0
    def tap(self,condition):
        if condition:
            if self.get_centerxy(condition):
                ranr = random.randint(1, self.r)
                rantime=random.randint(1,100)
                tap(self.x,self.y,xOffset=ranr,yOffset=ranr,delay4=(0.2+rantime/100))
                #点击此区域
    def doubletap(self,condition,delay=0.06):
        if condition:
            #双击击此区域
            if self.get_centerxy(condition):
                ranr = random.randint(1, self.r)
                rantime = random.randint(1, 100)
                tap(self.x,self.y,xOffset=ranr,yOffset=ranr,clicks=2,delay3=(delay+rantime/100),delay4=0.3)
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
    pyautogui.screenshot("hello.bmp",region=())

def main():
    yuhun=PartOfTheScreen("御魂","tmp/御魂.bmp",5)
    dashe=PartOfTheScreen("大蛇","tmp/蛇.bmp",10)
    tiaozhan=PartOfTheScreen("挑战","tmp/挑战.bmp",5)
    qi=PartOfTheScreen("qi","tmp/7.bmp",3)
    while True:
        # tap(149,533)
        # yuhun.swipe(1,149,522)
        # yuhun.doubletap(1)
        # if wenjian.get_centerxy(1):
        #     tap(wenjian.x,wenjian.y,clicks=1,delay4=0.4)
        qi.tap(1)
        print(qi.x,qi.y)
        # print(yuhun.x, yuhun.y)
        # dashe.doubletap(1)
        # tiaozhan.doubletap(1)
        time.sleep(2)
if __name__== '__main__':
    main()


def test():

    a=PartOfTheScreen("file","tmp/file.bmp")
    start =time.clock()
    # x,y=pyautogui.locateCenterOnScreen("tmp/file.bmp",grayscale=True)
    # x=dm.FindPic(0, 0, 2000, 2000, "tmp/file.bmp", "000000", 0.9, 0)
    a.get_centerxy(1)
    end =time.clock()
    print("找图花费%sS"%(end-start),a.x,a.y)
    # pyautogui.screenshot("hello.bmp")