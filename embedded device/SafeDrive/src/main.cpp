#include<main.h>




void printToLCD(String str1);
void printToLCD(String str1,String str2);
void printToLCD(String str1,String str2,String str3);
void printToLCD(String str1,String str2,String str3,String str4);

void printTitle();
void printAlcoholLevel(int value);
int readAlcohol();


void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
}

void loop() {
  delay(100);
  
  val = readAlcohol();
  printTitle();
  delay(1500);
 
  printTitle();
  printAlcoholLevel(val);  
  
  delay(5000);
  printToLCD("");
}

