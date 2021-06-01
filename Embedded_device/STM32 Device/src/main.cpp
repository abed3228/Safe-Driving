#include "main.h"
//---------------------------------------------------------------
//        var
//---------------------------------------------------------------
char pwd[4];
char menu='!';
int try_code = 0;
//LCD
const int colorR = 0;
const int colorG = 0;
const int colorB = 255;
//struct
struct device info;
//time
unsigned long time_strat;
unsigned long time_end;
//gps
static const uint32_t GPSBaud = 9600;
int cmp_gps;
int exit_gps=false;
static const int RXPin = 4, TXPin = 3;
TinyGPSPlus gps;
SoftwareSerial softSerial(RXPin, TXPin);
//sim
DFRobot_SIM808 sim808(&Serial);
int messageIndex = 0;//sms






void setup(){
    Serial.begin(9600); 
  //dc
  pinMode(DC, OUTPUT);
  //LCD
  lcd.begin(16, 2);
  lcd.setRGB(colorR, colorG, colorB);
  //SD
  pinMode(pinCS, OUTPUT);
  //Sim Initialization
   while(!sim808.init()) {
      delay(1000);
      Serial.print("Sim808 init error\r\n");
      lcd.setRGB(255, 0, 0);
      printToLCD("simerror");
  }  
  Serial.println("Sim808 init success");
  Serial.println("Start to send message ...");
  // SD Card Initialization
  while(1){
    if (SD.begin()){
      Serial.println("SD card is ready to use.");
      lcd.setRGB(colorR, colorG, colorB);
      SD_Read();
      break;
    }
    else{
      printToLCD("memory failed");
      lcd.setRGB(255, 0, 0);
      delay(3000);
    }
    lcd.setRGB(colorR, colorG, colorB);
  }
  //gps
  softSerial.begin(GPSBaud);

 printToLCD("get gps","loctions");
  while(!exit_gps){
    while (softSerial.available() > 0){
      if (gps.encode(softSerial.read())){
        displayInfo();
        delay(500);
        cmp_gps=0;
        cmp_gps = strcmp(info.location_lat,"31.95245543217836");
        Serial.println(cmp_gps);
      }
      if(cmp_gps != 0){
        Serial.println("exit cmp");
        exit_gps=true;
        break;
      }
    }
  }
  Serial.println("ready");
  delay(3000);
}

void loop() {
  AlcoholLevelWating();
  printToLCD("Please press"," # to strat");
  info.alcohol_level = readAlcohol();
  if(printAlcohol(info.alcohol_level)){
    while (softSerial.available() > 0)
      if (gps.encode(softSerial.read())){
        displayInfo();
        delay(1500);
      }
    printToLCD("You are drunk!","send sms");
    send_sms_drunk();
    loop();
  }
}



void dc_open(){
  analogWrite(DC,255);
}

void dc_close(){
  analogWrite(DC, 0);  
}


void printToLCD(String str1){
    /*  print to lcd monitor
        str1 == line 1 
      */
    lcd.clear(); 
    lcd.setCursor(1, 0);
    lcd.print(str1);  
}
void printToLCD(String str1, String str2){
    /*  print to lcd monitor
        str1 == line 1    
        str2 == line 2   
      */
    lcd.clear(); 
    lcd.setCursor(0, 0);
    lcd.print(str1);
    lcd.setCursor(0, 1);
    lcd.print(str2);
}
void pwd_print(int i){
  if(i == 0)
    printToLCD("Enter pwd:",String(pwd[i]));
  else if (i == 1)
    printToLCD("Enter pwd:","*"+String(pwd[i]));
  else if (i == 2)
    printToLCD("Enter pwd:","**"+String(pwd[i]));
  else if (i == 3)
    printToLCD("Enter pwd:","***"+String(pwd[i]));
  delay(300);
}

void SD_Read(){
  myFile = SD.open("pwd.txt");
  int i = 0;//id
  int j=0;//phone
  int k=0;//code
  int t=0;//car
  if (myFile) {
    Serial.println("Read:");
    while (myFile.available()) {
      char ch = myFile.read();
      if(i<=2){
        if(info.id[i] != ch){
          Serial.println("error dev id");
          break;
        }
      }
      else if(i>2 && i<=15){
        info.send_phone[j]=ch;
        j++;
      }
      else if(i>15 && i<=19){
        info.code_save[k]=ch;
        k++;
      }
      else{
        info.car_number[t]=ch;
        t++;
      }

      i++;
   }
  }
  else {
    Serial.println("error opening pwd");
  }
  Serial.println(info.id);
  Serial.println(info.send_phone);
  Serial.println(info.code_save);
  Serial.println(info.car_number);
  myFile.close();
}

