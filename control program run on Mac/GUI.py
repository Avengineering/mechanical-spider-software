from Tkinter import Tk, BOTH
import Tkinter
from ttk import Frame, Button, Style


class Example(Frame):
    
    def __init__(self, root):
        Frame.__init__(self, root)
        self.grid()
        self.root = root
        self.initUI()
    
    def initUI(self):
        
        self.root.title("Control GUI")
        self.style = Style()
        self.style.theme_use("default")
        #create widgets here
        
        #buttons
        #self.click = 0
        #self.button = Tkinter.Button(self)
        #self.button["text"] = "Total Clicks: 0"
        #self.button["command"] = self.update_count
        #self.button.grid(row=0,column=0)
    
        #label
        self.instruction = Tkinter.Label(self, text = "            Enter the password                ")
        self.instruction.grid(row=0,column=0,columnspan=2,sticky=Tkinter.W)
    
        #Entry
        self.password = Tkinter.Entry(self)
        self.password.grid(row=3,column=0,sticky=Tkinter.W)
    
        #summit button
        self.submit_button = Tkinter.Button(self, text="Submit", command=self.reveal)
        self.submit_button.grid(row=3,column=1,sticky=Tkinter.W)
        self.root.bind('<Return>',self.Return)
    
        #text
        self.text = Tkinter.Text(self,width=35, height=5,wrap=Tkinter.WORD)
        self.text.grid(row=1,column=0,columnspan=2,rowspan=2,sticky=Tkinter.W)
    
    def reveal(self):
        content = self.password.get()
        if content == "password":
            message = "You have access\n"
        else:
            message = "Access denied\n"
        #self.text.delete(0.0,Tkinter.END)
        self.text.insert(Tkinter.END,message)
        self.password.delete(0,Tkinter.END)

    def Return(self, event=None):
        self.reveal()
    
    def update_count(self):
        self.click += 1
        self.button["text"] = "Total Clicks: " + str(self.click)

app = 0

def main():
    
    root = Tk()
    root.geometry("500x400+300+300")
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()