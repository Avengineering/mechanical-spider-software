from Tkinter import Tk, BOTH
import Tkinter
from ttk import Frame, Button, Style
import serial

bluetooth = serial.Serial('/dev/tty.HC-06-DevB',9600,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=0.1)


class application(Frame):
    
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
        
        #create menu bar
        self.gotoTerminal_button = Tkinter.Button(self, width=17, text="GotoTerminal",command=self.gotoTerminal)
        self.gotoTerminal_button.grid(row=0,column=0,sticky=Tkinter.W)
        
        self.gotoButtonControl_button = Tkinter.Button(self, width=17, text="GotoButtonControl",command=self.gotoButtonControl)
        self.gotoButtonControl_button.grid(row=0,column=1,sticky=Tkinter.W)
        
        self.gotoHandControl_button = Tkinter.Button(self,width=17, text="GotoHandControl",command=self.gotoHandControl)
        self.gotoHandControl_button.grid(row=0,column=2,sticky=Tkinter.W)
        
        #terminal
        self.terminal = Tkinter.Text(self,width=80, height=20,wrap=Tkinter.WORD)
        self.terminal.grid(row=1,column=0,columnspan=4,rowspan=2,sticky=Tkinter.W)
        #entry
        self.entry = Tkinter.Entry(self,width=60)
        self.entry.grid(row=4,column=0,columnspan=3,sticky=Tkinter.W)
        #submit button
        self.submit_button = Tkinter.Button(self,text="Submit",width=15,command=self.submit)
        self.submit_button.grid(row=4,column=3,sticky=Tkinter.W)
        self.root.bind('<Return>', self.Return)
        self.root.bind('<Tab>', self.Tab)

        self.newData = ""
    
    def submit(self):
        content = self.entry.get()
        self.newData = ""
        if content:
            self.entry.delete(0,Tkinter.END)
            self.newData = content
        else:
            return

    def clear(self):
        self.terminal.grid_remove()
        self.entry.grid_remove()
        self.submit_button.grid_remove()
        self.clear_button.grid_remove()
    
    def gotoTerminal(self):
        return
    
    def gotoButtonControl(self):
        return
    
    def gotoHandControl(self):
        return
    
    #binding keys
    def Return(self,event=None):
        self.submit()
    
    def Tab(self, event=None):
        self.entry.insert(Tkinter.END, "\t")
    
    #data transfer
    def getNewData(self):
        data = self.newData
        self.newData = ""
        return data

    def writeToConsole(self, data):
            self.terminal.insert(Tkinter.END, data)
            self.terminal.see(Tkinter.END)


def main():
    def writeData():
        data = app.getNewData()
        if data:
            if data == "\exit":
                bluetooth.write('\x03')
            else:
                bluetooth.write(data+"\n")

    def readBluetoothData():
        bluetoothData = bluetooth.readline()
        for i in range (0,36):
            bluetoothData = bluetoothData.replace("[01;{0}m".format(i),"")
        bluetoothData = bluetoothData.replace("[0m","")
        if bluetoothData:
                app.writeToConsole(bluetoothData)

    
    def communication():
        writeData()
        readBluetoothData()
        root.after(10,communication)
    
    root = Tk()
    root.geometry("600x430+300+300")
    app = application(root)
    root.after(10,communication)
    root.mainloop()


if __name__ == '__main__':
    main()