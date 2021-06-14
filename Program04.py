# https://www.rs-online.com/designspark/python-tkinter-cn#_Toc61529922
import os
import tkinter as tk
from tkinter import filedialog

# import own modules
import Program03 as pg3

class Pgm04(pg3.Pgm03):
    def __init__(self, root, width=640, height=480):
        super().__init__(root, width, height)
        self.root.title('Image Editor')

if __name__ == '__main__':
    program = Pgm04(tk.Tk(), width=800, height=600)

    # load image data 
    cwd = os.getcwd()
    tiger = os.path.join(cwd, "data/tiger.jpeg")
    program.loadImage(tiger)

    program.run()
    print("quit, bye bye ...")