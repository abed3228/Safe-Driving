#include<SPI.h>
#include<Wire.h>
#include<Arduino.h>
#include <LiquidCrystal_I2C.h> // Library for LCD


LiquidCrystal_I2C lcd = LiquidCrystal_I2C(0x27, 20, 4); // Change to (0x27,16,2) for 16x2 LCD.



void printToLCD(String str1,String str2,String str3,String str4){
    /*  print to lcd monitor
        str1 == line 1   str3 == line 3  
        str2 == line 2   str4 -- line 4
      */
    lcd.clear(); 
    if(str1 != ""){
        lcd.setCursor(4, 0);
        lcd.print(str1);
    }
    if(str2 != ""){
        lcd.setCursor(4, 1);
        lcd.print(str2);
    }
    if(str4 != ""){
        lcd.setCursor(4, 2);
        lcd.print(str3);
    }
    if(str4 != ""){
        lcd.setCursor(4, 3);
        lcd.print(str4);
    }

}