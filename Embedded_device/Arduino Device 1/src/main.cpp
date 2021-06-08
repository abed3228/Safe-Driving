#include "main.h"
//---------------------------------------------------------------
//        var
//---------------------------------------------------------------
char pwd[4];
char menu='!';
int try_code = 0;
//struct
struct device info;

//gps
static const uint32_t GPSBaud = 9600;
TinyGPSPlus gps;

//---------------------------------------------------------------
//---------------------------------------------------------------
//---------------------------------------------------------------

void setup() {
   //keyboard
  TRANS_SERIAL.begin(9600); 
  SERIAL.begin(9600);  // start serial for output
  SERIAL.println("Version:v1.0");
  Serial.begin(9600);
  //dc
  pinMode(DC, OUTPUT);
  //LCD
  lcd.init();
  lcd.backlight();
  //SD Card Initialization
  pinMode(pinCS, OUTPUT);
  printToLCD("Memory","initialization","","");
  delay(400);
  while(1){
    if(SD.begin()){
      printToLCD("Memory","initialization","success","");
      SD_Read();
      break;
    }
  }
  printToLCD("SIM","initialization","","");
  delay(400);
  //Sim Initialization
  
  while(!sim808.init()) {
    delay(1000);
    Serial.println("Sim808 init error\r\n");
    printToLCD("simerror","","","");
  }  
  Serial.println("Sim808 init success");
  Serial.println("Start to send message ...");
  
  //GPS Initialization
  printToLCD("GPS","initialization","","");
  delay(400);
  Serial1.begin(GPSBaud);

}

void loop() {
  read_sms();
  AlcoholLevelWating();
  printToLCD("Click on the #","to start","","");
  button();
  printToLCD("Get GPS","","","");
  while (Serial1.available() > 0)
    if (gps.encode(Serial1.read())){
      displayInfo();
      delay(1500);
    }
  info.alcohol_level = readAlcohol();
  printAlcohol(info.alcohol_level);
  for(;try_code < try_code_max ; try_code++){
    if(try_code == 0)
      printToLCD("Enter pwd:","","","");
    else
      printToLCD("Enter pwd:","","","try "+String(try_code+1));
    keyboard_code();
    check = check_code();
    clean_code();
    if(check){
      printToLCD("Correct code","","","");
      delay(3000);
      break;
    }
    else{
      printToLCD("Wrong code","","","");
      delay(3000);
    }
  }
  Serial.println(try_code);
  if(try_code == try_code_max){
    send_sms_max_code();
    for(int i = 0 ; i < waiting * 60 ; i++){
      printToLCD("Maximum attempts",String(try_code_max) + " times","",String((waiting * 60)-i) + " sec");
      delay(1000);
    }
  }
  try_code = 0;

  printToLCD("Click on the button","to start","the engine","");
  button();
  dc_open();

  printToLCD("Click on the button","to shutdown","the engine","");
  button_off();
  dc_close(); 
}


void dc_open(){
  analogWrite(DC,255);
}

void dc_close(){
  analogWrite(DC, 0);  
}

void printToLCD(String str1, String str2,String str3,String str4){
    /*  print to lcd monitor
        str1 == line 1    
        str2 == line 2 
        str3 == line 3 
        str4 == line 4 
      */
    lcd.clear(); 
    lcd.setCursor(1, 0);
    lcd.print(str1);
    lcd.setCursor(1, 1);
    lcd.print(str2);
    lcd.setCursor(1, 2);
    lcd.print(str3);
    lcd.setCursor(1, 3);
    lcd.print(str4);
}


void SD_Read(){
  myFile = SD.open("pwd.txt");
  int i = 0;//id
  int j=0;//phone
  int k=0;//code
  int t=0;//car
  if (myFile) {
    Serial.println("Read:");
    delay(250);
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
   delay(250);
  }
  else {
    Serial.println("error opening pwd");
  }
  delay(250);
  Serial.println(info.id);
  Serial.println(info.send_phone);
  Serial.println(info.code_save);
  Serial.println(info.car_number);
  delay(250);
  myFile.close();
}

void SD_Create(char* msg){
  //char msg[]="130+972525598699322806537869";
  delay(250);
   myFile = SD.open("pwd.txt");
   if(myFile){
     if(SD.remove("pwd.txt")){
        Serial.println("SD remove pwd");
        delay(250);
     }
     else{
        Serial.println("error SD remove pwd");
        delay(250);
        return;
     }
   }
  myFile.close();
  delay(250);
   myFile = SD.open("pwd.txt", FILE_WRITE);
  delay(250);
  // if the file opened okay, write to it:
  if (myFile) {
    Serial.print("Writing to file...");
    // Write to file
    delay(250);
    for(int i = 0; i<28 ; i++){
      myFile.print(msg[i]);
    }
    delay(250);
    myFile.close(); // close the file
    Serial.println("Done.");
    delay(250);
     resetFunc();  //call reset
  }
  // if the file didn't open, print an error:
  else {
    Serial.println("error msg");
    delay(250);
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
  }

  Serial.println();
}





