import processing.serial.*;
import controlP5.*;

Serial mySerial = null;
ControlP5 cp5;

Textarea terminal;
Textfield input;
DropdownList SerialSelect;

String incomingData="";

int joystickXpos = 595;
int joystickYpos = 280;
int joystickOuterRadius = 115;
void setup()
{
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
                           .setFont(createFont("", 16))
                           .setLineHeight(14)
                           .setColor(color(128))
                           .setColorBackground(color(255,100))
                           .setColorForeground(color(255,100))
                           .setColor(color(#28F764))
                           .setGroup("Terminal")
                           .setText("Terminal")
                           ;
                input = cp5.addTextfield("input")
                           .setPosition(0,350)
                           .setSize(450,25)
                           .setFont(createFont("arial",16))
                           .setGroup("Terminal");
}

int jx=0; int jy=0;
int jxDst=0; int jyDst=0;
void createJoystick()
{
  int x = joystickXpos; int y = joystickYpos;
  jxDst = jxDst==0 ? x : jxDst;
  jyDst = jyDst==0 ? y : jyDst;
  jx = jx==0 ? x : (jx+jxDst)/2;
  jy = jy==0 ? y : (jy+jyDst)/2;
  int outerRadius = joystickOuterRadius;
  int innerRadius = outerRadius/3;
  ellipseMode(CENTER);
  noStroke();
  if(sqrt(pow((mouseX-x),2)+pow((mouseY-y),2))<=outerRadius)
  {
    fill(color(15,109,188));
  }
  else{
    fill(color(15,109,188,160));
  }
  ellipse(x, y, 2*outerRadius, 2*outerRadius);
  fill(color(34,42,240));
  ellipse(jx, jy, 2*innerRadius, 2*innerRadius);
}

void draw()
{
  background(0);
  createJoystick();
}

void serialEvent(Serial p)
{
  String newData = p.readString();
  printToTerminal(newData);
}

void printToTerminal(String Data)
{
  incomingData += Data;
  int length = incomingData.length();
  if(incomingData.charAt(length-1)=='\n'
   ||incomingData.charAt(length-1)=='$')
  {
    for(int i=33; i<=37; i++){
      String pattern = String.format("[01;%dm",i);
      incomingData = incomingData.replace(pattern,"");
    }
    incomingData = incomingData.replace("[0m","");
    terminal.append(incomingData);
    incomingData="";
  }
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
  }
}

public void input(String text)
{
  if(mySerial == null) return;
  mySerial.write(text+"\n");
}

void keyPressed()
{
  if(key==3)
  {
    input.clear();
    if(mySerial!=null)
      mySerial.write("\u0003");
  }
}

void mousePressed()
{
  if(sqrt(pow((mouseX-joystickXpos),2)+pow((mouseY-joystickYpos),2))<=joystickOuterRadius)
  {
     jxDst = mouseX;
     jyDst = mouseY; 
  }
}

void mouseDragged()
{
  if(sqrt(pow((mouseX-joystickXpos),2)+pow((mouseY-joystickYpos),2))<=joystickOuterRadius)
  {
     jxDst = mouseX;
     jyDst = mouseY; 
  }
}

void mouseReleased()
{
  jxDst = 0;
  jyDst = 0;
}
