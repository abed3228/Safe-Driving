#include <Arduino.h>
#include <Wire.h>
#include <string.h>
#include <SPI.h>
#include <SD.h>
#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <rgb_lcd.h>
#include"DFRobot_sim808.h"
//---------------------------------------------------------------
//        pins
//---------------------------------------------------------------

//dc
#define DC 2
//LCD
rgb_lcd lcd;
//SD
File myFile;
int pinCS = 14; 
//MQ3
int analogPin = A2;


//var
#define SIZE_ID 4
#define SIZE_CAR 9
#define SIZE_PHONE 14
#define SIZE_PWD 5

//---------------------------------------------------------------
//        func
//---------------------------------------------------------------
//           111111 1111 22222228
//012 3456789012345 6789 01234567
//125 +972525598699 1234 12345678 
//id    phone        pwd    car
struct device
{
    char id[SIZE_ID]="125";//V
    char car_number[SIZE_CAR];//V
    char send_phone[SIZE_PHONE];//V

    char location_lat[20] ;
    char location_lng[20];

    int alcohol_level;

    char code_save[SIZE_PWD];//V
};


//---------------------------------------------------------------
//        func
//---------------------------------------------------------------
//Mini Fan - DC
void dc_open();
void dc_close();
//LCD
void printToLCD(String str1);
void printToLCD(String str1,String str2);
void pwd_print(int i);
//SD
void SD_Read();// Reading the file
void SD_Create(char* msg);//Create/Open file
// resetFunc();  //call reset
void(* resetFunc) (void) = 0; //declare reset function @ address 0
//gps
void displayInfo();
//MQ3
bool printAlcohol(int value);
void AlcoholLevelWating();
int readAlcohol();
//sim
void send_sms_drunk();
void read_sms(int messageIndex);