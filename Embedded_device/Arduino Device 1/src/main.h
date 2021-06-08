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
//keyboard 
#if defined(ARDUINO_ARCH_AVR)
#define SERIAL Serial
SoftwareSerial mySerial(A10,A11);
#define TRANS_SERIAL  mySerial
#elif defined(ARDUINO_ARCH_SAMD)
#define SERIAL SerialUSB
#define TRANS_SERIAL  Serial
#else
#endif
//dc
#define DC A0
//var
#define SIZE_ID 4
#define SIZE_CAR 9
#define SIZE_PHONE 14
#define SIZE_PWD 5
#define TIME 120000
//LCD
LiquidCrystal_I2C lcd = LiquidCrystal_I2C(0x27, 20, 4);
//SD
File myFile;
int pinCS = 53; 
//MQ3
int analogPin = A2;
//sim
DFRobot_SIM808 sim808(&Serial);

const int try_code_max = 3;
const int waiting = 1;//min


//var 
bool check;

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
    char id[SIZE_ID]="130";//V
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
void send_sms_max_code();
void read_sms();
//keyboard
void pwd_print(int i);
void keyboard_code();
bool check_code();
void clean_code();
//
void button();
void button_off();