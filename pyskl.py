#coding=utf-8
# @Time    : 2018-01-18 15:34
# @Useage  : pyskl
# @Author  : crazylaser
# @File    : pyskl.py
# @Software: PyCharm
import imutils,cv2,time,numpy as np
from PIL import ImageGrab
from pymouse import PyMouse
from pykeyboard import PyKeyboard
m = PyMouse()
k = PyKeyboard()
x_dim, y_dim = m.screen_size()

"""跨平台PyUserInput"""
"""
pyautogui 中文文档
https://muxuezi.github.io/posts/doc-pyautogui.html"""

# 坐标类
class Location(object):
    def __init__(self,x,y):
        self.x = int(x)
        self.y = int(y)
    def __repr__(self):
        return  str(self.x)+","+str(self.y)

# 区域类
class Region(object):
    def __init__(self,topleftx=0,toplefty=0,w=x_dim,h=y_dim):
        self.topleftx = int(topleftx)
        self.toplefty = int(toplefty)
        self.topleft = Location(int(topleftx),int(toplefty))
        self.w = int(w)
        self.h = int(h)
        self.center = Location(int(topleftx+w/2),int(toplefty+h/2))
    def __repr__(self):
        return  "("+str(self.topleftx)+","+str(self.toplefty)+","+str(self.w)+","+str(self.h)+")"

