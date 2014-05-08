'''
Created on 2011-05-12

@author: asutton
'''

from Tkinter import *
import dhva_main as dhva

class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        self.button = Button(frame, text="QUIT", fg="red", command=frame.quit)
        self.button.pack(side=LEFT)

        self.hi_there = Button(frame, text="Run Program", command=self.work)
        self.hi_there.pack(side=LEFT)
    
    def work(self):
        dhva.dhva()
        
root = Tk()

app = App(root)

root.mainloop()