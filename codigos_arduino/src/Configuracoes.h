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
const int velocidadeMovimentacao = 75;
const int velocidadeParada = 90;

/* .......................................... Parâmetros PID .......................................... */

const float kp = 2.1;

/* .............................................. Métodos ............................................. */

void startGPIO();
void interrupcaoEncoderINT1();
void interrupcaoEncoderINT2();
float getDistanciaPercorrida();
bool controlePrescionado();

void startMPU();
float getAnguloAtual();

void startTreco();
void setVelocidade(int velocidade);
void finaliza();

float pid(float setpoint);

extern volatile float distanciaPercorrida1;
extern uint16_t contador;

#endif