import tkinter as tk
import programRoot

class Program01(programRoot.ProgramBase):
    def __init__(self, root):
        super().__init__(root)

if __name__ == '__main__':
    program = Program01(tk.Tk())
    program.start()
    print("quit, bye bye ...")