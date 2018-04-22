import os




def autoinstall(mod):
    try :
        import mod
    except:
        print("本地未安装%s模块，尝试网络安装"%mod)
        try:
            os.system("pip install -i https://pypi.tuna.tsinghua.edu.cn/simple %s"%mod)
        except:
            print("未从清华源中找到%s模块，正从官方安装"%(mod))
            os.system("pip install %s"%mod)

def init():
    """
    初次运行配置
    :return:
    """
    print("setp 1:尝试加载大漠插件.....")
    try:
        os.system("dm.bat")
        # dm = win32com.client.Dispatch('dm.dmsoft')
    except :
        print("加载模块出错....")
    finally:
        print("\n若加载失败请手动运行dm.bat文件")
    print("setp 2:创建图片资源目录.....")
    try:
        os.mkdir("tmp")
    except FileExistsError as e:
        print("erro :文件已存在")

    print("setp 3:安装一些python模块")
    try:
        import cv2
    except:
        print("请手动安装opencv")

    try:
        import pyautogui
    except:
        print("本地未安装pyautogui模块，尝试网络安装" )
        try:
            os.system("pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyautogui")
        except:
            print("未从清华源中找到pyautogui模块，正从官方安装")
            os.system("pip install %s")

    try:
        import image
    except:
        print("本地未安装image模块，尝试网络安装" )
        try:
            os.system("pip install -i https://pypi.tuna.tsinghua.edu.cn/simple image")
        except:
            print("未从清华源中找到image模块，正从官方安装")
            os.system("pip install image" )

    try:
        import win32com.client
    except:
        print("本地未安装pywin32模块，尝试网络安装" )
        try:
            os.system("pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pywin32")
        except:
            print("未从清华源中找到pywin32模块，正从官方安装")
            os.system("pip install pywin32" )

    try:
        import numpy
    except:
        print("本地未安装numpy模块，尝试网络安装" )
        try:
            os.system("pip install -i https://pypi.tuna.tsinghua.edu.cn/simple numpy")
        except:
            print("未从清华源中找到numpy模块，正从官方安装")
            os.system("pip install numpy" )


    try:
        from matplotlib import pyplot as plt
    except:
        print("本地未安装matplotlib模块，尝试网络安装" )
        try:
            os.system("pip install -i https://pypi.tuna.tsinghua.edu.cn/simple matplotlib")
        except:
            print("未从清华源中找到matplotlib模块，正从官方安装")
            os.system("pip install matplotlib" )


    # autoinstall("image")
    # autoinstall("pywin32")
    #
    # autoinstall("numpy")
    # autoinstall("matplotlib")
    #os.system("pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyautogui")
    #os.system("pip install -i https://pypi.tuna.tsinghua.edu.cn/simple image")

if __name__== "__main__":
    init()