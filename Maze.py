import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
import csv

# import own module
from Root import ProgramBase

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
        self.mouse = None

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
                    self.imageMouse = self.loadImage(path)
                    self.mouseID = self.canvas.create_image(left, top, anchor = 'nw', image = self.imageMouse)
                    self.canvas.pack()

    def resizeAsTKImg(self):
        im = Image.fromarray(self.imgCV2)
        im.thumbnail((im.width//24, im.height//24))
        return ImageTk.PhotoImage(im)

    def loadImage(self, path):
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        self.imgCV2 = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
        self.rotateImage(0, 0.8)
        return self.resizeAsTKImg()


    def rotateImage(self, angle, scale = 1.0):
        rows, cols = self.imgCV2.shape[:2]
        matrix2D = cv2.getRotationMatrix2D(((cols-1)/2.0, (rows-1)/2.0), angle, scale)
        self.imgCV2 = cv2.warpAffine(self.imgCV2, matrix2D, (cols,rows))

    def updateMouseImage(self):
        im = self.resizeAsTKImg()
        self.canvas.itemconfig(self.image_on_canvas, image=im)

if __name__ == '__main__':
    print(tk.TkVersion)
    program = Maze(tk.Tk())
    cwd = os.getcwd()
    program.loadMap(os.path.join(cwd,'data/maze_map01.csv'))    
    program.run()
    print("Mouse walks in Maze, bye bye ...")