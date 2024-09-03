#include "Arduino.h"
#include "Configuracoes.h"
#include "math.h"
#include <Servo.h>

bool sistemaLigado;

int coordinateX = 360, coordinateY = 0;
int xAtual = 0, yAtual = 0;

void receiveData(void) {
  if (Serial.available() > 4) {
    uint8_t rec = Serial.read();

    if (rec == 0x10) {

      int xx = (Serial.read() << 8) | Serial.read();
      int yy = (Serial.read() << 8) | Serial.read();

      if (sistemaLigado) {
        coordinateX = xx, coordinateY = yy;
        Serial.write(byte(coordinateX >> 8));
        Serial.write(byte(coordinateX));
        Serial.write(byte(coordinateY >> 8));
        Serial.write(byte(coordinateY));
      } else {
        xAtual = xx, yAtual = yy;
        Serial.write(byte(xAtual >> 8));
        Serial.write(byte(xAtual));
        Serial.write(byte(yAtual >> 8));
        Serial.write(byte(yAtual));
      }

    } else if (rec == 0x20) {
      rec = Serial.read();
      rec = Serial.read();
      rec = Serial.read();
      rec = Serial.read();

      if (rec == 112) {
        sistemaLigado = true;
        digitalWrite(LED_BUILTIN, HIGH);
      } else if (rec == 115) {
        sistemaLigado = false;
        digitalWrite(LED_BUILTIN, LOW);
      }
    }
  }
}

void calculeAtualPosition(void) {
  // static float distOld;
  // float dist = getDistanciaPercorrida();
  float angle = PI * getAnguloAtual() / 180.0;

  if (distanciaPercorrida1 > 0) {
    float dist = distanciaPercorrida1;
    distanciaPercorrida1 = 0;

    int x_percorrido = dist * cos(angle);
    int y_percorrido = dist * sin(angle);

    xAtual += x_percorrido;
    yAtual += y_percorrido;

    Serial.write(byte(xAtual >> 8));
    Serial.write(byte(xAtual));
    Serial.write(byte(yAtual >> 8));
    Serial.write(byte(yAtual));
  }
}

float getSetPointAngle(int spX, int spY) {
  float dx = spX - xAtual, dy = spY - yAtual;

  if (dx == 0) {
    if (dy > 0)
      return 90.0;
    else if (dy < 0)
      return -90.0;
    else
      return 0;
  }

  return atan(dy / dx) * 180.0 / PI;

  /*if ((dx > 0) && (dy > 0))
    return atan(dy / dx);

  else if (((dx < 0) && (dy > 0)) || ((dx < 0) && (dy < 0)))
    return atan(dy / dx) + PI;

  else if ((dx > 0) && (dy < 0))
    return atan(dy / dx) + 2 * PI;

  else if (dx == 0) {
    if (dy > 0)
      return PI / 2.0;
    else if (dy < 0)
      return 2 * PI / 3.0;
    else
      return 0;
  }*/
}

void setup() {
  Serial.begin(9600);

  startMPU();
  startTreco();
  startGPIO();

  sistemaLigado = false;  // só liga ao receber as 5 primeiras coordenadas
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  receiveData();

  //Serial.println(getAnguloAtual());

  if (sistemaLigado) {
    setVelocidade(velocidadeMovimentacao);
    calculeAtualPosition();
    float setpointAngulo = getSetPointAngle(coordinateX, coordinateY);
    pid(setpointAngulo);

  } else {
    finaliza();
  }
}
