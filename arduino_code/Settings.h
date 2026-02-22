#ifndef SETTINGS_H
#define SETTINGS_H

#include <Arduino.h>

/* ............................................. Pinout .............................................. */

#define ENCODER_INT1 3
#define ENCODER_INT2 2
#define ESC 5
#define RF_CH3 4
#define SERVO 6

/* ............................................ Parameters ............................................ */

const float SERVO_CENTER_ANGLE = 82.0;
const int CRUISE_SPEED = 74;
const int START_SPEED = 70;
const int STOP_SPEED = 90;
const int BRAKE_SPEED = 140;

/* .......................................... PID Parameters .......................................... */

const float KP = 2.1;

/* .............................................. Methods ............................................. */

bool isControlPressed();
float getDistanceTraveled();
void setupGPIO();

void setupMPU();
float getCurrentAngle();
void setAngularReference();
float setCorrection(float ref);

void setupActuators();
void applyBrake();
void shutdown();
void setSpeed(int speed);

float calculatePID(float setpoint);

// External variables for encoder tracking
extern volatile float distanceTraveled1, distanceTraveled2;

#endif