#include "Configuracoes.h"

volatile float distanciaPercorrida;

bool controlePrescionado() {
  unsigned long tiempo = pulseIn(RF_CH3, HIGH);

  if (tiempo > 1600.0)
    return true;
  else
    return false;
}

void interrupcaoEncoderINT1() {
  const float circunferenciaRoda = 11.5 * 3.14;  // em CM
  const float resolucaoEncoder = 8.0;
  distanciaPercorrida += circunferenciaRoda / resolucaoEncoder;
}

float getDistanciaPercorrida() {
  return distanciaPercorrida;
}

void startGPIO() {

  attachInterrupt(digitalPinToInterrupt(ENCODER_INT1), interrupcaoEncoderINT1, RISING);

  pinMode(RF_CH3, INPUT);
  pinMode(BUZZER, OUTPUT);
  digitalWrite(BUZZER, LOW);

  distanciaPercorrida = 0.0;
}

void tocaBuzzer() {
  digitalWrite(BUZZER, HIGH);
  delay(200);
  digitalWrite(BUZZER, LOW);
}
