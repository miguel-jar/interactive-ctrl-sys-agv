#ifndef CONFIGURACOES_H
#define CONFIGURACOES_H

#include <Arduino.h>

/* ............................................. Pinagem .............................................. */

#define ENCODER_INT1 3
#define ESC 5
#define RF_CH3 6
#define SERVO 9
#define BUZZER A3

/* ............................................ Parâmetros ............................................ */

const float anguloCentralServo = 82.0;
const int velocidadeMovimentacao = 59;
const int velocidadeParada = 90;

/* .......................................... Parâmetros PID .......................................... */

const float kp = 2.1;

/* .............................................. Métodos ............................................. */

void startGPIO();
void tocaBuzzer();
void interrupcaoEncoderINT1();
float getDistanciaPercorrida();
bool controlePrescionado();

void startMPU();
float getAnguloAtual();

void startTreco();
void setVelocidade(int velocidade);
void finaliza();

float pid(float setpoint);

#endif
