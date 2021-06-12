# https://www.rs-online.com/designspark/python-tkinter-cn#_Toc61529922
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# import own modules
import Root as rt

class Program03(rt.ProgramBase):
    def __init__(self, root, width=640, height=480):
        super().__init__(root, width, height)
        self.devImg = None
        self.lblImg = None
        self.btnOpen = None
        self.btnPause = None
        self.btnStop = None
        self.btnReplay = None
        self.lblMsg = None

    def defineLayout(self, widgets, cols=1, rows=1):
        def method(widget):
            for c in range(cols):    
                widget.columnconfigure(c, weight=1)
            for r in range(rows):
                widget.rowconfigure(r, weight=1)
            return

        if type(widgets)==list:        
            [ method(wgt) for wgt in widgets ]
        else:
            wgt = widgets
            method(wgt)                   
    
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
        self.defineLayout([divImg, divBtnArea, divMsg])

        # label as container of image
        self.devImg = divImg
        '''
        self.lblImg = tk.Label(divImg)
        self.lblImg['width'] = self.imgWidth
        self.lblImg['height'] = self.imgHeight
        self.lblImg.grid(row=0, column=0, sticky=align_mode)
        '''

        # 4 control buttons
        self.btnOpen = tk.Button(divBtnArea, text='open')
        self.btnOpen.pack(side='left')

        self.btnPause = tk.Button(divBtnArea, text='play')
        self.btnPause.pack(side='left')

        self.btnStop = tk.Button(divBtnArea, text='stop')
        self.btnStop.pack(side='left')

        self.btnReplay = tk.Button(divBtnArea,text='replay')
        self.btnReplay.pack(side='left')

        # label as message
        self.lblMsg = tk.Label(divMsg, text='show message here', bg='black', fg='white')
        self.lblMsg.grid(row=0, column=0, sticky='w')

    def showMessage(self, msg):
        self.lblMsg['text'] = msg
        
    def bindBtnEvents(self):
        self.btnOpen['command'] = lambda : self.onOpen()
        self.btnPause['command'] = lambda : self.onPause()   # play/pause 
        self.btnStop['command'] = lambda : self.onStop()
        self.btnReplay['command'] = lambda : self.onReplay()

    def onOpen(self):
        self.showMessage('open file...')
        filename =  filedialog.askopenfilename(initialdir="/", title="Select file")
        self.showMessage("open file {0:s}".format(filename))
        self.loadImage(filename)

    def onPlay(self):
        self.showMessage("play file {0:s}".format('...'))

    def onPause(self):
        self.showMessage("pause file {0:s}".format('...'))

    def onStop(self):
        self.showMessage("stop file {0:s}".format('...'))

    def onReplay(self):
        self.showMessage("replay file {0:s}".format('...'))

    def loadImage(self, path):
        im = Image.open(path)
        tkimage = ImageTk.PhotoImage( im.resize( (self.imgWidth, self.imgHeight) ) )

        if self.lblImg:
            self.lblImg.destroy()

        # create label
        self.lblImg = tk.Label(self.devImg, image=tkimage)
        self.lblImg.image = tkimage    
        self.lblImg.grid(row=0, column=0)
        self.lblImg['width'] = self.imgWidth
        self.lblImg['height'] = self.imgHeight

        align_mode = 'nswe'
        self.lblImg.grid(row=0, column=0, sticky=align_mode)

        self.showMessage("file {0:s} loaded".format(path))


if __name__ == '__main__':
    program = Program03(tk.Tk(), width=800, height=600)
    program.loadLayout()
    program.bindBtnEvents()

    # load image data 
    cwd = os.getcwd()
    tiger = os.path.join(cwd, "data/tiger.jpeg")
    program.loadImage(tiger)

    program.run()
    print("quit, bye bye ...")