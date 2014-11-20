import processing.serial.*;
import controlP5.*;

Serial mySerial = null;
ControlP5 cp5;

Textarea terminal;
Textfield input;
DropdownList SerialSelect;

void setup()
{
  background(0);
  size(750,500);
  cp5 = new ControlP5(this);
  gui();
}

void gui()
{
  SerialSelect = cp5.addDropdownList("SerialSelect")
                    .setPosition(470,25)
                    .setSize(250,100)
                    .setItemHeight(20)
                    .setBarHeight(20)
                    .setScrollbarWidth(10)
                    ;
        SerialSelect.captionLabel().set("Select Serial Port");
        SerialSelect.captionLabel().style().marginTop=3;
        SerialSelect.addItem("Select Serial Port",0);
        for(int i=1; i<mySerial.list().length;i++){
          SerialSelect.addItem(mySerial.list()[i],i);
        }
  
  Group terminalGroup = cp5.addGroup("Terminal")
                           .setPosition(10,20)
                           .setWidth(450)
                           .setHeight(15)
                           .setBackgroundHeight(450);
             terminal = cp5.addTextarea("terminal")
                           .setPosition(0,0)
                           .setSize(450,350)
                           .setFont(createFont("arial", 16))
                           .setLineHeight(14)
                           .setColor(color(128))
                           .setColorBackground(color(255,100))
                           .setColorForeground(color(255,100))
                           .setColor(color(#28F764))
                           .setGroup("Terminal")
                           .setText("hello world")
                           ;
                input = cp5.addTextfield("input")
                           .setPosition(0,350)
                           .setSize(450,25)
                           .setFont(createFont("arial",16))
                           .setGroup("Terminal");
}

void draw()
{
  background(0);
}

void controlEvent(ControlEvent event)
{
  if(event.isGroup())
  {
    if(event.getGroup().getName()=="SerialSelect")
    {
      if(mySerial != null){mySerial.stop(); mySerial = null;}
      if(event.value()==0){return;}
      mySerial = new Serial(this, SerialSelect.getItem((int)event.value()).getName(), 9600);
    }
    //println("event from group "+event.getGroup().getName()+" of item "+(SerialSelect.getItem((int)event.value())).getName());
  }
}

public void input(String text)
{
  terminal.append("\n"+text);
}

