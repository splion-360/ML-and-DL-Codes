char data;
int ledpin=2;
void setup() { 
  Serial.begin(9600);                              
  pinMode(ledpin, OUTPUT);                   
  digitalWrite (ledpin, LOW);                     
}

void loop() {
while (Serial.available()){data = Serial.read();}

if (data == '1'){digitalWrite(ledpin,HIGH);delay(100);}
else if (data == '0'){digitalWrite(ledpin,LOW);delay(100);}

}
