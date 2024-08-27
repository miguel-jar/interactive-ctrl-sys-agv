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

// float pid(float setpoint) {

//   float pv = getAnguloAtual();
//   float erroRestante = setpoint - getAnguloAtual();

//   // Para as rodas do carrinho estarem alinhadas pra frente, o angulo do servo deve estar em 82, por isso a soma
//   float saidaControlador = anguloCentralServo + kp * erroRestante;

//   // Limites mecânicos que o servo da direção pode virar
//   if (saidaControlador > 122.0)
//     saidaControlador = 122.0;
//   else if (saidaControlador < 42.0)
//     saidaControlador = 42.0;

//   servoMotor.write(saidaControlador);

//   return pv;
// }