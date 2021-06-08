#include <Arduino.h>
#include <Wire.h>
#include <string.h>
#include <SD.h>
#include <SPI.h>
#include <TinyGPS++.h>
#include <SoftwareSerial.h>
#include <DFRobot_sim808.h>
#include <Wire.h> 
#include <LiquidCrystal_I2C.h> 
//---------------------------------------------------------------
//        pins
//---------------------------------------------------------------
//dc
#define DC A0
//var
#define SIZE_ID 4
#define SIZE_CAR 9
#define SIZE_PHONE 14
#define SIZE_PWD 5
//LCD
LiquidCrystal_I2C lcd = LiquidCrystal_I2C(0x27, 20, 4);
//SD
File myFile;
int pinCS = 53; 
//MQ3
int analogPin = A2;
//sim
DFRobot_SIM808 sim808(&Serial);
//button
const int buttonPin = 6;     // the number of the pushbutton pin
int button=-1;
bool buttonState= false;

//engie
bool egine = false;
unsigned long time = 0;
unsigned long timeout = 0;
unsigned long time_to_exit = 120000;


//---------------------------------------------------------------
//        func
//---------------------------------------------------------------
//           111111 1111 22222228
//012 3456789012345 6789 01234567
//125 +972525598699 1234 12345678 
//id    phone        pwd    car
//31.95245543217836, 34.90169287913625
struct device
{
    char id[SIZE_ID]="125";//V
    char car_number[SIZE_CAR] = "01234567";//V
    char send_phone[SIZE_PHONE]="+972525598699";//V

    char location_lat[20]="31.95245543217836";
    char location_lng[20]="34.90169287913625";

    int alcohol_level=0;

    char code_save[SIZE_PWD];//V
};


//---------------------------------------------------------------
//        func
//---------------------------------------------------------------
//Mini Fan - DC
void dc_open();
void dc_close();
//LCD
void printToLCD(String str1,String str2,String str3 ,String str4);


//SD
void SD_Read();// Reading the file
void SD_Create(char* msg);//Create/Open file
// resetFunc();  //call reset
void(* resetFunc) (void) = 0; //declare reset function @ address 0
//gps
void displayInfo();
//MQ3
void printAlcohol(int value);
void AlcoholLevelWating();
int readAlcohol();
//sim
void send_sms_drunk();
void read_sms();
