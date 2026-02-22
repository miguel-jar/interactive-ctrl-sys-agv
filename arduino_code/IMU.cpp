#include <Wire.h>
#include <MPU6050_tockn.h>

MPU6050 mpu(Wire);

float referenceAngle, globalReference = 0.0, correction = 0.0;

void setupMPU() {
  Wire.begin();
  mpu.begin();
  mpu.calcGyroOffsets(false);  // Calibrates the gyroscope
  mpu.update();                // Updates sensor data
  referenceAngle = mpu.getAngleZ();  // Sets initial reference angle based on accelerometer
  return;
}

float getCurrentAngle() {
  mpu.update();                                              // Updates sensor data
  return mpu.getAngleZ() - referenceAngle + globalReference + correction;  // Returns corrected angle
}

void setAngularReference() {
  mpu.update();  // Updates sensor data
  globalReference = mpu.getAngleZ();
  return;
}

float setCorrection(float ref) {
  correction = ref;
  return correction;
}