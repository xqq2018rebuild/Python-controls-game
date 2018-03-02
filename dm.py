# -*- coding:utf-8 -*-
"""
1.注册大漠插件
2.安装python和模块
    opencv pywin32 matplotlib
3.脚本和dmtmp文件夹放到雷电模拟器安装目录下
4.在游戏的探索界面开启

"""
import win32com.client
import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
import time
import random

DEBUG = False
redfont="\033[1;31m"
fontend="\033[0m"


dm = win32com.client.Dispatch('dm.dmsoft')
hwnd = dm.FindWindow("LDPlayerMainFrame", "雷电模拟器")
b = dm.BindWindow(hwnd,"dx2","normal","normal",0)

# 雷电坐标230,69 图片坐标：219,102
def tap(x,y):
    """
    雷电模拟器点击屏幕
    :param x:
    :param y:
    :return:
    """
    os.system("ld input tap %.1f %.1f"%(x,y))
    if DEBUG:
        print("点击：",x,y)
def swipe(x1, y1, x2, y2,ms=200):
    """
    雷电模拟器滑动屏幕
    :param x1: 起始点x轴
    :param y1: 起始点y轴
    :param x2: 结束点x轴
    :param y2: 结束点y轴
    :return:
    """
    os.system("ld input swipe %.1f %.1f %.1f %.1f %s" % (x1, y1, x2, y2,ms))
    if DEBUG:
        print("从%s,%s滑动到%s,%s"%(x1, y1, x2, y2))
def Capture():

    a, x1, y1, x2, y2 = dm.GetClientRect(hwnd)

    # print( x1, y1, x2, y2)
    # 笔记本屏幕缩放125% 所以坐标乘以1.25
    # x1, y1, x2, y2 = int(x1 * 1.25), int(y1 * 1.25), int(x2 * 1.25), int(y2 * 1.25)

    dm.Capture(x1, y1, x2, y2, "dmtmp/tmp.bmp")

def imread(filename):
    '''
    Like cv2.imread
    This function will make sure filename exists
    '''
    im = cv2.imread(filename)
    if im is None:
        raise RuntimeError("file: '%s' not exists" % filename)
    return im
def show(img):
    ''' 显示一个图片 '''
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def find_all_template(im_source, im_search, threshold=0.95, maxcnt=0, rgb=False, bgremove=False):
    '''
    Locate image position with cv2.templateFind

    Use pixel match to find pictures.

    Args:
        im_source(string): 图像、素材
        im_search(string): 需要查找的图片
        threshold: 阈值，当相识度小于该阈值的时候，就忽略掉

    Returns:
        A tuple of found [(point, score), ...]

    Raises:
        IOError: when file read error
    '''
    # method = cv2.TM_CCORR_NORMED
    # method = cv2.TM_SQDIFF_NORMED
    method = cv2.TM_CCOEFF_NORMED

    if rgb:
        s_bgr = cv2.split(im_search)  # Blue Green Red
        i_bgr = cv2.split(im_source)
        weight = (0.3, 0.3, 0.4)
        resbgr = [0, 0, 0]
        for i in range(3):  # bgr
            resbgr[i] = cv2.matchTemplate(i_bgr[i], s_bgr[i], method)
        res = resbgr[0] * weight[0] + resbgr[1] * weight[1] + resbgr[2] * weight[2]
    else:
        s_gray = cv2.cvtColor(im_search, cv2.COLOR_BGR2GRAY)
        i_gray = cv2.cvtColor(im_source, cv2.COLOR_BGR2GRAY)
        # 边界提取(来实现背景去除的功能)
        if bgremove:
            s_gray = cv2.Canny(s_gray, 100, 200)
            i_gray = cv2.Canny(i_gray, 100, 200)

        res = cv2.matchTemplate(i_gray, s_gray, method)
    w, h = im_search.shape[1], im_search.shape[0]

    result = []
    while True:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        if DEBUG:
            print('templmatch_value(thresh:%.1f) = %.3f' % (threshold, max_val))  # not show debug
        if max_val < threshold:
            break
        # calculator middle point
        middle_point = (top_left[0] + w / 2, top_left[1] + h / 2)
        result.append(dict(
            result=middle_point,
            rectangle=(top_left, (top_left[0], top_left[1] + h), (top_left[0] + w, top_left[1]),
                       (top_left[0] + w, top_left[1] + h)),
            confidence=max_val
        ))
        if maxcnt and len(result) >= maxcnt:
            break
        # floodfill the already found area
        cv2.floodFill(res, None, max_loc, (-1000,), max_val - threshold + 0.1, 1, flags=cv2.FLOODFILL_FIXED_RANGE)
    return result


