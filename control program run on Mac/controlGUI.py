from Tkinter import Tk, BOTH
import Tkinter
from ttk import Frame, Button, Style
import serial

#bluetooth = serial.Serial('/dev/tty.HC-06-DevB',9600,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=0.1)


class application(Frame):
    
    def __init__(self, root):
        Frame.__init__(self, root)
        self.grid()
        self.root = root
        self.root.title("Control GUI")
        self.style = Style()
        self.style.theme_use("default")
        self.initMenu()
        self.initWidgets()
        self.initTerminal()
    
    def initMenu(self):
        #create menu bar
        self.gotoTerminal_button = Tkinter.Button(self, width=17, text="GotoTerminal",command=self.gotoTerminal)
        self.gotoTerminal_button.grid(row=0,column=0,sticky=Tkinter.W)
        
        self.gotoButtonControl_button = Tkinter.Button(self, width=17, text="GotoButtonControl",command=self.gotoButtonControl)
        self.gotoButtonControl_button.grid(row=0,column=1,sticky=Tkinter.W)
        
        self.gotoHandControl_button = Tkinter.Button(self,width=17, text="GotoHandControl",command=self.gotoHandControl)
        self.gotoHandControl_button.grid(row=0,column=2,sticky=Tkinter.W)
    
        self.newData = ""
    
    def initWidgets(self):
        #widgets for terminal
        self.terminal = Tkinter.Text(self,width=80, height=20,wrap=Tkinter.WORD)
        self.entry = Tkinter.Entry(self,width=60)
        self.submit_button = Tkinter.Button(self,text="Submit",width=15,command=self.submit)
        
        #widgets for ButtonControl
        self.forward_button = Tkinter.Button(self, width=17,text="Forward", command=self.forward)
        self.backward_button = Tkinter.Button(self, width=17, text="Backward", command=self.backward)
        self.left_button = Tkinter.Button(self, width=17, text="Left", command=self.turnLeft)
        self.right_button = Tkinter.Button(self, width=17, text="Right", command=self.turnRight)
        self.stop_button = Tkinter.Button(self, width=17, text="Stop", command=self.stop)
        return

    def initTerminal(self):
        #define widgets layout here
        #terminal
        self.terminal.grid(row=1,column=0,columnspan=4,rowspan=2,sticky=Tkinter.W)
        #entry
        self.entry.grid(row=4,column=0,columnspan=3,sticky=Tkinter.W)
        #submit button
        
        self.submit_button.grid(row=4,column=3,sticky=Tkinter.W)
        self.root.bind('<Return>', self.Return)
        self.root.bind('<Tab>', self.Tab)
    
    def initButtonControl(self):
        self.forward_button.grid(row=1, column=1, sticky=Tkinter.W)
        self.backward_button.grid(row=3, column=1, sticky=Tkinter.W)
        self.left_button.grid(row=2, column=0, sticky=Tkinter.W)
        self.right_button.grid(row=2, column=2, sticky=Tkinter.W)
        self.stop_button.grid(row=2, column=1, sticky=Tkinter.W)
        return
    
    
    
    def submit(self):
        content = self.entry.get()
        self.newData = ""
        if content:
            self.entry.delete(0,Tkinter.END)
            self.newData = content
        else:
            return
    
    #clear all widgets
    def clear(self):
        self.terminal.grid_remove()
        self.entry.grid_remove()
        self.submit_button.grid_remove()
        self.forward_button.grid_remove()
        self.backward_button.grid_remove()
        self.right_button.grid_remove()
        self.left_button.grid_remove()
        self.stop_button.grid_remove()
    
    #menu navigation buttons callback
    def gotoTerminal(self):
        self.clear()
        self.initTerminal()
        return
    def gotoButtonControl(self):
        self.clear()
        self.initButtonControl()
        return
    def gotoHandControl(self):
        return

    #Button Control callback
    def forward(self):
        self.newData = "forward"
        return
    def backward(self):
        self.newData = "backward"
    def turnLeft(self):
        self.newData = "left"
    def turnRight(self):
        self.newData = "right"
    def stop(self):
        self.newData = "stop"

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
        #writeData()
        #readBluetoothData()
        root.after(2,communication)
    
    root = Tk()
    root.geometry("600x430+300+300")
    app = application(root)
    root.after(2,communication)
    root.mainloop()


if __name__ == '__main__':
    main()