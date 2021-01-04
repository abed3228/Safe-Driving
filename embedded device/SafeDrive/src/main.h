#include<SPI.h>
#include<Wire.h>
#include<Arduino.h>
#include <LiquidCrystal_I2C.h> // Library for LCD
#include <SPI.h>
#include <Wire.h>

LiquidCrystal_I2C lcd = LiquidCrystal_I2C(0x27, 20, 4); // Change to (0x27,16,2) for 16x2 LCD.


//MQ3 GAS SENSOR
int analogPin = 0; 
int val = 0; 


void printToLCD(String str1){
    /*  print to lcd monitor
        str1 == line 1 
      */
    lcd.clear(); 
    lcd.setCursor(4, 0);
    lcd.print(str1);  
}
void printToLCD(String str1,String str2){
    /*  print to lcd monitor
        str1 == line 1    
        str2 == line 2   
      */
    lcd.clear(); 
    lcd.setCursor(4, 0);
    lcd.print(str1);
    lcd.setCursor(4, 1);
    lcd.print(str2);
}

void printToLCD(String str1,String str2,String str3){
    /*  print to lcd monitor
        str1 == line 1   str3 == line 3  
        str2 == line 2   
      */
    lcd.clear(); 
    lcd.setCursor(4, 0);
    lcd.print(str1);
    lcd.setCursor(4, 1);
    lcd.print(str2);
    lcd.setCursor(4, 2);
    lcd.print(str3);
}

void printToLCD(String str1,String str2,String str3,String str4){
    /*  print to lcd monitor
        str1 == line 1   str3 == line 3  
        str2 == line 2   str4 -- line 4
      */
    lcd.clear(); 
    lcd.setCursor(4, 0);
    lcd.print(str1);
    lcd.setCursor(4, 1);
    lcd.print(str2);
    lcd.setCursor(4, 2);
    lcd.print(str3);
    lcd.setCursor(4, 3);
    lcd.print(str4);
}


void printTitle(){
  printToLCD("Breath Analyzer");
}


void printAlcoholLevel(int value){ 
    String val = String(value,DEC);
    

    if(value<200){
        printToLCD("value:",val,"You are sober.");
    }
    if (value>=200 && value<280){
        printToLCD("value:",val,"You had a beer.");
    }
    if (value>=280 && value<350){
        printToLCD("value:",val,"Two or more beers.");
    }
    if (value>=350 && value <450){
        printToLCD("value:",val,"I smell Oyzo!");
    }
    if(value>450){
        printToLCD("value:",val,"You are drunk!");
    }
 }


 int readAlcohol(){
    int val = 0;
    int val1;
    int val2;
    int val3; 
    
    printToLCD("");

    val1 = analogRead(analogPin); 
    delay(10);
    val2 = analogRead(analogPin); 
    delay(10);
    val3 = analogRead(analogPin);
    
    val = (val1+val2+val3)/3;
    return val;
 }