import os
import tkinter as tk
from PIL import Image, ImageTk

# import own modules
import Root as rt

class Program01(rt.ProgramBase):
    def __init__(self, root, width=640, height=480):
        super().__init__(root, width, height)

    def loadImage(self, path):
        img = Image.open(path)                    
        img = img.resize( (self.root.width , self.root.height ) )   
        imgTk =  ImageTk.PhotoImage(img)                        

        lbl = tk.Label(self.root, image=imgTk)                   
        lbl.image = imgTk
        lbl.grid(column=0, row=0)                             

if __name__ == '__main__':
    program = Program01(tk.Tk())
    
    cwd = os.getcwd()
    tiger = os.path.join(cwd, "data/tiger.jpeg")
    program.loadImage(tiger)

    program.start()
    print("quit, bye bye ...")