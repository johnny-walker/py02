# https://www.rs-online.com/designspark/python-tkinter-cn#_Toc61529922
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np

from Root import ProgramBase

class Pgm05(ProgramBase):
    def __init__(self, root, path, width=640, height=480):
        super().__init__(root, width, height)
        self.root.title('Canvas')

        self.canvas = tk.Canvas(self.root, bg = "gray", width=width, height=height)
        self.canvas.pack()

        img = Image.open('data/mouse.png')
        img = img.resize((img.width//20,img.height//20), Image.ANTIALIAS)
        self.img = self.loadImage('data/mouse.png')
        self.canvas.create_image(10, 10, anchor = 'nw', image = self.img)
        self.root.update()
    
    def loadImage(self, path):
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
        im = Image.fromarray(img)
        im.thumbnail((im.width//32, im.height//32))
        return ImageTk.PhotoImage(im)

if __name__ == '__main__':
    cwd = os.getcwd()
    mouse = os.path.join(cwd, "data/mouse.png")
    program = Pgm05(tk.Tk(), mouse )

    program.run()
    print("quit, bye bye ...")