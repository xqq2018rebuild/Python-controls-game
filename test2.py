# -*- coding:utf-8 -*-
import time
import win32gui, win32ui, win32con, win32api
import os
import random
import cv2
import numpy as np


DEBUG = False

def tap(x,y):
    os.system("ld input tap %.1f %.1f"%(x,y))
    # time.sleep(5)
def swipe(x1,y1,x2,y2):
    os.system("ld input swipe %.1f %.1f %.1f %.1f" % (x1, y1,x2,y2))

def show(img):
    ''' 显示一个图片 '''
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def imread(filename):
    '''
    Like cv2.imread
    This function will make sure filename exists
    '''
    im = cv2.imread(filename)
    if im is None:
        raise RuntimeError("file: '%s' not exists" % filename)
    return im

def find_all_template(im_source, im_search, threshold=0.8, maxcnt=0, rgb=False, bgremove=False):
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


def window_capture(filename):
    # hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
    hwnd = win32gui.FindWindow(0,u"雷电模拟器")
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)

def see_to_tap(im_source, im_search,n=0,ranx=50,rany=15):
    """
    找到什么点什么
    :param im_source: 已经使用cv2.imread(filename) 打开过的图片
    :param im_search: 已经打开的位图块
    :param n:  点击在找到的列表中第几个
    :return:
    """
    randx = random.randint(1, ranx)
    randy = random.randint(1, rany)
    L = find_all_template(im_source, im_search)
    if len(L) >= 1:
        tap(L[n]["result"][0] + randx-16, L[n]["result"][1] + randy-35)
        print("find something...")
        return 1

    # for mubiao in L:
    #     left_p = mubiao["rectangle"][1]
    #     right_p = mubiao["rectangle"][2]
    #     im_source = cv2.rectangle(im_source,left_p,right_p,(0,255,0),3)
    # show(imsrc)
    return 0
def hunshi():
    times=0
    imtiaozhan = imread('tmp/tiaozhan.png')
    imshengli2 = imread('tmp/shengli2.png')
    imjieshou= imread('tmp/jieshou.png')

    while True:
        try:
            beg = int(time.time())
            for x in range(10):
                window_capture("tmp/tmp/now%s.png"%(beg))
            # end = time.time()
            # print("截图时间：",end - beg)
        except:
            time.sleep(100)
            print("卡到截图的地方")
            for x in range(10):
                window_capture("tmp/tmp/now%s.png"%(beg))

        imnow = imread("tmp/tmp/now%s.png"%(beg))
        # 点击挑战
        if see_to_tap(imnow,imtiaozhan):
            times += 1
            print("目前第%s次挑战" % (times))
        # 点击胜利
        see_to_tap(imnow,imshengli2)
        see_to_tap(imnow,imjieshou)
        if times%20==0 :
            print("休息中。。。。")
            time.sleep(200)


        time.sleep(5)
        os.remove("tmp/tmp/now%s.png"%(beg))
def fuben():
    times = 0
    imtansuo = imread('tmp/tansuo.png')
    imshengli2 = imread('tmp/shengli2.png')
    # imfuben = imread('tmp/fuben.png')
    imfuben2 = imread('tmp/fuben2.png')#闪光副本
    imboss = imread('tmp/boss.png')
    imzhiren = imread('tmp/zhiren.png')
    imjiangli = imread('tmp/getjiangli.png')
    imzhang25 = imread('tmp/zhang25.png')
    imbaoxiang = imread('tmp/baoxiang.png')
    immanji= imread('tmp/manji.png')
    # imunlock = imread('tmp/unlock.png') #解锁阵容

    fitting = 0 #没有在战斗
    while True:
        # beg = time.time()
        for x in range(10):
            window_capture("tmp/now.png")
        # end = time.time()
        # print("截图时间：",end - beg)

        imnow = imread("tmp/now.png")

        if see_to_tap(imnow, imboss):
            fitting=1
        f=see_to_tap(imnow, imfuben2, ranx=1, rany=1)

        # see_to_tap(imnow, imfuben, ranx=1, rany=1)
        if see_to_tap(imnow, imzhang25):
            fitting=1
        if see_to_tap(imnow, imtansuo):
            fitting=0

        if see_to_tap(imnow, imshengli2):
            fitting=0
        if see_to_tap(imnow,imbaoxiang,ranx=1,rany=1):
            fitting=1
        if see_to_tap(imnow,imzhiren):
            fitting=1
        if see_to_tap(imnow,imjiangli,ranx=600,rany=430):
            fitting=1
        if f:
            fitting=1

        # if see_to_tap(imnow,immanji):
        #     return 0
        elif f==0 and fitting==0:
            swipe(1035,350, 545 ,380)
            print("move srcean")

        time.sleep(2)
def main():
    hunshi()
    # fuben()
    # for x in range(10):
    #     window_capture("tmp/now.png")
if __name__ == '__main__':
    main()



