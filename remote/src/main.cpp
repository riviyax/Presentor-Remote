#include <Arduino.h>
#include <IRremote.h>

#define IR_PIN 3
#define POWER_LED 10
#define SIGNAL_LED 12

unsigned long signalLedTimer = 0;
const unsigned long signalLedDuration = 100; // LED blink duration

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
    uint8_t flags = IrReceiver.decodedIRData.flags;

    // Only process if it's NOT a repeat and command is valid
    if (cmd != 0 && !(flags & IRDATA_FLAGS_IS_REPEAT)) {
      switch(cmd) {
        case 0x5A: Serial.println("NEXT"); break;
        case 0x08: Serial.println("PREVIOUS"); break;
        case 0x45: Serial.println("START"); break;
        case 0x46: Serial.println("END"); break;
        case 0x47: Serial.println("BLACK"); break;
        case 0x44: Serial.println("WHITE"); break;
        case 0x18: Serial.println("UP"); break;
        case 0x52: Serial.println("DOWN"); break;
        case 0x1C: Serial.println("APP"); break;
        case 0x19: Serial.println("PAUSE"); break;
        case 0x16: Serial.println("EXIT"); break;
        case 0x0D: Serial.println("TASK"); break;
        default: Serial.println("UNKNOWN"); break;
      }

      // Blink signal LED
      digitalWrite(SIGNAL_LED, HIGH);
      signalLedTimer = millis();
    }

    IrReceiver.resume(); // Ready for next signal
  }

  // Turn off LED after duration
  if (digitalRead(SIGNAL_LED) == HIGH && millis() - signalLedTimer >= signalLedDuration) {
    digitalWrite(SIGNAL_LED, LOW);
  }
}
