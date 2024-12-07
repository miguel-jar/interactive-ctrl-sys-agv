#include "Arduino.h"
#include "Configuracoes.h"
#include <Servo.h>

Servo servoMotor, esc;

void startTreco() {
  servoMotor.attach(SERVO);
  esc.attach(ESC);

  servoMotor.write(anguloCentralServo);
  esc.write(velocidadeParada);
}

void frear() {
  //esc.write(velocidadeParada);
  delay(200);
  esc.write(velocidadeFreio);
  delay(1500);
}

void finaliza() {
  esc.write(velocidadeParada);
  servoMotor.write(anguloCentralServo);
}

void setVelocidade(int velocidade) {
  esc.write(velocidade);
}

float pid(float setpoint) {

  float erroRestante = setpoint - getAnguloAtual();

  if (erroRestante > 180.0)
    erroRestante -= 360.0;
  else if (erroRestante < -180.0)
    erroRestante += 360.0;

  // Para as rodas do carrinho estarem alinhadas pra frente, o angulo do servo deve estar em 82, por isso a soma
  float saidaControlador = anguloCentralServo + kp * erroRestante;

  // Limites mecânicos que o servo da direção pode virar
  if (saidaControlador > 122.0)
    saidaControlador = 122.0;
  else if (saidaControlador < 42.0)
    saidaControlador = 42.0;

  servoMotor.write(saidaControlador);

  return erroRestante;
}
