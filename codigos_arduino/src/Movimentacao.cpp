#include "Configuracoes.h"
#include <Servo.h>

Servo servoMotor, esc;

void startTreco() {
  servoMotor.attach(SERVO);
  esc.attach(ESC);
//
  servoMotor.write(anguloCentralServo);
  esc.write(velocidadeParada);
}

void finaliza() {
  esc.write(velocidadeParada);
  servoMotor.write(anguloCentralServo);
}

void setVelocidade(int velocidade) {
  esc.write(velocidade);
}

