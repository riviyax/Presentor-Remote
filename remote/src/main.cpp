#include <Arduino.h>
#include <IRremote.h>

#define IR_PIN 3
#define POWER_LED 10   // any free pin
#define SIGNAL_LED 12

void setup() {
  pinMode(POWER_LED, OUTPUT); // Green (POWER MODE)
  pinMode(SIGNAL_LED, OUTPUT); // Blue (SIGNAL LIGHT)

  digitalWrite(POWER_LED, HIGH); // POWER ON

  Serial.begin(9600);
  IrReceiver.begin(IR_PIN, ENABLE_LED_FEEDBACK);
  Serial.println("IR Receiver ready");
}

void loop() {
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
      else if (cmd == 0x19){
        Serial.println("PAUSE");
      }
      else if (cmd == 0x16) {
        Serial.println("EXIT");
      }
      else if (cmd == 0xD) {
        Serial.println("TASK");
      }
      else {
        Serial.println("UNKNOWN");
      }

      // Blink signal LED
      digitalWrite(SIGNAL_LED, HIGH);
      delay(150);
      digitalWrite(SIGNAL_LED, LOW);
    }

    IrReceiver.resume(); // Ready for next signal
  }
}