def see_to_tap2(search,n=0,ranx=50,rany=15):
    """
        找到什么点什么
        :param im_source: 已经使用cv2.imread(filename) 打开过的图片
        :param im_search: 已经打开的位图块
        :param n:  点击在找到的列表中第几个
        :return:
        """
    im_source = imread("dmtmp/tmp.bmp")
    im_search = imread(search)
    randx = random.randint(1, ranx)
    randy = random.randint(1, rany)
    L = find_all_template(im_source, im_search)
    if len(L) >= 1:
        tap(L[n]["result"][0] + randx, L[n]["result"][1] + randy - 35)
        print("find %s"%(search))
        return 1

    # for mubiao in L:
    #     left_p = mubiao["rectangle"][1]
    #     right_p = mubiao["rectangle"][2]
    #     im_source = cv2.rectangle(im_source,left_p,right_p,(0,255,0),3)
    # show(imsrc)
    return 0

def see_to_swipe(search,n=0,ranx=50,rany=15):

    im_source = imread("dmtmp/tmp.bmp")
    im_search = imread(search)
    randx = random.randint(1, ranx)
    randy = random.randint(1, rany)
    L = find_all_template(im_source, im_search)
    if len(L) >= 1:
        swipe(L[n]["result"][0] + randx, L[n]["result"][1] + randy - 35,L[n]["result"][0] + randx+20,L[n]["result"][1] + randy - 35+30,1000)
        print("find %s" % (search))
        return 1
    return 0

def see_to_longtap(search,n=0,ranx=50,rany=15):

    im_source = imread("dmtmp/tmp.bmp")
    im_search = imread(search)
    randx = random.randint(1, ranx)
    randy = random.randint(1, rany)
    L = find_all_template(im_source, im_search)
    if len(L) >= 1:
        swipe(L[n]["result"][0] + randx, L[n]["result"][1] + randy - 35,L[n]["result"][0] + randx, L[n]["result"][1] + randy - 35,1500)
        print("find %s" % (search))
        return 1
    return 0
def see_to_doubletap(search,n=0,ranx=50,rany=15):
    """
        找到什么点什么
        :param im_source: 已经使用cv2.imread(filename) 打开过的图片
        :param im_search: 已经打开的位图块
        :param n:  点击在找到的列表中第几个
        :return:
        """
    im_source = imread("dmtmp/tmp.bmp")
    im_search = imread(search)
    randx = random.randint(1, ranx)
    randy = random.randint(1, rany)
    L = find_all_template(im_source, im_search)
    if len(L) >= 1:

        tap(L[n]["result"][0] + randx, L[n]["result"][1] + randy - 35)
        time.sleep(0.5)
        tap(L[n]["result"][0] + randx, L[n]["result"][1] + randy - 35)
        print("find %s" % (search))
        return 1

    # for mubiao in L:
    #     left_p = mubiao["rectangle"][1]
    #     right_p = mubiao["rectangle"][2]
    #     im_source = cv2.rectangle(im_source,left_p,right_p,(0,255,0),3)
    # show(imsrc)
    return 0


def see_to_delaytap(search, n=0, ranx=50, rany=15):
    """
        找到什么点什么
        :param im_source: 已经使用cv2.imread(filename) 打开过的图片
        :param im_search: 已经打开的位图块
        :param n:  点击在找到的列表中第几个
        :return:
        """
    im_source = imread("dmtmp/tmp.bmp")
    im_search = imread(search)
    randx = random.randint(1, ranx)
    randy = random.randint(1, rany)
    L = find_all_template(im_source, im_search)
    if len(L) >= 1:
        time.sleep(0.8)
        tap(L[n]["result"][0] + randx, L[n]["result"][1] + randy - 35)
        print("find %s" % (search))
        time.sleep(1.5)
        return 1

    # for mubiao in L:
    #     left_p = mubiao["rectangle"][1]
    #     right_p = mubiao["rectangle"][2]
    #     im_source = cv2.rectangle(im_source,left_p,right_p,(0,255,0),3)
    # show(imsrc)
    return 0


