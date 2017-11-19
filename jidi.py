import cv2
import numpy as np
from ctypes import *

class Jidi():

    def __init__(self,frame=None):
        #提取出的红队水晶和蓝队水晶的rgb值
        self.red=[[224,54,53]]
        self.blue=[[110,250,254],[8,146,200]]
        #待匹配图片
        self.frame=frame



    def sim_pic(self,frame,colors):
        im=np.zeros(frame.shape[:2]).astype(np.uint8)
        for color in colors:
            r=abs(frame[:,:,2].astype(np.int)-color[0])
            g=abs(frame[:,:,1].astype(np.int)-color[1])
            b=abs(frame[:,:,0].astype(np.int)-color[2])
        #print(r.shape)
            im[r+g+b<100]=255
        return im

    def whowin(self):
        red_pic=self.sim_pic(self.frame,self.red)
        blue_pic = self.sim_pic(self.frame, self.blue)

        image, contours, hierarchy = cv2.findContours(red_pic, 1, 2)
        red_square=max(cv2.contourArea(i) for i in contours)

        image, contours, hierarchy = cv2.findContours(blue_pic, 1, 2)
        blue_square = max(cv2.contourArea(i) for i in contours)
        if red_square>blue_square:
            #红队胜
            return 1
        else:
            #蓝队胜
            return 0