void printAlcohol(int value)
{
  value=25;
  Serial.println(info.alcohol_level);
  if(value>400)
  {
     printToLCD("You are drunk!","Sends a message to","a vehicle contact","");
     send_sms_drunk();
     delay(8000);
     loop();
  }
  else{
      printToLCD("You are sober.","","","");
      delay(2500);
  }
 }

 void AlcoholLevelWating(){
  int val = 0;
  int min_val = 30;

  printToLCD("Initializes","a sensor","","");

  while(1){
    val = 25;// analogRead(analogPin);
    Serial.println(val);
    if(val < min_val)
      break;
    delay(2000);
  }
    
  printToLCD("The sensor","is ready","","");
  delay(1000);

 }

 int readAlcohol()
 {
  unsigned int val = 0;

  unsigned int val1 = 0;
  unsigned int val2 = 0;
  unsigned int val3 = 0;
  unsigned int val4 = 0;

  int time = 10;

  printToLCD("Breath Analyzer","Please blow air","10 sec","");
  delay(1000);
  for(int i = 0 ; i<= time ; i++){
    printToLCD("Please blow air","Another " + String(time-i) + " sec","","");
    val1 += analogRead(analogPin); 
    delay(250);
    val2 += analogRead(analogPin); 
    delay(250);
    val3 += analogRead(analogPin);
    delay(250);
    val4 += analogRead(analogPin);
    delay(250);
  }
  val = (val1+val2+val3+val4)/(time*4);
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


  sim808.sendSMS(info.send_phone,msg); 
  Serial.println(msg);
  Serial.println(strlen(msg));
  sim808.sendSMS(info.send_phone,msg_loc); 
  Serial.println(msg_loc);
  Serial.println(strlen(msg_loc));
 }
void send_sms_max_code(){
  char msg[160]="Hello customer\ncar number ";
  strcat(msg,info.car_number);
  strcat(msg,"\n");
  strcat(msg,"The driver reached the maximum of his attempts\n");
  strcat(msg,"at enteringֿ the vehicle code");
}

 void read_sms(){
    int messageLength = 160;
    char message[messageLength];
    int messageIndex = 0;

    char phone[16];
    char datetime[24];

    messageIndex = sim808.isSMSunread();
    Serial.print("messageIndex: ");
    Serial.println(messageIndex);
    //125+972525598699 1234 12345678 

    if (messageIndex > 0) { 
      sim808.readSMS(messageIndex, message, messageLength, phone, datetime);
                  
      sim808.deleteSMS(messageIndex);
      
      Serial.println(message); 
      SD_Create(message);
    
    if(messageIndex > 3)
      for(int i=1 ; i<messageIndex;i++)
        sim808.deleteSMS(i);
  }
 }

void pwd_print(int i){
  if(i == 0)
    printToLCD("Enter pwd:",String(pwd[i]),"","");
  else if (i == 1)
    printToLCD("Enter pwd:","*"+String(pwd[i]),"","");
  else if (i == 2)
    printToLCD("Enter pwd:","**"+String(pwd[i]),"","");
  else if (i == 3)
    printToLCD("Enter pwd:","***"+String(pwd[i]),"","");
  delay(300);
}

void keyboard_code() {
    unsigned long time_strat = millis();
    unsigned long time_end = time_strat + TIME;
    int i = 0;
    while(i<4){
      time_strat = millis();
      if(time_strat > time_end)
        loop();
      TRANS_SERIAL.listen();
      while(TRANS_SERIAL.available()) {
        uint8_t data = TRANS_SERIAL.read();
        TRANS_SERIAL.stopListening();
        switch(data) {
                case 0xE1 :
                    pwd[i] = '1';
                    pwd_print(i);
                    i++;
                    Serial.print(1);
                    break;
                case 0xE2 :
                    pwd[i] = '2';
                    pwd_print(i);
                    i++;
                    Serial.print(2);
                    break;
                case 0xE3 :
                    pwd[i] = '3';
                    pwd_print(i);
                    i++;
                    Serial.print(3);
                    break;
                case 0xE4 :
                    pwd[i] = '4';
                    pwd_print(i);
                    i++;
                    Serial.print(4);
                    break;
                case 0xE5 :
                    pwd[i] = '5';
                    pwd_print(i);
                    i++;
                    Serial.print(5);
                    break;
                case 0xE6 :
                    pwd[i] = '6';
                    pwd_print(i);
                    i++;
                    Serial.print(6);
                    break;
                case 0xE7 :
                    pwd[i] = '7';
                    pwd_print(i);
                    i++;
                    Serial.print(7);
                    break;
                case 0xE8 :
                    pwd[i] = '8';
                    pwd_print(i);
                    i++;
                    Serial.print(8);
                    break;
                case 0xE9 :
                    pwd[i] = '9';
                    pwd_print(i);
                    i++;
                    Serial.print(9);
                    break;
                case 0xEB :
                    pwd[i] = '0';
                    pwd_print(i);
                    i++;
                    Serial.print(0);
                    break;
                default:
                    break;
            }
      }
  }
  Serial.println();
}

bool check_code(){
  for(int i = 0 ;i<3;i++)
    if(info.code_save[i] != pwd[i])
      return false;
  return true;
}

void clean_code(){
  for(int j = 0 ; j < 4 ; j++ ){
    Serial.print(pwd[j]);
    pwd[j]=-1;
  }
  Serial.println();
}

void button(){
  unsigned long time_strat = millis();
  unsigned long time_end = time_strat + TIME;
  bool exit = false;
  TRANS_SERIAL.listen();

  while(!exit){
    time_strat = millis();
    if(time_strat > time_end)
      loop();
    while(TRANS_SERIAL.available()) {
      uint8_t data = TRANS_SERIAL.read();
      TRANS_SERIAL.stopListening();
      switch(data) {
        case 0xEC :
          SERIAL.println("#");
          exit = true;
          break;
      }
    }
  }
}

void button_off(){
  bool exit = false;
  TRANS_SERIAL.listen();

  while(!exit){
    while(TRANS_SERIAL.available()) {
      uint8_t data = TRANS_SERIAL.read();
      TRANS_SERIAL.stopListening();
      switch(data) {
        case 0xEC :
          SERIAL.println("#");
          exit = true;
          break;
      }
    }
  }
}