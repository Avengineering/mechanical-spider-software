from Tkinter import Tk, BOTH
import Tkinter
from ttk import Frame, Button, Style


class Example(Frame):
    
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.grid()
        self.parent = parent
        self.initUI()
    
    def initUI(self):
        
        self.parent.title("Control GUI")
        self.style = Style()
        self.style.theme_use("default")
        #create widgets here
        self.click = 0
        self.button = Tkinter.Button(self)
        self.button["text"] = "Total Clicks: 0"
        self.button["command"] = self.update_count
        self.button.grid(row=0,column=0)
    
        self.click2 = 0
        self.button2 = Tkinter.Button(self)
        self.button2["text"] = "Total Clicks: 0"
        self.button2["command"] = self.update_count2
        self.button2.grid(row=0,column=1)
    
    def update_count(self):
        self.click += 1
        self.button["text"] = "Total Clicks: " + str(self.click)
    def update_count2(self):
        self.click2 += 1
        self.button2["text"] = "Total Clicks: " + str(self.click2)


def main():
    
    root = Tk()
    root.geometry("500x400+300+300")
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()