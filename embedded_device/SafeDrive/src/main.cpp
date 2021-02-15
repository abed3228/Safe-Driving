#include<main.h>



//LCD
void printToLCD(String str1);
void printToLCD(String str1,String str2);

//MQ3-GAS
void printTitle();
void printAlcoholLevel(int value);
int readAlcohol();
//GPS


void setup() {
 
  Serial.begin(9600);
  Serial2.begin(9600); // connect gps sensor
  lcd.init();
  lcd.backlight();
  pinMode(40, OUTPUT);
  digitalWrite(40, LOW);
  ss.begin(9600);
  while(!sim808.init()) {
      delay(1000);
      Serial.print("Sim808 init error\r\n");
      digitalWrite(40, HIGH);
  }
  
}


void loop() {
  delay(100);
  
  val = readAlcohol();
  delay(1500);
 
  printTitle();
  printAlcoholLevel(val);  
  
  delay(5000);
  printToLCD("");

 
}




