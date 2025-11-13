#include <Arduino.h>
#include <IRremote.h>

#define IR_PIN 3

void setup() {
  pinMode(13, OUTPUT); // Green (POWER MODE)
  pinMode(12, OUTPUT); // Blue (SIGNAL LIGHT)

  Serial.begin(9600);
  IrReceiver.begin(IR_PIN, ENABLE_LED_FEEDBACK);
  Serial.println("IR Receiver ready");
}

void loop() {
  digitalWrite(13, HIGH); // POWER ON

  if (IrReceiver.decode()) {
    uint8_t cmd = IrReceiver.decodedIRData.command;

    // Ignore repeat and noise signals
    if (IrReceiver.decodedIRData.flags != IRDATA_FLAGS_IS_REPEAT && cmd != 0) {
      // Serial.print("Command: ");
      // Serial.print(cmd, HEX);
      // Serial.print(" → ");

      // ---- Command Mappings ----
      if (cmd == 0x5A) {             // Example command for NEXT
        Serial.println("NEXT");
      } 
      else if (cmd == 0x8) {        // Example command for BACK
        Serial.println("PREVIOUS");
      } 
      else if (cmd == 0x45) {        // Example command for PLAY/PAUSE
        Serial.println("START");
      } 
      else if (cmd == 0x46) {        // Example command for STOP
        Serial.println("END");
      } 
      else if (cmd == 0x47) {        // Example command for POWER OFF
        Serial.println("BLACK");
      } else if (cmd == 0x44) {        // Example command for VOLUME UP
        Serial.println("WHITE");
      } else if (cmd == 0x18) {        // Example command for VOLUME DOWN
        Serial.println("UP");
      } else if (cmd == 0x52) {        // Example command for MUTE
        Serial.println("DOWN");
      } else if (cmd == 0x1C) {         // Example command for MENU
        Serial.println("APP");
      }
      else {
        Serial.println("UNKNOWN");
      }

      // Blink signal LED
      digitalWrite(12, HIGH);
      delay(150);
      digitalWrite(12, LOW);
    }

    IrReceiver.resume(); // Ready for next signal
  }
}
