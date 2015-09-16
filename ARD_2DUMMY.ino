
#include <Servo.h> 
#include "math.h"
int yellowPin = 2;
int redPin = 7;                  
int greenPin = 11; 
int temp;
int  ldrvalue;
int moisvalue;
String readString, servo1,servo2;
Servo myservo1; 
void setup() 
{
   Serial.begin(9600);           
   pinMode(redPin, OUTPUT);       
   pinMode(greenPin, OUTPUT);      
   pinMode(yellowPin, OUTPUT);
   myservo1.attach(6);
   while(!Serial)
   {
    ;
    }
}
void loop() 
{ 
   while (Serial.available()) 
     {
       delay(3);  //delay to allow buffer to fill 
       if(Serial.available()>0)
         {
           char c= Serial.read();
           readString += c;
        }
    }
  if(readString.length() >0)
     {
        //Serial.println(readString);
        servo1= readString.substring(0,1);
        servo2= readString.substring(1,6);
        Serial.println(servo1);
        Serial.println(servo2);
        if(servo1 == "T")
          {
            temp=servo2.toInt();
            temp=abs(temp);
            for (int i=0;i<=temp;i++)
             {
                 digitalWrite(yellowPin, HIGH);
                 delay(100);
                 digitalWrite(yellowPin, LOW);
                 delay(100);
             }
         }
       else if(servo1 == "L")
         {
             ldrvalue=servo2.toInt();
             ldrvalue=abs(ldrvalue);
             for (int i=0;i<=ldrvalue;i++)
               {
                 digitalWrite(redPin, HIGH);
                 delay(100);
                 digitalWrite(redPin, LOW);
                 delay(100);
              }
       }
      else if(servo1 == "H")
         {
             moisvalue=servo2.toInt();
             moisvalue=abs(moisvalue);
            for (int i=0;i<=moisvalue;i++)
              {
                 digitalWrite(greenPin, HIGH);
                 delay(100);
                 digitalWrite(greenPin, LOW);
                 delay(100);
              }
       } 
    }            
  readString="";      
}    
