#include "Arduino.h"
#include "Configuracoes.h"
#include "math.h"
#include <Servo.h>
// testing git
bool sistemaLigado;
float setpointAngulo;
// branch
extern Servo servoMotor;

#define QUANTITY_OF_POINTS 5
#define ACCEPT_MARGIN 10

int coordinateX = 0, coordinateY = 0;
int actualX, actualY;
uint8_t receivedCoordinates;

void setPID(void);
void receiveData(void);
double getSetPointAngle(int spX, int spY);
void calculeAtualPosition(void);

void setup()
{
  Serial.begin(115200);

  startMPU();
  startTreco();
  startGPIO();

  sistemaLigado = false; // só liga ao receber as 5 primeiras coordenadas
  setpointAngulo = 90.0;

  setVelocidade(velocidadeMovimentacao);

  pinMode(LED_BUILTIN, OUTPUT);
}

void loop()
{
  receiveData();

  // if (controlePrescionado())
  // {
  //   finaliza();
  //   sistemaLigado = false;
  // }
  if (sistemaLigado)
  {
    calculeAtualPosition();
    setPID();
  }
  else
  {
    finaliza();
  }
}

void setPID(void)
{
  float setpoint = getSetPointAngle(coordinateX, coordinateY);

  float erroRestante = setpoint - getAnguloAtual();

  // Para as rodas do carrinho estarem alinhadas pra frente, o angulo do servo deve estar em 82, por isso a soma
  float saidaControlador = anguloCentralServo + kp * erroRestante;

  // Limites mecânicos que o servo da direção pode virar
  if (saidaControlador > 122.0)
    saidaControlador = 122.0;
  else if (saidaControlador < 42.0)
    saidaControlador = 42.0;

  servoMotor.write(saidaControlador);
}

double getSetPointAngle(int spX, int spY)
{
  return atan((spY - actualY) / (spX - actualX));
}

void calculeAtualPosition(void)
{
  // static float distOld; 
  // float dist = getDistanciaPercorrida();
  float angle = getAnguloAtual();

  angle = (angle / 180.0) * 3.14;

  int x_percorrido, y_percorrido;

  if (distanciaPercorrida1 > 0)
  {
    float dist = distanciaPercorrida1;
    distanciaPercorrida1 = 0;

    x_percorrido = dist * sin(angle);
    y_percorrido = dist * cos(angle);

    actualX += x_percorrido;
    actualY += y_percorrido;

    Serial.write(byte(contador >> 8));
    Serial.write(byte(contador));
    Serial.write(byte(actualY >> 8));
    Serial.write(byte(actualY));
  }
}

void receiveData(void)
{
  if (Serial.available() > 4)
  {
    uint8_t rec = Serial.read();

    if (rec == 0x10)
    {
      int pX = ((byte)Serial.read() << 8) | Serial.read();
      int pY = ((byte)Serial.read() << 8) | Serial.read();

      coordinateX = pX;
      coordinateY = pY;
      Serial.write(byte(coordinateX >> 8));
      Serial.write(byte(coordinateX));
      Serial.write(byte(coordinateY >> 8));
      Serial.write(byte(coordinateY));
    }
    else if (rec == 0x20)
    {
      rec = Serial.read();
      rec = Serial.read();
      rec = Serial.read();
      rec = Serial.read();

      if (rec == 112)
      {
        sistemaLigado = true;
        digitalWrite(LED_BUILTIN, HIGH);
      }
      else if (rec == 115)
      {
        sistemaLigado = false;
        digitalWrite(LED_BUILTIN, LOW);
      }
    }
  }
}
