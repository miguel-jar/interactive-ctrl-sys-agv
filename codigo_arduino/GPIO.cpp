#include "Configuracoes.h"

volatile float distanciaPercorrida1;
volatile float distanciaPercorrida2;

const float circunferenciaRoda = 11.5 * 3.14;  // em CM
const float resolucaoEncoder = 8.0;

bool controlePrescionado() {
  unsigned long tiempo = pulseIn(RF_CH3, HIGH);

  if (tiempo > 1600.0)
    return true;
  else
    return false;
}

void interrupcaoEncoderINT1() {
  distanciaPercorrida1 += circunferenciaRoda / resolucaoEncoder;
}

void interrupcaoEncoderINT2() {
  distanciaPercorrida2 += circunferenciaRoda / resolucaoEncoder;
}

float getDistanciaPercorrida() {
  float distancia = (distanciaPercorrida1 + distanciaPercorrida2) / 2.0;
  //float distancia = distanciaPercorrida2;
  distanciaPercorrida1 = 0.0, distanciaPercorrida2 = 0.0;
  return distancia;
}

void startGPIO() {
  attachInterrupt(digitalPinToInterrupt(ENCODER_INT1), interrupcaoEncoderINT1, RISING);
  attachInterrupt(digitalPinToInterrupt(ENCODER_INT2), interrupcaoEncoderINT2, RISING);

  //pinMode(RF_CH3, INPUT);

  distanciaPercorrida1 = 0.0;
  distanciaPercorrida2 = 0.0;
}
