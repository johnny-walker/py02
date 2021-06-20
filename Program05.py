# https://www.rs-online.com/designspark/python-tkinter-cn#_Toc61529922
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
from Root import ProgramBase

import threading

THREAD_MOUSE_ID = 1    

class MazeThread (threading.Thread):
    def __init__(self, threadID, name, owner):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.owner  = owner       

    def run(self):
        print("Starting " + self.name + " id= " +str(self.threadID))
        
        if self.threadID == THREAD_MOUSE_ID :
            self.owner.move(self.name)

class Pgm05(ProgramBase):
    threadEventMouse = threading.Event()
    threadMouse = None
    
    def __init__(self, root, path, width=640, height=480):
        super().__init__(root, width, height)
        self.root.title('Canvas')

        self.canvas = tk.Canvas(self.root, bg = "gray", width=width, height=height)
        self.canvas.pack()
        self.imgCV2 = None
        self.imgTK = self.loadImage('data/mouse.png')
        self.mouseImgID = self.canvas.create_image(100, 100, anchor = 'nw', image = self.imgTK)
        self.root.update()
    
    def loadImage(self, path):
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        self.imgCV2 = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
        self.rotateImage(90, 0.8)
        return self.resizeAsTKImg()

    def resizeAsTKImg(self):
        im = Image.fromarray(self.imgCV2)               # convert to pillow image fomrat
        im.thumbnail((im.width//12, im.height//12))     # resize by pillow
        return ImageTk.PhotoImage(im)                   # convert to tkinter image

    def rotateImage(self, angle, scale=1.0):
        rows, cols = self.imgCV2.shape[:2]
        matrix2D = cv2.getRotationMatrix2D(((cols-1)/2.0, (rows-1)/2.0), angle, scale)
        self.imgCV2 = cv2.warpAffine(self.imgCV2, matrix2D, (cols,rows))

    def updateMouseImage(self):
        self.imageTKMouse = self.resizeAsTKImg()
        self.canvas.itemconfig(self.mouseImgID, image=self.imageTKMouse)

    def onKey(self, event):
        if event.char == event.keysym or len(event.char) == 1:
            if event.keysym == 'Escape':
                self.threadEventMouse.set() # signal the thread loop to quit
                print("key Escape") 
                self.root.destroy()
            else: # any other key
                self.startWalking()
    
    def startWalking(self):
        print ('start moving')
        self.threadEventMouse.clear()   # reset the thread event
    
        # create thread
        self.threadMouse = MazeThread(THREAD_MOUSE_ID, "Mouse Thread", self)
        self.threadMouse.start()
    
    def move(self, threadName):
        while True:
            if self.threadEventMouse.wait(0.1):  # moving for every 100 ms
                break
            print ('[{0}] keep moving'.format(threadName))
            self.rotateImage(10, 1.0)
            self.updateMouseImage()
        print('[{0}] exit'.format(threadName))

if __name__ == '__main__':
    cwd = os.getcwd()
    mouse = os.path.join(cwd, "data/mouse.png")
    program = Pgm05(tk.Tk(), mouse )

    program.run()
    print("quit, bye bye ...")