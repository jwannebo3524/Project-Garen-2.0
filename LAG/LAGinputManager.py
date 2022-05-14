import numpy as np
import keyboard
import mouse
from PIL import Image
import pyautogui as ag
import pydirectinput as di

class LIM:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.Keys = ['q','w','e','1','2','3','f','5','6','r','d','b']
    def GetImageData(self):
        image = ag.screenshot()
        left = 448
        right = 1472
        upper = 156
        lower = 924
        #imagec = image.crop((left,upper,right,lower))
        imagec = image
        return np.array(imagec)

    def HandleOutput(self,vector,mod):
        PI = 3.1415
        O = PI/3
        c = 0
        dist = 10
        xs = 0
        ys = 0
        pos = 0
        if(vector[21]):
            dist = 25*mod
        if(vector[22]):
            dist = 50*mod
        if(vector[23]):
            dist = 75*mod
        if(vector[24]):
            dist = 150*mod
        if(vector[25]):
            dist = 200*mod
        if(vector[26]):
            dist = 250*mod
        while(c<12):
            if(vector[c]>0.5):
                di.keyDown(self.Keys[c])
            else:
                di.keyUp(self.Keys[c])
            c += 1
        if(vector[12]):
            pos = 1
        if(vector[13]):
            pos = 2
        if(vector[14]):
            pos = 3
        if(vector[15]):
            pos = 4
        if(vector[16]):
            pos = 5
        if(vector[17]):
            pos = 6
        if(vector[18]):
            donothing = 0 #accidental extra slot
        xs = (np.cos(O*pos)*dist)+960
        ys = (np.sin(O*pos)*dist)+540
        ag.moveTo(xs, ys)
        if(vector[19]):
            ag.click(button='right')
        if(vector[20]):
            ag.click(button='left')
    def GetUserAction(self,mod):
        PI = 3.1415
        O = PI/3
        self.lx = self.x
        self.ly = self.y
        self.x, self.y = ag.position()
        dist = np.sqrt(np.power(self.x,2)+np.power(self.y,2))
        out = np.zeros(27)
        if(dist>225*mod):
            out[26] = 1
        elif(dist>175*mod):
            out[25] = 1
        elif(dist>112.5*mod):
            out[24] = 1
        elif(dist>62.5*mod):
            out[23] = 1
        elif(dist>37.5*mod):
            out[22] = 1
        elif(dist>17.5*mod):
            out[21] = 1
        c = 0
        while(c<12):
            if(keyboard.is_pressed(self.Keys[c])):
               out[c] = 1
            c += 1
        if((self.x-540) != 0):
            Angle = np.arctan(np.nan_to_num((self.y-960)/(self.x-540)))
        else:
            Angle = 0
        if((self.x-960<0) and (self.y-540<0)):
            Angle = -1*Angle
        elif((self.y-540>0) and(self.x-960<0)):
            Angle = -1*Angle
        if(Angle<0):
            Angle += 2*PI
        if(Angle>2*PI):
            Angle -= 2*PI
        Pos = Angle/O
        if(Pos>5.5):
            out[17] = 1
        elif(Pos>4.5):
            out[16] = 1
        elif(Pos>3.5):
            out[15] = 1
        elif(Pos>2.5):
            out[14] = 1
        elif(Pos>1.5):
            out[13] = 1
        elif(Pos>0.5):
            out[12] = 1
        else:
            out[17] = 1
        if(mouse.is_pressed(button='left')):
               out[19] = 1
        if(mouse.is_pressed(button='right')):
               out[20] = 1
        return out
    def HandleReward(self):
        re = 0
        null = False
        if(keyboard.is_pressed('up')):
            re += 1
        elif(keyboard.is_pressed('left')):
            re += 0.3
        elif(keyboard.is_pressed('right')):
            re -= 0.3
        elif(keyboard.is_pressed('down')):
            re -= 1
        elif(keyboard.is_pressed('z')):
            re = 0
        elif(keyboard.is_pressed('space')):
            assert 1 == 2, 'Program manually stopped'
        else:
            null = True
        return re,null
           
