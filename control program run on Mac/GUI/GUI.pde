import processing.serial.*;
import controlP5.*;
import ddf.minim.*;

Serial mySerial = null;
ControlP5 cp5;
AudioPlayer player;
Minim minim;

Textarea terminal;
Textfield input;
DropdownList SerialSelect;
Toggle toggleControl;
Knob Rknob;
Knob Lknob;
ListBox musicListBox;
Chart musicChart;
Button playButton;

String incomingData="";

int joystickXpos = 595;
int joystickYpos = 280;
int joystickOuterRadius = 115;

boolean joystickControl = false;
int numOfSpeeds = 8;
int prevLmotor=0;
int prevRmotor=0;


File dir;
String[] musicList;
boolean playMusic = false;
int musicCount;
int currentMusic=0;
void setup()
{
  size(750,500);
  cp5 = new ControlP5(this);
  gui();
  //music part
  minim = new Minim(this);
  dir = new File(dataPath(""));
  File[] listOfFiles = dir.listFiles();
  musicList = new String[listOfFiles.length];

  for(int i=0; i<listOfFiles.length; i++)
  if(listOfFiles[i].isFile() && listOfFiles[i].getName().indexOf(".mp3")>=0)
      musicList[i] = listOfFiles[i].getName();
  musicGui();
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
                           .setGroup("Terminal")
                           .setFocus(true)
                           .keepFocus(true);
                           
  toggleControl = cp5.addToggle("toggleControl")
                     .setLabel("ON              OFF")
                     .setPosition(480,130)
                     .setSize(70,25)
                     .setValue(false)
                     .setMode(ControlP5.SWITCH);
        
  Lknob = cp5.addKnob("Lknob")
             .setLabel("L motor speed")
             .setRange(-numOfSpeeds,numOfSpeeds)
             .setValue(0)
             .setPosition(490,390)
             .setRadius(45)
             .setNumberOfTickMarks(2*numOfSpeeds)
             .setTickMarkLength(4)
             .snapToTickMarks(true)
             ;
             
  Rknob = cp5.addKnob("Rknob")
             .setLabel("R motor speed")
             .setRange(-numOfSpeeds,numOfSpeeds)
             .setValue(0)
             .setPosition(615,390)
             .setRadius(45)
             .setNumberOfTickMarks(2*numOfSpeeds)
             .setTickMarkLength(4)
             .snapToTickMarks(true)
             ;
                     
                     
}

void musicGui()
{
  musicListBox = cp5.addListBox("musicListBox")
                    .setPosition(10, 425)
                    .setSize(135,65)
                    .setItemHeight(15)
                    .setBarHeight(15)
                    .setLabel("Select Music")
                    .setScrollbarWidth(10)
                    ;
                
  musicListBox.captionLabel().style().marginTop=3;
  musicCount = 0;
  for(int i=0; i<musicList.length; i++){
    if(musicList[i]!=null){
      musicListBox.addItem(musicList[i], musicCount);
      musicCount += 1;
    }
  }
  
  musicChart = cp5.addChart("musicChart")
                  .setPosition(210,410)
                  .setSize(250, 80)
                  .setRange(0,10)
                  .setView(Chart.BAR);
        //musicChart.getColor().setBackground(color(0));
        musicChart.addDataSet("wave")
                  .setColors("wave", color(255,0,0), color(0,255,0))
                  .setData("wave", new float[100])
                  ;
  PImage[] images = {loadImage("Pause.png"),loadImage("Pause.png"),loadImage("Play.png")};         
  playButton = cp5.addButton("playButton")
                  .setPosition(153,440)
                  .setImages(images)
                  .updateSize()
                  ;
}

void updateChart()
{
  if(player!=null && player.isPlaying())
  {
    float[] wave = new float[player.bufferSize()];
    for(int i=0; i<player.bufferSize(); i++)
    {
      wave[i] = player.left.get(i)*10;
    }
    musicChart.setData("wave", wave);
  }else
  {
    musicChart.setData("wave", new float[100]);
  }
  //play next music
  if(playMusic && player!=null && !player.isPlaying()
   && musicCount!=0)
  {
    currentMusic = (currentMusic+1)%musicCount;
    String nextMusicName = musicListBox.getItem(currentMusic).getName();
    player.close();
    minim.stop();
    player = minim.loadFile(nextMusicName);
    player.play();
  }
}

