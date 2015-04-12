#include <SoftwareSerial.h>


const int pinRx = UART;
const int pinTx = UART;


SoftwareSerial sensor(pinTx,pinRx);


unsigned char flg_get = 0;              // if get sensor data


const unsigned char cmd_get_sensor[] = {
0xff, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79};


bool sendCmdGetDta(int *gas_strength, int *temperature)
{
    for(int i=0; i<sizeof(cmd_get_sensor); i++)
    {
        sensor.write(cmd_get_sensor[i]);
    }
    
    long cnt_timeout = 0;
    while(!sensor.available())              // wait for data
    {
        delay(1);
        cnt_timeout++;
        
        if(cnt_timeout>1000)return 0;       // time out
    }
    
    int len = 0;
    unsigned char dta[20];
    
    while(sensor.available())
    {
        dta[len++] = sensor.read();
    }
    
    if((9 == len) && (0xff == dta[0]) && (0x86 == dta[1]))      // data ok
    {
        *gas_strength = 256*dta[2]+dta[3];
        *temperature = dta[4] - 40;
        
        return 1;
    }
    
    return 0;
   
}

void setup()
{
    Serial.begin(9600);
    sensor.begin(9600);
}


void loop()
{

//        Serial.println("get a 'g', begin to read from sensor!");
        Serial.println("********************************************************");
        Serial.println();
        flg_get = 0;
        int gas, temp;
        
        if(sendCmdGetDta(&gas, &temp))          // get data ok
        {
//            Serial.println("get data ok: ");
            Serial.print("gas_strength = ");
            Serial.println(gas);
//            Serial.print("\ttemperature = ");
//            Serial.println(temp);            
        }
        else 
        {
            Serial.println("get data error");
        }

    
    delay(1000);
}



void serialEvent() 
{
    while (Serial.available()) 
    {
        char c = Serial.read();
        if(c == 'g')flg_get = 1;
        
    }
}

