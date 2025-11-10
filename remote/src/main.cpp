#include <Arduino.h>
#include <IRremote.hpp>

void setup() {
  pinMode(13, OUTPUT); //Green (POWER MODE)
  pinMode(12, OUTPUT); //Blue (SIGNAL LIGHT)

  digitalWrite(13, HIGH); //POWER ON
}

void loop() {
  digitalWrite(12, HIGH); //SIGNAL LIGHT ON

}