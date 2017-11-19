#coding:utf8
import cv2
import os
import copy
from jidi import Jidi
from bifen_baidu import OCR


class Bifen_pic():
    def __init__(self,frame=None):
        #人头比分和推塔数的矩形框
        self.left_rentou = [19, 67, 887, 940]
        self.right_rentou = [19, 67, 985, 1036]
        self.left_tower = [18, 57, 668, 707]
        self.right_tower = [18, 57, 1247, 1292]
        #待匹配图片
        self.frame=frame

    def match_num(self,im,num_pic,num,result,x_s,dis):
        if im.shape[0]<num_pic.shape[0] or im.shape[1]<num_pic.shape[1]:
            return
        res = cv2.matchTemplate(im, num_pic, cv2.TM_SQDIFF_NORMED)
        res = cv2.minMaxLoc(res)

        #[相似度(越小越相似),数字的位置，数字值]
        result.append([res[0], (res[2][0]+x_s,res[2][1]), num])

        #匹配左边的数字
        if res[2][0]>=dis:
            self.match_num(im[:,:res[2][0]], num_pic, num, result,x_s,dis)
        #匹配右边的数字
        if res[2][0]<=im.shape[1]-dis:
            self.match_num(im[:,res[2][0]+15:], num_pic, num, result,x_s+res[2][0]+15,dis)

    #最终的数字
    def ocr_num(self,frame,rect,width,dir):
        im=frame[rect[0]:rect[1],rect[2]:rect[3]]
        result = []
        result_num = ''
        left_x = 0
        right_x = 0
        for i in os.listdir('.\\'+dir):
            num_pic = cv2.imread('.\\'+dir+'\\' + i)
            num = int(i[0])
            self.match_num(im, num_pic, num, result, 0, width)

        result.sort()
        result = list(i for i in result if i[0] < 0.3)
        for i in result:
            if i[1][0] > right_x:
                result_num += str(i[2])
                if len(result_num) == 1:
                    left_x = i[1][0]
                    right_x = left_x + width
                else:
                    return int(result_num)
            elif i[1][0] < left_x - width:
                result_num = str(i[2]) + result_num
                return int(result_num)
        return int(result_num)

    #人头数和推塔数
    def ocr(self):
        left_num = self.ocr_num(self.frame, self.left_rentou, 15, 'bifen_new_left')
        right_num = self.ocr_num(self.frame, self.right_rentou, 15, 'bifen_new_right')
        left_num_tower = self.ocr_num(self.frame, self.left_tower, 10, 'bifen_new_left_small')
        right_num_tower = self.ocr_num(self.frame, self.right_tower, 10, 'bifen_new_right_small')
        print('kill:', left_num, ':', right_num)
        print('tower：', left_num_tower, ':', right_num_tower)
        return (left_num,right_num,left_num_tower,right_num_tower)

ocr=Bifen_pic()
cap = cv2.VideoCapture(r'E:\Downloads\Desktop\15094223560.mp4')

left_head=cv2.imread('.\\head\\left_head.png',cv2.IMREAD_COLOR)
right_head=cv2.imread('.\\head\\right_head.png',cv2.IMREAD_COLOR)

ret,frame=cap.read()
num=1
start_frame=None
start_frame_pic=None
#最后300帧图片，用来判断哪方赢
end_frames_pic=[None]*300
temp_frames_pic=[None]*300
cnt=-1
while True:
    ret, frame = cap.read()
    if not ret:
        break
    res1 = cv2.matchTemplate(frame[5:71, 561:633], left_head, cv2.TM_SQDIFF_NORMED)
    res1 = cv2.minMaxLoc(res1)[0]
    res2 = cv2.matchTemplate(frame[5:71, 1279:1347], right_head, cv2.TM_SQDIFF_NORMED)
    res2 = cv2.minMaxLoc(res2)[0]

    print(num,res1+res2)
    if res1+res2<0.1:
        if start_frame is None:
            start_frame=num
        elif num-start_frame==60:
            start_frame_pic=frame
            break
        if cnt==-1:
            cnt=1
        else:
            cnt=cnt+1
        temp_frames_pic[(cnt-1)%300]=frame
    else:
        if cnt>300:
            end_frames_pic=copy.deepcopy(temp_frames_pic)
            #最后一帧图片，判断比分
            end_frame_pic=temp_frames_pic[(cnt-1)%300]
        cnt=-1
        temp_frames_pic = [None] * 300

    num+=1


#判断哪方赢
jidiwhowin=Jidi()
jidi_cnt=0
for frame in end_frames_pic:
    jidiwhowin.frame=frame
    jidi_cnt+=jidiwhowin.whowin()
if jidi_cnt>150:
    print('red win!!')
else:
    print('blue win!!')

print(jidi_cnt)

#人头比分，推塔数
ocr.frame=end_frame_pic
print(ocr.ocr())

baidu_ocr=OCR()
cv2.imwrite('12345.png',end_frame_pic[0:48,379:412])

#左边大比分
print(baidu_ocr.ocr('12345.png'))
cv2.imwrite('12345.png',end_frame_pic[0:48,1506:1532])
#右边大比分
print(baidu_ocr.ocr('12345.png'))
