char command;
const int led_red = 3;
const int led_green = 4;

void setup(){
  Serial.begin(9600);
  pinMode(led_red, OUTPUT);
  pinMode(led_green, OUTPUT);
}

void loop(){
  if(Serial.available()> 0){ 
    command = Serial.read();
    if(command == '0')
      digitalWrite(led_red, HIGH);
    else if(command == '1')
      digitalWrite(led_red, LOW);
    else if(command == '2')
      digitalWrite(led_green, HIGH);
    else if(command == '3')
      digitalWrite(led_green, LOW);
  }
}