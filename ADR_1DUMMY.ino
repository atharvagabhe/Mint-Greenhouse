int kelvin;
int temp;
int celcius;
int ldrvalue;
int moisvalue;
float humi;
float prehum;
float humconst;
int relativehum;
float pretruehum;
int pretruehumconst;
int humidity;

int tempPin=0;
int ldrPin=2;
int moisPin=4;
String stringone, stringtwo, stringthree, stringcelcius, stringlight, stringmois;
void setup() 
{
  // put your setup code here, to run once:
   pinMode (tempPin, temp);
   analogWrite(0,temp);
   pinMode (ldrPin, ldrvalue);
   analogWrite(2,ldrvalue);
   pinMode (moisPin, moisvalue);
   analogWrite(4,moisvalue);
   Serial.begin(9600);
   stringone=String("T");
   stringtwo=String("L");
   stringthree=String("H");
   stringcelcius=String();
   stringlight=String();
   stringmois=String();

}

void loop() 
{
  if(Serial.available()>0)
     {
      char select =Serial.read();
       if(select == 'T')
        {
        temp=analogRead(tempPin);
        kelvin=(5.0*temp*100)/1024.0;
        celcius=kelvin-267;
        stringcelcius=stringone+ celcius;
        Serial.println(stringcelcius);
        delay(100);
         }
       else if(select == 'L')
       {
         ldrvalue=analogRead(ldrPin);
         stringlight=stringtwo+ analogRead(ldrPin);
         Serial.println(stringlight);
         delay(100);
          }
       else if(select == 'H')
       {
          moisvalue=analogRead(moisPin);
          prehum = (moisvalue/5);
          humconst = (0.16/0.0062);
          humi = (prehum - humconst);
          pretruehumconst = 0.00216*celcius;
          pretruehum = 1.0546-pretruehumconst;
          relativehum = humi/pretruehum ;
          humidity=220.0-relativehum;
 

          stringmois=stringthree+ humidity;
          Serial.println(stringmois);
          delay(100);
              }
 
     }
 } 
  
 
        
 







