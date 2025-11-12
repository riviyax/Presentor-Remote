#include <Arduino.h>
#include <IRremote.hpp>

void setup() {
  pinMode(13, OUTPUT); //Green (POWER MODE)
  pinMode(12, OUTPUT); //Blue (SIGNAL LIGHT)

  digitalWrite(13, HIGH); //POWER ON

  Serial.begin(9600);
  IrReceiver.begin(11, ENABLE_LED_FEEDBACK); //IR RECEIVER ON
}

void loop() {
  digitalWrite(12, HIGH); //SIGNAL LIGHT ON

  Serial.println("PREVIOUS");

}