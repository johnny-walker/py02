# https://www.rs-online.com/designspark/python-tkinter-cn#_Toc61529922
import os
import tkinter as tk
from PIL import Image, ImageTk

# import own modules
import Root as rt

class Program02(rt.ProgramBase):
    def __init__(self, root, width=640, height=480):
        super().__init__(root, width, height)

    def defineLayout(self, widgets, cols=1, rows=1):
        def method(widget, col, row):
            for c in range(col):    
                widget.columnconfigure(c, weight=1)
            for r in range(row):
                widget.rowconfigure(r, weight=1)

        if type(widgets)==list:        
            [ method(wgt, cols, rows) for wgt in widgets ]
        else:
            wgt = widgets
            method(wgt, cols, rows)                   
    
    def loadLayout(self):
        align_mode = 'nswe'
        padding= 2

        imgWidth = self.root.width
        btnHeight = 40
        msgHeight = 40
        imgHeight = self.root.height - btnHeight - msgHeight

        divImg = tk.Frame(self.root,  width=imgWidth , height=imgHeight , bg='blue')
        divBtnArea = tk.Frame(self.root,  width=imgWidth , height=btnHeight , bg='white')
        divMsg = tk.Frame(self.root,  width=imgWidth , height=msgHeight , bg='black')

        divImg.grid(row=0, column=0, padx=padding, pady=padding, columnspan=1, sticky=align_mode)
        divBtnArea.grid(row=1, column=0, padx=padding, pady=padding, columnspan=1, sticky=align_mode)
        divMsg.grid(row=2, column=0, padx=padding, pady=padding, columnspan=1, sticky=align_mode)

        self.defineLayout(self.root, rows=1, cols=1)
        self.defineLayout([divImg, divBtnArea, divMsg], rows=1, cols=1)

        btnPlay = tk.Button(divBtnArea, text='open')
        btnPlay.pack(side='left')

        btnPause = tk.Button(divBtnArea, text='play')
        btnPause.pack(side='left')

        btnPlay1 = tk.Button(divBtnArea, text='stop')
        btnPlay1.pack(side='left')

        btnPause1 = tk.Button(divBtnArea,text='replay')
        btnPause1.pack(side='left')

        lblMsg = tk.Label(divMsg, text='show message here', bg='black', fg='white')
        lblMsg.grid(row=0, column=0, columnspan=1, sticky='w')

        self.root.update()

if __name__ == '__main__':
    program = Program02(tk.Tk())
    program.loadLayout()
    program.run()
    print("quit, bye bye ...")