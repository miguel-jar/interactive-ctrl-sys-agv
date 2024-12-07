#include "Arduino.h"
#include "Configuracoes.h"
#include "math.h"
#include <Servo.h>

int coordinateX = 0, coordinateY = 0;
float xAtual = 0.0, yAtual = 0.0;
bool sistemaLigado, stop_exec;
float angle_old, cc = 0.0;
unsigned long tempo;
float retornoPID;
uint64_t tempo1;

#define MARGIN 43.0

void receiveData(void) {
  if (Serial.available() > 4) {
    uint8_t rec = Serial.read();

    if (rec == 0x10) {
      int xx = (Serial.read() << 8) | Serial.read();
      int yy = (Serial.read() << 8) | Serial.read();

      if (sistemaLigado) {
        stop_exec = false;
        coordinateX = xx, coordinateY = yy;
        coordinateX -= 3.5 * abs(xAtual - coordinateX) / 100.0;
        coordinateY -= 3.5 * abs(yAtual - coordinateY) / 100.0;

        float setpoint = getSetpointAngle();  // - correcao;z
        retornoPID = pid(setpoint);
        cc = setCorrecao(retornoPID * 25.0 / 180.0);
        
      } else {
        xAtual = xx, yAtual = yy;
      }

      tempo = millis();
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
  float dist = getDistanciaPercorrida();

  if (dist > 0.0) {
    float x_percorrido = dist * cos(angle_old);
    float y_percorrido = dist * sin(angle_old);

    xAtual += x_percorrido;
    yAtual += y_percorrido;

    // Serial.println("Dist: " + String(dist));
    // Serial.println(String(xAtual) + " - " + String(yAtual));
    // Serial.println();

    if ((abs(xAtual - coordinateX) <= MARGIN) && (abs(yAtual - coordinateY) <= MARGIN)) {
      Serial.write(byte(32760 >> 8));
      Serial.write(byte(32760));
      Serial.write(byte(32760 >> 8));
      Serial.write(byte(32760));
      stop_exec = true;
    } else {
      Serial.write(byte(int(xAtual) >> 8));
      Serial.write(byte(int(xAtual)));
      Serial.write(byte(int(yAtual) >> 8));
      Serial.write(byte(int(yAtual)));
    }

    angle_old = (PI * getAnguloAtual() / 180.0);  // + correcao;
  }
}

float getSetpointAngle() {
  float dx = coordinateX - xAtual;
  float dy = coordinateY - yAtual;
  return atan2(dy, dx) * 180.0 / PI;
}

void setup() {
  Serial.begin(115200);

  startMPU();
  startTreco();
  startGPIO();

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

  angle_old = PI * getAnguloAtual() / 180.0;
  sistemaLigado = false, stop_exec = false;  // só liga ao receber as 5 primeiras coordenadas
  tempo1 = millis();
}

void loop() {
  receiveData();

if((millis() - tempo1) > 60)
{
  tempo1 = millis();
  if (sistemaLigado) {
    calculeAtualPosition();
    float setpoint = getSetpointAngle();  // - correcao;
    pid(setpoint);

    if (!stop_exec) {
      if ((millis() - tempo) > 1500) {
        setVelocidade(velocidadeMovimentacao);
      } else {
        setVelocidade(velocidadePartida);
      }
    } else {
      frear();
      setReferenciaAngular();
      startMPU();
    }
  } else {
    finaliza();
  }
}
}
