#include "Settings.h"

volatile float distanceTraveled1;
volatile float distanceTraveled2;

const float WHEEL_CIRCUMFERENCE = 11.5 * 3.14;  // in CM
const float ENCODER_RESOLUTION = 8.0;

bool isControlPressed() {
  unsigned long pulseTime = pulseIn(RF_CH3, HIGH);

  if (pulseTime > 1600.0)
    return true;
  else
    return false;
}

void encoderInterrupt1() {
  distanceTraveled1 += WHEEL_CIRCUMFERENCE / ENCODER_RESOLUTION;
}

void encoderInterrupt2() {
  distanceTraveled2 += WHEEL_CIRCUMFERENCE / ENCODER_RESOLUTION;
}

float getDistanceTraveled() {
  float distance = (distanceTraveled1 + distanceTraveled2) / 2.0;
  
  // Reset distance counters after reading to calculate delta in the next loop
  distanceTraveled1 = 0.0;
  distanceTraveled2 = 0.0;
  
  return distance;
}

void setupGPIO() {
  attachInterrupt(digitalPinToInterrupt(ENCODER_INT1), encoderInterrupt1, RISING);
  attachInterrupt(digitalPinToInterrupt(ENCODER_INT2), encoderInterrupt2, RISING);

  distanceTraveled1 = 0.0;
  distanceTraveled2 = 0.0;
}