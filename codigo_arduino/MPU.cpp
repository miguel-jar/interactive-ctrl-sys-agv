#include <Wire.h>
#include <MPU6050_tockn.h>

MPU6050 mpu(Wire);

float refAngle, refGlobal = 0.0, correcao = 0.0;

void startMPU() {
  Wire.begin();
  mpu.begin();
  mpu.calcGyroOffsets(false);  // Calibra o giroscópio
  mpu.update();                // Atualiza os dados do sensor
  refAngle = mpu.getAngleZ();  // Define o ângulo de referência inicial baseado no acelerômetro
  return;
}

float getAnguloAtual() {
  mpu.update();                                              // Atualiza os dados do sensor
  return mpu.getAngleZ() - refAngle + refGlobal + correcao;  // Retorna o ângulo corrigido
}

void setReferenciaAngular() {
  mpu.update();  // Atualiza os dados do sensor
  refGlobal = mpu.getAngleZ();
  return;
}
float setCorrecao(float ref) {
  correcao = ref;
  return correcao;
}