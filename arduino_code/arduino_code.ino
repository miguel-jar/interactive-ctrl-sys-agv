#include "Arduino.h"
#include "Settings.h"
#include "math.h"
#include <Servo.h>

// Navigation and State Variables
int targetX = 0, targetY = 0;
float currentX = 0.0, currentY = 0.0;
bool isSystemOn = false, stopExecution = false;
float oldAngle, correctionValue = 0.0;
unsigned long lastSerialTime;
float pidOutput;
uint64_t lastLoopTime;

#define TARGET_MARGIN 43.0

void receiveData(void) {
  if (Serial.available() > 4) {
    uint8_t header = Serial.read();

    // 0x10: Update Target Coordinates
    if (header == 0x10) {
      int incomingX = (Serial.read() << 8) | Serial.read();
      int incomingY = (Serial.read() << 8) | Serial.read();

      if (isSystemOn) {
        stopExecution = false;
        targetX = incomingX;
        targetY = incomingY;

        // Soft position adjustment logic
        targetX -= 3.5 * abs(currentX - targetX) / 100.0;
        targetY -= 3.5 * abs(currentY - targetY) / 100.0;

        float setpoint = getSetpointAngle();
        pidOutput = calculatePID(setpoint);
        correctionValue = setCorrection(pidOutput * 25.0 / 180.0);
      } else {
        currentX = incomingX;
        currentY = incomingY;
      }
      lastSerialTime = millis();
    } 
    // 0x20: System Commands (Start/Stop)
    else if (header == 0x20) {
      uint8_t cmd;
      cmd = Serial.read(); // Skip padding
      cmd = Serial.read();
      cmd = Serial.read();
      cmd = Serial.read();

      if (cmd == 112) { // ASCII 'p' for Play
        isSystemOn = true;
        digitalWrite(LED_BUILTIN, HIGH);
      } else if (cmd == 115) { // ASCII 's' for Stop
        isSystemOn = false;
        digitalWrite(LED_BUILTIN, LOW);
      }
    }
  }
}

void calculateCurrentPosition(void) {
  float distance = getDistanceTraveled();

  if (distance > 0.0) {
    // Dead reckoning: updating X and Y based on distance and angle
    float xTraveled = distance * cos(oldAngle);
    float yTraveled = distance * sin(oldAngle);

    currentX += xTraveled;
    currentY += yTraveled;

    // Check if the target coordinates are within the allowed margin
    if ((abs(currentX - targetX) <= TARGET_MARGIN) && (abs(currentY - targetY) <= TARGET_MARGIN)) {
      // Send "Target Reached" signal (32760)
      Serial.write(byte(32760 >> 8));
      Serial.write(byte(32760));
      Serial.write(byte(32760 >> 8));
      Serial.write(byte(32760));
      stopExecution = true;
    } else {
      // Send current telemetry back
      Serial.write(byte(int(currentX) >> 8));
      Serial.write(byte(int(currentX)));
      Serial.write(byte(int(currentY) >> 8));
      Serial.write(byte(int(currentY)));
    }

    // Update angle for the next iteration
    oldAngle = (PI * getCurrentAngle() / 180.0);
  }
}

float getSetpointAngle() {
  float dx = targetX - currentX;
  float dy = targetY - currentY;
  return atan2(dy, dx) * 180.0 / PI;
}

void setup() {
  Serial.begin(115200);

  setupMPU();
  setupActuators();
  setupGPIO();

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

  oldAngle = PI * getCurrentAngle() / 180.0;
  isSystemOn = false;
  stopExecution = false;
  lastLoopTime = millis();
}

void loop() {
  receiveData();

  // Task Scheduler: Executes every 60ms
  if ((millis() - lastLoopTime) > 60) {
    lastLoopTime = millis();

    if (isSystemOn) {
      calculateCurrentPosition();
      float setpoint = getSetpointAngle();
      calculatePID(setpoint);

      if (!stopExecution) {
        // Switch between Cruise and Starting speed based on timeout
        if ((millis() - lastSerialTime) > 1500) {
          setSpeed(CRUISE_SPEED);
        } else {
          setSpeed(START_SPEED);
        }
      } else {
        applyBrake();
        setAngularReference();
        setupMPU();
      }
    } else {
      shutdown();
    }
  }
}