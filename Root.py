# https://www.rs-online.com/designspark/python-tkinter-cn#_Toc61529916

import tkinter as tk
#from tkinter import messagebox

class ProgramBase(tk.Frame):
    def __init__(self, root, width=600, height=400):
        super().__init__(root)
        self.root = root
        self.frame = self
        
        # configure window
        root.width = width
        root.height = height
        geometry = '{0:d}x{1:d}'.format(root.width+5, root.height+5) 
        root.geometry(geometry)    # root.geometry('605x405')
        root.title("window")

        # bind events
        root.bind_all('<Key>', self.onKey)

    def start(self):
        self.root.mainloop()

    def onKey(self, event):
        if event.char == event.keysym or len(event.char) == 1:
            if event.keysym == 'Right':
                print("key Right") 
            elif event.keysym == 'Left':
                 print("key Left") 
            elif event.keysym == 'Space':
                 print("key Space") 
            elif event.keysym == 'Escape':
                print("key Escape") 
                self.root.destroy()
                #messagebox.showinfo("ProgramBase", "Bye Bye")
        #else:
        #print('event.char=', event.char)

if __name__ == '__main__':
    program = ProgramBase(tk.Tk())
    program.start()
    print("quit, bye bye ...")





        