# 自定义类 region类的拓展
class pyskl(object):
    def __init__(self,topleftx=0,toplefty=0,w=x_dim,h=y_dim):
        self.topleftx = topleftx
        self.toplefty = toplefty
        self.topleft = Location(topleftx,toplefty)
        self.w = w
        self.h = h
        self.center = Location(topleftx+w/2,toplefty+h/2)
        self.region = Region(topleftx,toplefty,w,h)
        #print u"区域参数",self.region
    def findTopLeft(self,imgname,value=0.8):
        imgname = imgname + ".png"
        list1 = findLocal(jietu(self.region),cv2.imread(imgname),value)
        return list1[0]
    def findCenter(self,imgname,value=0.8):
        imgname = imgname + ".png"
        list1 = findLocal(jietu(self.region),cv2.imread(imgname),value)
        return list1[0]
    # 本地读取图像比较
    def findLocal(image, imgname, value):
        Target = imgname + ".png"
        img_rgb = cv2.imread(image)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(Target, 0)
        # w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = value
        loc = np.where(res >= threshold)
        list1 = []
        for pt in zip(*loc[::-1]):
            # print pt[0], pt[1]
            list1.append(Location(pt[0], pt[1]))
            # 图片           两个对角点坐标             颜色     线宽
        #     cv2.rectangle(img_gray, pt, (pt[0] + w, pt[1] + h), (7, 249, 151), 2)
        # cv2.imshow('Detected', img_gray)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    # 存在一张图片 屏幕读取
    def exsit(self,imgname,value=0.9):
        Target = imgname + ".png"
        image = self.jietu()
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(Target, 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = value
        loc = np.where(res >= threshold)
        list1 = []
        return len(loc[0])>0
    def exsitNum(self,imgname,value=0.9):
        Target = imgname + ".png"
        image = self.jietu()
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(Target, 0)
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = value
        loc = np.where(res >= threshold)
        list1 = []
        return len(loc[0])
    # 存在图片列表 屏幕读取 布尔
    def exsitImgList(self,imgnamelist,value=0.9):
        image = self.jietu()
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        for i in imgnamelist:
            Target = i + ".png"
            #delflag
            # print Target
            template = cv2.imread(Target, 0)
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = value
            loc = np.where(res >= threshold)
            if len(loc[0]) > 0:
                return True
            # del falg
            # else:
            #     print u"不存在exsitImgList"
        return False
    # 判断列表中存在图片的名字
    def exsitWhichImg(self,imgnamelist,value=0.9):
        image = self.jietu()
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        for i in imgnamelist:
            Target = i + ".png"
            template = cv2.imread(Target, 0)
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = value
            loc = np.where(res >= threshold)
            if len(loc[0]) > 0:
                return i
        return u"notexsitname"
    # 手动传入图片判断存在
    def exsitduibi(image,Target,value):
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(Target, 0)
        # w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = value
        loc = np.where(res >= threshold)
        # list1 = []
        return len(loc[0])>0

    def cameraexsit(image,Target,v):
        res = cv2.matchTemplate(image, Target, cv2.TM_CCOEFF_NORMED)
        threshold = value
        loc = np.where(res >= threshold)
        return len(loc[0])>0

    # 内存图像比较 查找并返回图片中心
    def find(self, imgname, value=0.9):
        Target = imgname+".png"
        image = self.jietu()
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(Target, 0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = value
        loc = np.where(res >= threshold)
        # print loc
        list1 = []
        if len(loc[0])>0:
            for pt in zip(*loc[::-1]):
                # print pt[0], pt[1]
                list1.append(Region(pt[0], pt[1],w,h))
            return list1
        else:
            pass
            # print u"没有匹配图片"
            # 图片           两个对角点坐标             颜色     线宽
        #     cv2.rectangle(img_gray, pt, (pt[0] + w, pt[1] + h), (7, 249, 151), 2)
        # cv2.imshow('Detected', img_gray)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


    # 对区域进行截图 pyqutogui反应迟钝
    # import pyautogui
    # def jietu_pyautogui(region = rscreen):
    #     img1 = pyautogui.screenshot()
    #     img1 = cv2.cvtColor(np.array(img1), cv2.COLOR_RGB2BGR)
    #     print u"对区域",region,u"进行截图"
    #     img2 = img1[region.toplefty:region.h, region.topleftx:region.w]
    #     return img2

    # 对区域进行截图 pil
    def jietu(self):
        region = self.region
        bbox = (region.topleftx, region.toplefty,region.topleftx+region.w, region.toplefty+region.h)
        img1 = ImageGrab.grab(bbox)
        img1 = cv2.cvtColor(np.array(img1), cv2.COLOR_RGB2BGR)
        # print u"对区域",region,u"进行截图"
        return img1

    def clickimg(self,imgname,value=0.9):
        list1 = self.find(imgname,value)
        # print list1[0]
        self.movezero(list1[0].center)
        self.click()
    def dblclickimg(self,imgname):
        list1 = self.find(imgname)
        # print list1[0]
        self.movezero(list1[0].center)
        self.dblclick()
    def rclickimg(self,imgname):
        list1 = self.find(imgname)
        # print list1[0]
        self.movezero(list1[0].center)
        self.rclick()

    def click(self):
        x0, y0 = m.position()
        m.click(x0,y0)
    # 绝对定位
    def movexy(self,x,y):
        # windll.user32.SetCursorPos(x, y)
        m.move(x,y)
    # 相对鼠标当前指针定位
    def movedev(self,x,y):
        x0,y0 = m.position()
        self.movexy(x+x0, y+y0)
    # 相对零点定位
    def movezero(self,location):
        x0 = self.topleftx
        y0 = self.toplefty
        x = location.x
        y = location.y
        self.movexy(x+x0, y+y0)
    # 绝对移动
    def move(self,location):
        self.movexy(location.x,location.y)
    def dblclick(self):
        x0, y0 = m.position()
        m.click(x0,y0,1,2)
    def rclick(self):
        x0, y0 = m.position()
        m.click(x0, y0, 2, 1)
    def wheel(i):
        m.scroll(-i)
    def press(self,keyname):
        k.press_key(keyname)
    def release(self,keyname):
        k.release_key(keyname)
    def tap(self,keyname):
        k.tap_key(keyname)
    # 连续按键
    def tapmore(self,keyname,times=2,yanshi=5):
        k.tap_key(keyname, times, yanshi)
    def type(str1):
        k.type_string(str1)
    def zuhe(self,keyname1,keyname2):
        k.press_keys([keyname1,keyname2])
    # p1.zuhe(k.windows_l_key,'d')
    # F1~12
    # 小键盘
    def pause(self,sleeptime):
        time.sleep(sleeptime)
    def wait(self,imgname,waittime=10):
        for i in range(waittime):
            if self.exsit(imgname):
                print u"图片出现了"
                return True
            self.pause(1)
        print imgname,u"不存在"
        return False
    # 实现函数的重载
    def waitandclick(self,imgnamewait,imgnameclick = 1,waittime=10):
        # 只输入一个参数 即存在图片a点击图片a 默认走第一个方法
        if isinstance(imgnamewait, str) and isinstance(imgnameclick, int):
            for i in range(waittime):
                if self.exsit(imgnamewait):
                   self.clickimg(imgnamewait)
                   return
                self.pause(0.3)
            print u"图片",imgnamewait,u"不存在"
        # 输入两个参数 存在图片a点击图片b
        if isinstance(imgnamewait, str) and isinstance(imgnameclick, str):
            for i in range(waittime):
                if self.exsit(imgnamewait):
                   self.clickimg(imgnameclick)
                   return
                self.pause(0.3)
            print u"图片"+imgnamewait,u"不存在"
        # 异常点击图片
    def waitclick(self,imgnamewait,waittime=0.05):
        while 1:
            try :
                self.clickimg(imgnamewait)
                print u"点击了 "+imgnamewait
                break
            except Exception:
                self.pause(waittime)
                continue
    def waitVanish(self,imgname,waittime=3600):
        for i in range(waittime):
            if not self.exsit(imgname):
                print u"图片消失了"
                return True
            self.pause(1)
        return False
    def waitImgList(self,imglist,waittime=3600):
        for i in range(waittime):
            if self.exsitImgList(imglist):
                return True
            self.pause(1)
        print imglist,u"不存在"
        return False
    def waitWhichImgList(self,imglist,waittime=3600):
        for i in range(waittime):
            exsitname = "notexsitname"
            exsitname = self.exsitWhichImg(imglist)
            if exsitname != "notexsitname":
                return exsitname
            self.pause(1)
        return exsitname
    def waitImgListVanish(self,imglist,waittime=3600):
        for i in range(waittime):
            if not self.exsitImgList(imglist):
                return True
            self.pause(1)
        return False
    def clicklocation(self,x,y):
        self.movezero(Location(x,y))
        self.click()
if __name__ == '__main__':
    # rscreen = Region()
    # print rscreen.center
    # print rscreen.topleft
    # print "width =", GetSystemMetrics (0)
    # print "hight =", GetSystemMetrics (1)
    #
    # r1 = pyskl(341,191,400,400).region
    # print r1
    # img2 = jietu(r1)
    # cv2.imshow("Screenshot", img2)
    #
    # for i in find(img2,"gouxuan.png",0.9):
    #     print i
    #
    # # 截全屏幕
    # # imgscreen  = jietu()
    # # "" mat 一定要有
    # # cv2.imshow("",imgscreen)
    #
    #
    #
    #
    #
    # cv2.waitKey(0)

    # p1.movexy(list1[0].center.x,list1[0].center.y)
    # p1.move(Location(103,277))
    # p1.move(Location(list1[0]).center)
    # p1.dblclick()
    print
