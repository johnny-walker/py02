import tkinter as tk
#from tkinter import messagebox

class ProgramBase(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        
        # configure Window
        root.width = 600
        root.height = 400
        geometry = '{0:d}x{1:d}'.format(root.width+5, root.height+5)   # '600x400'
        root.geometry(geometry)    
        root.title("Main Window")

        # create Canvas
        canvas = tk.Canvas(root, bg = "black", width=root.width, height=root.height)
        canvas.pack()

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





        