void SD_Create(char* msg){
  char send[]="Hello customer\ncar number ";
  strcat(send,info.car_number);
  strcat(send,"\nupdate complete\nThank you");
   myFile = SD.open("pwd.txt");
   if(myFile){
     if(SD.remove("pwd.txt"))
        Serial.println("SD remove pwd");
     else{
        Serial.println("error SD remove pwd");
        return;
     }
   }
  myFile.close();
  Serial.println(msg);
   myFile = SD.open("pwd.txt", FILE_WRITE);
  
  // if the file opened okay, write to it:
  if (myFile) {
    Serial.println("Writing to file...");
    delay(1200);
    // Write to file
    for(int i = 0; i<28 ; i++){
      myFile.print(msg[i]);
    }
    delay(1200);
    myFile.close(); // close the file
    Serial.println("Done.");
    delay(1200);
    sim808.sendSMS(info.send_phone,send); 
    delay(1200);
    resetFunc();  //call reset
  }
  // if the file didn't open, print an error:
  else {
    Serial.println("error msg");
    return;
  }
}
void displayInfo()
{
 
  String lat;
  String lng;

  Serial.print(F("Location: ")); 
  if (gps.location.isValid())
  {
   
    lat = String(gps.location.lat(),DEC);
    lng = String(gps.location.lng(),DEC);

    lat.toCharArray(info.location_lat,20); 
    lng.toCharArray(info.location_lng,20);    
   
    Serial.print(F("     "));
    Serial.print(info.location_lat);
    Serial.print(F(","));
    Serial.print(info.location_lng);
  }
  else
  {
    Serial.print(F("INVALID"));
    strcpy(info.location_lat,"31.95245543217836");
    strcpy(info.location_lng,"34.90169287913625");
  }

  Serial.println();
}





bool printAlcohol(int value)
{
  Serial.println(info.alcohol_level);
  if(value>400)
  {
     printToLCD("You are drunk!");
      delay(1500);
     return true;
  }
  else{
      printToLCD("You are sober.");
      delay(1500);
  }
  return false;
 }

 void AlcoholLevelWating(){
  int val = 0;
  int min_val = 30;

  printToLCD("Initializes","a sensor");

  while(1){
    val = analogRead(analogPin);
    if(val < min_val)
      break;
    delay(2000);
  }
    
  printToLCD("The sensor","is ready");
  delay(1000);

 }

 int readAlcohol()
 {
  unsigned int val = 0;
  unsigned int test = 0 ;
  unsigned int val1 = 0;
  unsigned int val2 = 0;
  unsigned int val3 = 0;
  unsigned long time = millis()/1000;
  unsigned long time_end = millis()/1000 + 10; 

  printToLCD("Breath Analyzer");

  while(time = millis()/1000 < time_end){
    val1 += analogRead(analogPin); 
    delay(150);
    val2 += analogRead(analogPin); 
    delay(150);
    val3 += analogRead(analogPin);
    test++;
  }
  val = (val1+val2+val3)/(test*3);
  return val;
 }


 void send_sms_drunk(){
   //Please come to the following address:ֿ\nhttps://www.google.co.il/maps/dir//31.838982,34.987047/@31.8397003,34.9933818,17.35z/data=!4m2!4m1!3e0?hl=iw\0";


   //   /@31.8397003,34.9933818,17.35z/data=!4m2!4m1!3e0?hl=iw\0";


  char msg[160]="Hello customer\ncar number ";
  char msg_loc[160]="https://www.google.co.il/maps/dir//";

  strcat(msg,info.car_number);
  strcat(msg,"\n");
  strcat(msg,"The driver of the car is drunk\n");
  strcat(msg,"Please come to the following address");

  strcat(msg_loc,info.location_lat);
  strcat(msg_loc,",");
  strcat(msg_loc,info.location_lng);
  strcat(msg_loc,"/@");
  strcat(msg_loc,info.location_lat);
  strcat(msg_loc,",");
  strcat(msg_loc,info.location_lng);
  strcat(msg_loc,",17.35z/data=!4m2!4m1!3e0?hl=iw\0");
  //******** define phone number and text **********

  delay(1500);
  sim808.sendSMS(info.send_phone,msg); 
  sim808.sendSMS(info.send_phone,msg_loc); 
 }



 void read_sms(int msgIndex){
    int messageLength = 160;
    char message[messageLength];

    char phone[16];
    char datetime[24];

    Serial.print("messageIndex: ");
    Serial.println(msgIndex);
    //125+972525598699 1234 12345678 

    if (msgIndex > 0) { 
      sim808.readSMS(msgIndex, message, messageLength, phone, datetime);
            
    if(msgIndex > 0)
      for(int i=1 ; i<msgIndex;i++)
        sim808.deleteSMS(i);
  
    Serial.println(message);
    if(message[0] == info.id[0] && message[1] == info.id[1] && message[2] == info.id[2] ) 
      SD_Create(message);
  
  }
 }