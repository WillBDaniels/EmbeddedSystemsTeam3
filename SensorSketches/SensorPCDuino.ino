/*
Author:          Brian Dignam
Date Created:    3/1/2015
*/


#include "DHT.h"

#include "AirQuality.h"
#include "Arduino.h"

#define DHTPIN A0
#define DHTTYPE DHT11   // DHT 11 
DHT dht(DHTPIN, DHTTYPE);

#define MQ2PIN A3

AirQuality airqualitysensor;
int current_quality =-1;

int TIMESTAMP;

void setupDHT()
{  
  dht.begin();
}

void setup() 
{
    Serial.begin(9600); 
    Serial.println("Serial Connection Established");
    
    airqualitysensor.init(14);  //AC 1.3
    
    TIMESTAMP = 0;
    
    setupDHT();
}

float getHumidity()
{
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  
  float h = dht.readHumidity();
  
  if (!isnan(h))
    return h;
  else
    return 0.0;
    
}

float getTemp()
{
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  
  float t = dht.readTemperature();
  
  if (!isnan(t))
    return t;
  else
    return 0.0;
    
}

float getMQ2Gas()
{
  float vol;
  int sensorValue = analogRead(MQ2PIN);
  vol=(float)sensorValue/1024*5.0;
  //Serial.println(vol,1);
  
  return vol;
}

int getAirQuality1_1()
{
  if(airqualitysensor.counter==122)//set 2 seconds as a detected duty
    {

      airqualitysensor.last_vol=airqualitysensor.first_vol;
      airqualitysensor.first_vol=analogRead(A1);
      airqualitysensor.counter=0;
      airqualitysensor.timer_index=1;
      PORTB=PORTB^0x20;     
    }
      else
    {
      airqualitysensor.counter++;
      return current_quality;
    }
}

/*
//Gas Sensor - MQ5
//Used as reference: http://seeedstudio.com/wiki/Twig_-_Gas_Sensor(MQ5)
float getGasDensity()
{
  float vol;
  int sensorValue = analogRead(A0);
  vol=(float)sensorValue/1024*5.0;
  return vol;
}
*/

void loop() 
{
  Serial.print("Timestamp:  ");
  Serial.println(TIMESTAMP);
  Serial.println();
  delay(500);
  
  Serial.print("Temp:  ");
  Serial.println(getTemp());
  delay(500);
  
  Serial.print("Humidity:  ");  
  Serial.println(getHumidity() );
  delay(500);
  
  /*
  Serial.print("MQ2 Gas:  ");
  Serial.println(getMQ2Gas(),1);
  delay(500);
  */
  
  /*
  //Air Quality v1.1
  Serial.print("Air Quality:  ");
  Serial.println(getAirQuality1_1(),1);
  delay(500);
  */
  
  Serial.println();  
  TIMESTAMP++;
  delay(2000);  //2s
}
