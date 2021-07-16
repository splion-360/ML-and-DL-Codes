#include<Firmata.h>
#include<LiquidCrystal.h>
LiquidCrystal lcd(12,11,5,4,3,2);
int lastline = 1;
void stringCallback(char *mystring){

if(lastline){

  lastline = 0;
  lcd.clear();
}
else{
 lastline = 1; 
}
lcd.setCursor(0,1);
lcd.print(mystring);
}

void setup() {
  // put your setup code here, to run once:
  
lcd.begin(16,2);
Firmata.setFirmwareVersion(FIRMATA_MAJOR_VERSION,FIRMATA_MINOR_VERSION);
Firmata.attach(STRING_DATA,stringCallback);
Firmata.begin();

}

void loop() {
  // put your main code here, to run repeatedly:
lcd.setCursor(0,0);
lcd.print("Emotion : ");
while(Firmata.available()){

  Firmata.processInput();
}

}
