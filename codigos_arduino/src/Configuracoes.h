#ifndef CONFIGURACOES_H
#define CONFIGURACOES_H

#include <Arduino.h>

/* ............................................. Pinagem .............................................. */

#define ENCODER_INT1 3
#define ENCODER_INT2 2
#define ESC 5
#define RF_CH3 4
#define SERVO 6

/* ............................................ Parâmetros ............................................ */

const float anguloCentralServo = 82.0;
const int velocidadeMovimentacao = 70;
const int velocidadeParada = 90;

/* .......................................... Parâmetros PID .......................................... */

const float kp = 2.2;

/* .............................................. Métodos ............................................. */

bool controlePrescionado();
float getDistanciaPercorrida();
void startGPIO();

void startMPU();
float getAnguloAtual();

void startTreco();
void setVelocidade(int velocidade);
void finaliza();

float pid(float setpoint);

extern volatile float distanciaPercorrida1;

#endif