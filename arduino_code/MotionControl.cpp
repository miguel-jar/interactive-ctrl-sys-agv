#include "Arduino.h"
#include "Settings.h"
#include <Servo.h>

Servo steeringServo, motorEsc;

void setupActuators() {
  steeringServo.attach(SERVO);
  motorEsc.attach(ESC);

  steeringServo.write(SERVO_CENTER_ANGLE);
  motorEsc.write(STOP_SPEED);
}

void applyBrake() {
  // motorEsc.write(STOP_SPEED);
  delay(200);
  motorEsc.write(BRAKE_SPEED);
  delay(1500);
}

void shutdown() {
  motorEsc.write(STOP_SPEED);
  steeringServo.write(SERVO_CENTER_ANGLE);
}

void setSpeed(int speed) {
  motorEsc.write(speed);
}

float calculatePID(float setpoint) {

  float remainingError = setpoint - getCurrentAngle();

  // Normalize error between -180 and 180 degrees
  if (remainingError > 180.0)
    remainingError -= 360.0;
  else if (remainingError < -180.0)
    remainingError += 360.0;

  // Steering alignment: the servo must be at the center angle for the wheels to be straight
  float controllerOutput = SERVO_CENTER_ANGLE + KP * remainingError;

  // Mechanical limits for the steering servo
  if (controllerOutput > 122.0)
    controllerOutput = 122.0;
  else if (controllerOutput < 42.0)
    controllerOutput = 42.0;

  steeringServo.write(controllerOutput);

  return remainingError;
}