def find_pic(search,n=0,ranx=50,rany=15):

    im_source = imread("dmtmp/tmp.bmp")
    im_search = imread(search)
    randx = random.randint(1, ranx)
    randy = random.randint(1, rany)
    L = find_all_template(im_source, im_search)
    if len(L) >= 1:
        return 1
    return 0


def fuben(zhang):

    nowstatus = 0
    nextstatus = 1
    swiplock = 1
    swiptimes=0
    boss = 0

    #换狗粮标志位
    manji=0
    tapf=0
    huan =0
    while 1:
        x = random.randint(1,100)
        y = random.randint(1,100)
        Capture()
        if nowstatus == 0:
            see_to_tap2("dmtmp/baoxiang.bmp", n=0, ranx=1, rany=1)
            see_to_tap2("dmtmp/shengli.bmp", n=0, ranx=50, rany=50)
            if see_to_doubletap(zhang, n=0, ranx=20, rany=30):
                nowstatus = nextstatus
                nextstatus = 2
            see_to_tap2("dmtmp/zhiren.bmp", n=0, ranx=10, rany=10)
            # see_to_tap2("dmtmp/tansuodenglou.bmp", n=0, ranx=2, rany=3)

            see_to_tap2("dmtmp/jieshou.bmp", n=0, ranx=2, rany=4)
            see_to_tap2("dmtmp/waikuang.bmp", n=0, ranx=20, rany=10)

        elif nowstatus == 1:

            if see_to_tap2("dmtmp/tansuo.bmp", n=0, ranx=2, rany=5):
                nowstatus = nextstatus
                nextstatus = 0
                swiplock = 0
                swiptimes = 0
            see_to_tap2("dmtmp/jieshou.bmp", n=0, ranx=2, rany=4)
        elif nowstatus == 2:
            if see_to_tap2("dmtmp/boss.bmp", n=0, ranx=2, rany=3):
                swiplock = 1
                boss = 1
                swiptimes = 0
            fguai= see_to_tap2("dmtmp/guai.bmp", n=0, ranx=1, rany=1)
            if fguai:
                swiplock =1

            elif fguai == 0 and swiplock == 0 :
                if swiptimes<=15:
                    swipe(1055+x, 468-y, 690+y, 434+x)
                    time.sleep(0.5)
                elif 15<swiptimes and swiptimes<=30:
                    swipe(690 + y, 434 + x,1055 + x, 468 - y)
                    time.sleep(0.5)
                elif swiptimes>30:
                    swiptimes=0
                swiptimes += 1
            else:
                swiplock = 1

            see_to_tap2("dmtmp/jieshou.bmp", n=0, ranx=2, rany=4)
            if find_pic("dmtmp/zhunbei.bmp", n=0, ranx=50, rany=40):
                if manji ==0 :
                    see_to_tap2("dmtmp/zhunbei.bmp", n=0, ranx=50, rany=40)
                    tapf = 0
                    huan=0
                elif manji ==1:
                    if tapf == 0 and see_to_doubletap("dmtmp/qingming.bmp", n=0, ranx=3, rany=4):
                        tapf=1
                    if tapf==1 and see_to_tap2("dmtmp/all.bmp", n=0, ranx=4, rany=3):
                        tapf=2
                    if tapf ==2 and see_to_tap2("dmtmp/Nka.bmp", n=0, ranx=2, rany=4):
                        tapf=3
                    if huan ==0 and tapf==3:
                        swipe(598,580,173,322,1000)
                        time.sleep(3)
                        swipe(733,583,626,234,500)
                        huan=1
                        manji=0
            if find_pic("dmtmp/manji.bmp", n=0, ranx=1, rany=1):
                manji=1
                print(redfont+"发现满级"+fontend)
            if find_pic("dmtmp/manji2.bmp", n=0, ranx=1, rany=1):
                manji=1
                print(redfont+"发现满级"+fontend)
            if find_pic("dmtmp/manji1.bmp", n=0, ranx=1, rany=1):
                manji=1
                print(redfont+"发现满级"+fontend)
            see_to_tap2("dmtmp/shengli1.bmp", n=0, ranx=50, rany=50)
            if see_to_delaytap("dmtmp/shengli.bmp", n=0, ranx=50, rany=50):

                if boss:
                    nowstatus = nextstatus
                    nextstatus = 1
                    boss = 0

                # see_to_tap2("dmtmp/shengli.bmp", n=0, ranx=1, rany=1)
                swiplock = 0



