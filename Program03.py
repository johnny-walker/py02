# https://www.rs-online.com/designspark/python-tkinter-cn#_Toc61529922
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# import own modules
import Root as rt

class Pgm03(rt.ProgramBase):
    divImg = None
    lblImg = None
    lblMsg = None

    btnOpen = None
    btnReset = None
    btnBlur = None
    btnSharp = None
    btnCompare = None

    def __init__(self, root, width=640, height=480):
        super().__init__(root, width, height)
        self.root.title('Image Viewer')
        self.loadLayout()
        self.bindBtnEvents()

    def defineLayout(self, widget, cols=1, rows=1):
        #https://stackoverflow.com/questions/45847313/what-does-weight-do-in-tkinter
        for c in range(cols):    
            widget.columnconfigure(c, weight=1)
        for r in range(rows):
            widget.rowconfigure(r, weight=1)
    
    def loadLayout(self):
        align_mode = 'nswe'
        padding= 2
        btnHeight = 40
        msgHeight = 40

        self.imgWidth = self.root.width
        self.imgHeight = self.root.height - btnHeight - msgHeight

        divImg = tk.Frame(self.root,  width=self.imgWidth , height=self.imgHeight , bg='blue')
        divBtnArea = tk.Frame(self.root,  width=self.imgWidth , height=btnHeight , bg='white')
        divMsg = tk.Frame(self.root,  width=self.imgWidth , height=msgHeight , bg='black')

        self.root.update()

        divImg.grid(row=0, column=0, padx=padding, pady=padding, sticky=align_mode)
        divBtnArea.grid(row=1, column=0, padx=padding, pady=padding, sticky=align_mode)
        divMsg.grid(row=2, column=0, padx=padding, pady=padding, sticky=align_mode)

        self.defineLayout(self.root)
        self.defineLayout(divImg)
        self.defineLayout(divBtnArea)
        self.defineLayout(divMsg)

        # label as container of image
        self.divImg = divImg
        '''
        self.lblImg = tk.Label(divImg)
        self.lblImg['width'] = self.imgWidth
        self.lblImg['height'] = self.imgHeight
        self.lblImg.grid(row=0, column=0, sticky=align_mode)
        '''

        # 5 control buttons
        self.btnOpen = tk.Button(divBtnArea, text='open')
        self.btnOpen.pack(side='left')

        self.btnReset = tk.Button(divBtnArea, text='reset')
        self.btnReset.pack(side='left')

        self.btnBlur = tk.Button(divBtnArea, text='blur')
        self.btnBlur.pack(side='left')

        self.btnSharp = tk.Button(divBtnArea,text='sharp')
        self.btnSharp.pack(side='left')

        self.btnCompare = tk.Button(divBtnArea,text='B/A')
        self.btnCompare.pack(side='left')

        # label as message
        self.lblMsg = tk.Label(divMsg, text='show message here', bg='black', fg='white')
        self.lblMsg.grid(row=0, column=0, sticky='w')

    def showMessage(self, msg):
        self.lblMsg['text'] = msg
        
    def bindBtnEvents(self):
        self.btnOpen['command'] = lambda : self.onOpen()
        self.btnReset['command'] = lambda : self.onReset()   
        self.btnBlur['command'] = lambda : self.onBlur()
        self.btnSharp['command'] = lambda : self.onSharp()

    def onOpen(self):
        filename =  filedialog.askopenfilename(initialdir="/", title="Select file")
        if filename:
            self.showMessage("open file {0:s}".format(filename))
            self.loadImage(filename)

    def onReset(self):
        self.showMessage("reset effects")

    def onBlur(self):
        self.showMessage("apply blur effect")

    def onSharp(self):
        self.showMessage("apply sharpness effect")

    def loadImage(self, path):
        im = Image.open(path)
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

        self.showMessage("file {0:s} loaded".format(path))


if __name__ == '__main__':
    program = Pgm03(tk.Tk(), width=800, height=600)
    program.loadLayout()
    program.bindBtnEvents()

    # load image data 
    cwd = os.getcwd()
    tiger = os.path.join(cwd, "data/tiger.jpeg")
    program.loadImage(tiger)

    program.run()
    print("quit, bye bye ...")