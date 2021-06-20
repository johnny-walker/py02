import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
import csv
import threading
from Root import ProgramBase

THREAD_MOUSE_ID = 1    
class MazeThread (threading.Thread):
    def __init__(self, threadID, name, owner):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.owner  = owner       

    def run(self):
        print('[{0}] starts, id={1}'.format(self.name, self.threadID))
        if self.threadID == THREAD_MOUSE_ID :
            self.owner.move(self.name)

# action and info for moving
class Map():
    def __init__(self):
        self.info = []
        self.rows = 0
        self.cloumns = 0

    def loadMap(self, filepath):
        with open(filepath, newline='') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                print(row)
                self.info.append(row)
        self.rows = len(self.info)
        self.cloumns = len(self.info[0])
        print('map rows = {0}, cloumns = {1}'.format(self.rows, self.cloumns))
    
class Maze(ProgramBase):
    threadEventMouse = threading.Event()
    threadMouse = None

    def __init__(self, root, width=640, height=480):
        super().__init__(root, width, height)
        self.width = width
        self.height = height
        self.root.title('Mouse Maze')
        self.canvas = tk.Canvas(self.root, bg = "gray", width=width, height=height)
        self.canvas.pack()

        self.map = Map()
        self.sizeX = 0
        self.sizeY = 0
        self.direction = 'east'
        self.imgMouses = {}  # prepare 4 directions' mouse images 
        self.imageTKMouse = None
        self.mouseImgID = 0

    def loadMap(self, path):
        self.map.loadMap(path)
        self.sizeX = self.width/self.map.cloumns
        self.sizeY = self.height/self.map.rows
        self.drawMap()
        self.locateMouse()

    def drawMap(self):
        for x in range (self.map.cloumns):
            for y in range (self.map.rows):
                centx, centy = (x*self.sizeX+self.sizeX/2, y*self.sizeY+self.sizeY/2)
                if self.map.info[y][x] == '0':
                    radius = 5
                    coord_rect = centx-radius, centy-radius, centx+radius, centy+radius
                    self.canvas.create_oval(coord_rect, fill="green")
                else:
                    radius = 2
                    coord_rect = centx-radius, centy-radius, centx+radius, centy+radius
                    color = 'yellow'
                    if self.map.info[y][x] == '2':
                        color = 'blue'
                    elif self.map.info[y][x] == '3':
                        color = 'red'
                    self.canvas.create_oval(coord_rect, fill=color)
    
    def locateMouse(self):
        for x in range (self.map.cloumns):
            for y in range (self.map.rows):
                if self.map.info[y][x] == '2':
                    left, top = (x*self.sizeX, x*self.sizeY)  #top-left corner position
                    cwd = os.getcwd()
                    path = os.path.join(cwd,'data/mouse.png')  
                    print(path)
                    self.imageTKMouse = self.loadImage(path)
                    self.mouseImgID = self.canvas.create_image(left, top, anchor = 'nw', image = self.imageTKMouse)
                    self.canvas.pack()

    def loadImage(self, path):
        imgCV2 = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        imgCV2 = cv2.cvtColor(imgCV2, cv2.COLOR_BGRA2RGBA)
        self.rows, self.cols = imgCV2.shape[:2]
        self.imgMouses['south'] = imgCV2 = self.rotateImage(imgCV2, 0, 0.8)
        self.imgMouses['east']  = self.rotateImage(imgCV2,  90, 1.0)
        self.imgMouses['north'] = self.rotateImage(imgCV2, 180, 1.0)
        self.imgMouses['west']  = self.rotateImage(imgCV2, -90, 1.0)
        return self.resizeAsTKImg(self.imgMouses['south'])
    
    def resizeAsTKImg(self, image):                     # input is CV2 image
        im = Image.fromarray(image)                     # convert to PIL image
        im.thumbnail((im.width//24, im.height//24))     # resize by PIL
        return ImageTk.PhotoImage(im)                   # convert to tkimage PhotoImage

    def rotateImage(self, image, angle, scale=1.0):
        matrix2D = cv2.getRotationMatrix2D(((self.cols-1)/2.0, (self.rows-1)/2.0), angle, scale)
        imgRotate = cv2.warpAffine(image, matrix2D, (self.cols, self.rows))
        return imgRotate

    def updateMouseImage(self, image):
        self.imageTKMouse = self.resizeAsTKImg(image)
        self.canvas.itemconfig(self.mouseImgID, image=self.imageTKMouse)
    
    # override
    def onKey(self, event):
        if event.char == event.keysym or len(event.char) == 1:
            if event.keysym == 'Escape':
                self.threadEventMouse.set() # signal the thread loop to quit
                print("key Escape") 
                self.root.destroy()
            else: # any other key
                if not self.threadMouse:
                    self.startThread()
    
    def startThread(self):
        self.threadMouse = MazeThread(THREAD_MOUSE_ID, "Mouse Thread", self)
        self.threadEventMouse.clear()   # reset the thread event
        self.threadMouse.start()
    
    def move(self, threadName):
        while not self.threadEventMouse.wait(0.2):  # moving for every 200 ms
            #print ('[{0}][{1}] keep moving'.format(threadName, time.time()))
            self.rotateImage(45, 1.0)
            self.updateMouseImage(self.imgMouses[self.direction])
        print('[{0}] exit'.format(threadName))

if __name__ == '__main__':
    print(tk.TkVersion)
    program = Maze(tk.Tk())
    cwd = os.getcwd()
    program.loadMap(os.path.join(cwd,'data/maze_map01.csv'))    
    program.run()
    print("Mouse walks in Maze, bye bye ...")