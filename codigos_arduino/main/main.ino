#include "Configuracoes.h"

bool sistemaLigado;
float setpointAngulo;

void setup() {

  Serial.begin(9600);

  while (Serial.available() > 0)  // limpa buffer da serial
    Serial.read();

  startMPU();
  startTreco();
  startGPIO();

  sistemaLigado = true,
  setpointAngulo = 90.0;

  tocaBuzzer();
  setVelocidade(velocidadeMovimentacao);
}

void loop() {

  if (controlePrescionado()) {
    finaliza();
    sistemaLigado = false;
  }

  else if (sistemaLigado) {
    float pv = pid(setpointAngulo);
  }
}
