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
const int velocidadeMovimentacao = 74;
const int velocidadePartida = 70;
const int velocidadeParada = 90;
const int velocidadeFreio = 140;

/* .......................................... Parâmetros PID .......................................... */

const float kp = 2.1;

/* .............................................. Métodos ............................................. */

bool controlePrescionado();
float getDistanciaPercorrida();
void startGPIO();

void startMPU();
float getAnguloAtual();
void setReferenciaAngular();
float setCorrecao(float ref);

void startTreco();
void frear();
void finaliza();
void setVelocidade(int velocidade);

float pid(float setpoint);

extern volatile float distanciaPercorrida1, distanciaPercorrida2;

#endif