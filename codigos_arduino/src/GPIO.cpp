#include <Wire.h>
#include <MPU6050_tockn.h>

MPU6050 mpu(Wire);

void startMPU() {
  Wire.begin();
  mpu.begin();
  mpu.calcGyroOffsets(false);
}

float getAnguloAtual() {
  mpu.update();
  return mpu.getAngleZ(); // anotação (10)
}