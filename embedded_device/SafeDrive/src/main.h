#include<SPI.h>
#include<Wire.h>
#include<Arduino.h>
#include <LiquidCrystal_I2C.h> // Library for LCD
#include <SPI.h>
#include <Wire.h>
#include <DFRobot_sim808.h>
#include <SoftwareSerial.h>
#include <TinyGPS.h>

//sim808

DFRobot_SIM808 sim808(&Serial);

//LCD
LiquidCrystal_I2C lcd = LiquidCrystal_I2C(0x27, 16, 2); // Change to (0x27,20,4) for 20x4 LCD.

//MQ3 GAS SENSOR
int analogPin = 0; 
int val = 0; 

//GPS
TinyGPS gps;
SoftwareSerial ss(19, 18);

 //var 
  char car_number[9] = "12345678";
  char phone_number[11] = "0525598699";
  char message[200] = "hello\ncar number: 12345678\ndriver is drunk\nPlease come to the following address:ֿ\nhttps://www.google.co.il/maps/dir//31.838982,34.987047/@31.8397003,34.9933818,17.35z/data=!4m2!4m1!3e0?hl=iw\0";




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
    lcd.setCursor(1, 0);
    lcd.print(str1);
    lcd.setCursor(1, 1);
    lcd.print(str2);
}

void printTitle(){
  printToLCD("Breath Analyzer");
}


void printAlcoholLevel(int value){ 
    String val = String(value,DEC);
    unsigned long chars;
    unsigned short sentences, failed;


    while (ss.available()){
        char c = ss.read();
        if (gps.encode(c)){ 
            float flat, flon;
            unsigned long age;
            gps.f_get_position(&flat, &flon, &age);
            Serial.print("LAT=");
            Serial.println(flat == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flat, 6);
            Serial.print("LON=");
            Serial.println(flon == TinyGPS::GPS_INVALID_F_ANGLE ? 0.0 : flon, 6);
            delay(2000);
        }
    }

    if(value<290){
        printToLCD("value: " + val,"You are sober.");
    }
    if(value>=290){
        printToLCD("value: " + val,"You are drunk!");
        delay(2500);
        printToLCD("Send SMS");
        delay(2500);
        sim808.sendSMS(phone_number,message);
    }
 }


 int readAlcohol(){
    int val = 0;
    int count = 0;
    int time = 12;// for 500*12=6000 => 6s
    int sec = time/2; // for display 6 sec
    printToLCD("Please blow to the device:");

    
    
    for(int i=0;i<time;i++){
        if(i%2 == 0){
            printToLCD("Please blow to","the device: " + String(sec,DEC) + "s");
            sec--;
        }
        val += analogRead(analogPin);
        count++;
        delay(450);
    }
    
    return val/count;
 }