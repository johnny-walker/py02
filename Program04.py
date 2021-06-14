# https://www.rs-online.com/designspark/python-tkinter-cn#_Toc61529922
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np

# import own modules
from Program03 import Pgm03

class Pgm04(Pgm03):
    cvImg = None
    cvImgUpdate = None

    def __init__(self, root, width=640, height=480):
        super().__init__(root, width, height)
        self.root.title('Image Editor')
        self.bind3BtnEvents()

    def bind3BtnEvents(self):
        self.btnReset['command'] = lambda : self.onReset()   
        self.btnBlur['command'] = lambda : self.onBlur()
        self.btnSharp['command'] = lambda : self.onSharp()
    
    def onReset(self):
        self.showMessage("reset effects")
        self.cvImgUpdate = self.cvImg
        self.updateImage()

    def onBlur(self):
        size = 9
        self.showMessage("apply gaussian blur ")
        self.cvImgUpdate = cv2.GaussianBlur(self.cvImgUpdate,(size, size), 0)
        self.updateImage()

    def onSharp(self):
        self.showMessage("apply sharpen effect")
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        self.cvImgUpdate = cv2.filter2D(self.cvImgUpdate, -1, kernel)
        self.updateImage()

    def loadImage(self, path):
        self.cvImg = cv2.imread(path)
        self.cvImg = self.cvImg[:,:,::-1] # 將 BGR 圖片轉為 RGB 圖片
        self.cvImgUpdate = self.cvImg.copy()
        self.updateImage()
        self.showMessage("file {0:s} loaded".format(path))

    def updateImage(self):
        im = Image.fromarray(self.cvImgUpdate)
        im.thumbnail((self.imgWidth, self.imgHeight))
        tkimage = ImageTk.PhotoImage(im)

        if self.lblImg:
            self.lblImg.destroy()

        # create label
        self.lblImg = tk.Label(self.divImg, image=tkimage)
        self.lblImg.image = tkimage    
        self.lblImg.grid(row=0, column=0)
        self.lblImg['width'] = self.imgWidth
        self.lblImg['height'] = self.imgHeight

        align_mode = 'nswe'
        self.lblImg.grid(row=0, column=0, sticky=align_mode)

if __name__ == '__main__':
    program = Pgm04(tk.Tk(), width=800, height=600)

    # load image data 
    cwd = os.getcwd()
    tiger = os.path.join(cwd, "data/tiger.jpeg")
    program.loadImage(tiger)

    program.run()
    print("quit, bye bye ...")