def hunshi():
    times=0
    while 1:
        Capture()
        if see_to_tap2("dmtmp/tiaozhan.bmp", n=0, ranx=5, rany=10):
            times += 1
            print("第" + redfont, times//2, fontend + "挑战")
        see_to_tap2("dmtmp/shengli1.bmp", n=0, ranx=70, rany=50)
        see_to_tap2("dmtmp/shengli.bmp", n=0, ranx=50, rany=40)
        see_to_tap2("dmtmp/jieshou.bmp", n=0, ranx=2, rany=4)
def jiejie():
    times=0
    nowstatus=0
    nextstatus=1
    while 1:
        Capture()
        if nowstatus==0:
            see_to_delaytap("dmtmp/shengli.bmp", n=0, ranx=10, rany=20)
            while times >= 3:
                Capture()
                if see_to_tap2("dmtmp/jiejie/queding.bmp", n=0, ranx=4, rany=10):
                    times=0
                see_to_tap2("dmtmp/jiejie/shuaxin.bmp", n=0, ranx=4, rany=10)


            if see_to_tap2("dmtmp/jiejie/xunzhangling.bmp",n=0,ranx=4,rany=10):
                nowstatus=nextstatus
                nextstatus=2
            elif see_to_tap2("dmtmp/jiejie/xunzhangyi.bmp", n=0, ranx=4, rany=10):
                nowstatus = nextstatus
                nextstatus = 2

            elif see_to_tap2("dmtmp/jiejie/xunzhanger.bmp", n=0, ranx=4, rany=10):
                nowstatus = nextstatus
                nextstatus = 2

            elif see_to_tap2("dmtmp/jiejie/xunzhangsan.bmp", n=0, ranx=4, rany=10):
                nowstatus = nextstatus
                nextstatus = 2

            elif see_to_tap2("dmtmp/jiejie/xunzhangwu.bmp", n=0, ranx=4, rany=10):
                nowstatus = nextstatus
                nextstatus = 2


        if nowstatus ==1 :
            if see_to_tap2("dmtmp/jiejie/jingong.bmp", n=0, ranx=4, rany=10):
                nowstatus=nextstatus
                nextstatus=0

        if nowstatus==2:
            see_to_delaytap("dmtmp/shengli1.bmp", n=0, ranx=10, rany=20)
            if see_to_delaytap("dmtmp/jiejie/shibai.bmp", n=0, ranx=10, rany=20):
                nowstatus = nextstatus
                nextstatus = 1
            if see_to_delaytap("dmtmp/shengli.bmp",n=0,ranx=10,rany=20):
                times += 1
                nowstatus=nextstatus
                nextstatus=1

def main():
    fuben("dmtmp/ershierzhang.bmp")
    # hunshi()
if __name__ == '__main__':
    main()
# def test():
#     hwnd = dm.FindWindow("LDPlayerMainFrame", "雷电模拟器")
#     a, x1, y1, x2, y2 = dm.GetClientRect(hwnd)
#
#     # 笔记本屏幕缩放125% 所以坐标乘以1.25
#     x1, y1, x2, y2 = int(x1 * 1.25), int(y1 * 1.25), int(x2 * 1.25), int(y2 * 1.25)
#     # b = dm.FindColor(x1, y1, x2, y2, "F27385-000000", 0.9, 0)
#     b = dm.FindPic(x1, y1, x2, y2, "dmtmp/zhang.bmp", "000000", 0.9, 0)
#     bx, by = b[1] - x1, b[2] - y1
#
#     print("屏幕坐标：", x1, y1, x2, y2)
#     print("找到点的在图片上坐标:", b, bx, by)
#
#     dm.Capture(x1, y1, x2, y2, "aaa.bmp")
#
#     # b = dm.FindPic(x1, y1, x2, y2,"a.png", "000000",0.5, 0)
#     # b1,b2=int(b[1]/1.25-x1),int(b[2]/1.25-y1)
#
#     img = cv2.imread("aaa.bmp")
#     cv2.circle(img, (bx, by), 10, (0, 0, 255), 1)
#     cv2.line(img, (bx - 30, by), (bx + 30, by), (0, 0, 255), 1)
#     cv2.line(img, (bx, by - 30), (bx, by + 30), (0, 0, 255), 1)
#     cv2.imshow('image', img)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
# def see_to_tap(bmp):
#     hwnd = dm.FindWindow("LDPlayerMainFrame", "雷电模拟器")
#     GetHwnd, x1, y1, x2, y2 = dm.GetClientRect(hwnd)
#     # 笔记本屏幕缩放125% 所以坐标乘以1.25
#     if GetHwnd:
#         x1, y1, x2, y2 = int(x1 * 1.25), int(y1 * 1.25), int(x2 * 1.25), int(y2 * 1.25)
#         fp = dm.FindPic(x1, y1, x2, y2, bmp, "000000", 0.95, 0)
#         if fp[0] >= 0:
#             tux, tuy = fp[1] - x1, fp[2] - y1
#             ldx, ldy = tux, tuy-33
#             tap(ldx, ldy)
#             return 1
#         else:
#             print(redfont + "未找到%s图片!"%(bmp) + fontend)
#             return 0
#         if DEBUG:
#             print("屏幕坐标：", x1, y1, x2, y2)
#             print("找图片返回值", fp)
#     else:
#         print(redfont + "未获得雷电模拟器句柄！" + fontend)
#         return 0
# def find_photo(bmp):
#     hwnd = dm.FindWindow("LDPlayerMainFrame", "雷电模拟器")
#     GetHwnd, x1, y1, x2, y2 = dm.GetClientRect(hwnd)
#     # 笔记本屏幕缩放125% 所以坐标乘以1.25
#     if GetHwnd:
#         x1, y1, x2, y2 = int(x1 * 1.25), int(y1 * 1.25), int(x2 * 1.25), int(y2 * 1.25)
#         fp = dm.FindPic(x1, y1, x2, y2, bmp, "000000", 0.9, 0)
#         if fp[0] >= 0:
#             tux, tuy = fp[1] - x1, fp[2] - y1
#             ldx, ldy = tux + 5, tuy - 33 + 5
#             return fp[0],ldx,ldy
#         else:
#             print(redfont + "未找到%s图片!" % (bmp) + fontend)
#             return -1,-1,-1
#         if DEBUG:
#             print("屏幕坐标：", x1, y1, x2, y2)
#             print("找图片返回值", fp)
#     else:
#         print(redfont + "未获得雷电模拟器句柄！" + fontend)
#         return -1,-1,-1
#
#
# def main_test1():
# ############################################################
# #       开始      探索      找怪      找奖励
# #
# #
# #
# #
#     nowstatus=0
#     nextstatus=1
#     swiplock=1
#     boss = 0
#     while 1:
#         if nowstatus == 0:
#             if see_to_tap("dmtmp/zhang.bmp"):
#                 nowstatus=nextstatus
#                 nextstatus=2
#             see_to_tap("dmtmp/zhiren.bmp|dmtmp/baoxiang.bmp|dmtmp/shengli.bmp|dmtmp/waikuang.bmp")
#
#             # see_to_tap("dmtmp/baoxiang.bmp")
#             #
#             # see_to_tap("dmtmp/shengli.bmp")
#             #
#             # see_to_tap("dmtmp/waikuang.bmp")
#
#         elif nowstatus==1:
#             if see_to_tap("dmtmp/tansuo.bmp"):
#                 nowstatus = nextstatus
#                 nextstatus =0
#                 swiplock=0
#         elif nowstatus==2:
#             if see_to_tap("dmtmp/boss.bmp"):
#                 swiplock=1
#                 boss=1
#             elif see_to_tap("dmtmp/guai.bmp") == 0 and swiplock == 0 :
#                 swipe(1055,468,890,434)
#             else:
#                 swiplock=1
#             # elif see_to_tap("dmtmp/zhunbei.bmp") and huangouliang :
#             #     huangouliang()
#             s, x, y = find_photo("dmtmp/manji.bmp")
#             if s == 0:
#                 pass
#                 # huangouliang
#             see_to_tap("dmtmp/shengli1.bmp")
#             if see_to_tap("dmtmp/shengli.bmp"):
#
#                 if boss:
#                     nowstatus = nextstatus
#                     nextstatus = 1
#                     boss=0
#                 swiplock=0