int jx=0; int jy=0;
int jxDst=0; int jyDst=0;
void createJoystick()
{
  int x = joystickXpos; int y = joystickYpos;
  //set the destination of where joystick moves to
  jxDst = jxDst==0 ? x : jxDst;
  jyDst = jyDst==0 ? y : jyDst;
  //joystick moves to destination smoothly
  jx = jx==0 ? x : jx+(jxDst-jx)/3;//(jx+jxDst)/2;
  jy = jy==0 ? y : jy+(jyDst-jy)/3;//(jy+jyDst)/2;
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
  /////////////////////////////
  //send to serial to control//
  /////////////////////////////
  int jcorX = jx-joystickXpos;  //cordinate of x and y from center of joystick
  int jcorY = -(jy-joystickYpos); //reverse the y cordinate
  float length = sqrt(pow(jcorX,2)+pow(jcorY,2)); //displacement of joystick from center
  int avgSpeed = (int)(length/(joystickOuterRadius/numOfSpeeds));
  float angle = atan2((float)jcorY,(float)jcorX); //angle from x-axis
  angle = angle>=0 ? angle : angle + 2*PI;
  int sectorNum = (int)(angle/(2*PI/(4*2*numOfSpeeds)))+1;
  int Lmotor=0, Rmotor=0;
  if(sectorNum >=1 && sectorNum<=2*numOfSpeeds)
  {
    Lmotor = avgSpeed;
    Rmotor = avgSpeed*(-numOfSpeeds+sectorNum)/numOfSpeeds;
  }else if(sectorNum<=2*2*numOfSpeeds)
  {
    Lmotor = avgSpeed*(numOfSpeeds-(sectorNum-2*numOfSpeeds))/numOfSpeeds;
    Rmotor = avgSpeed;
  }else if(sectorNum<=3*2*numOfSpeeds)
  {
    Lmotor = -avgSpeed;
    Rmotor = avgSpeed*(numOfSpeeds-(sectorNum-2*2*numOfSpeeds))/numOfSpeeds;
  }else
  {
    Lmotor = avgSpeed*(-numOfSpeeds+(sectorNum-3*2*numOfSpeeds))/numOfSpeeds;
    Rmotor = -avgSpeed;
  }
  Lknob.setValue(Lmotor);
  Rknob.setValue(Rmotor);
  if(mySerial!=null && joystickControl 
    && (Lmotor!=prevLmotor || Rmotor!=prevRmotor))
  {
    mySerial.write(Lmotor+","+Rmotor+'\n');
    prevLmotor = Lmotor;
    prevRmotor = Rmotor;
    print(Lmotor+","+Rmotor+'\n');
  }
}

void draw()
{
  background(0);
  createJoystick();
  updateChart();
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
    if(incomingData.length()>0)
      terminal.append(incomingData);
    incomingData="";
    terminal.scroll(1);
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
    }else if(event.getGroup().getName()=="musicListBox")
    {
      if(player!=null && player.isPlaying())
        player.close();
      minim.stop();
      player = minim.loadFile(musicListBox.getItem((int)event.value()).getName());
      player.play();
      playMusic = true;
      currentMusic = (int) event.value();
    }
  }
}

public void input(String text)
{
  if(mySerial == null) return;
  mySerial.write(text+"\n");
}

public void toggleControl(int value)
{
  joystickControl = value==1 ? true : false;
  if(mySerial!=null && value == 0)
    mySerial.write("sl\n");
}

public void playButton()
{
  if(playMusic==false){
    PImage[] images = {loadImage("Pause.png"), loadImage("Pause.png"), loadImage("Play.png")};
    playButton.setImages(images);
    playButton.updateSize();
    if(player!=null)
      player.play();
  }else if(playMusic==true){
    PImage[] images = {loadImage("Play.png"), loadImage("Play.png"), loadImage("Pause.png")};
    playButton.setImages(images);
    playButton.updateSize();
    if(player!=null && player.isPlaying())
      player.pause();
  }
  playMusic = !playMusic;
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
