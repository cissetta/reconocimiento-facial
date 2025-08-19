#include <Servo.h>

Servo servo;
int boton = 7;
int ledVerde = 4;
int ledRojo = 2;

int estado=0;

void setup() {
  Serial.begin(9600);
  servo.attach(9);
  pinMode(boton, INPUT_PULLUP);
  pinMode(ledVerde, OUTPUT);
  pinMode(ledRojo, OUTPUT);
  servo.write(0); // puerta cerrada
  digitalWrite(ledVerde, HIGH);
  digitalWrite(ledRojo, HIGH);


}

void loop() {
  // Botón como "timbre"
  if (digitalRead(boton) == LOW) {
    delay(500);
    Serial.println("ESPERANDO");  // Avisar a Python
    estado=0;
  }
  else
  {  delay(500);
    Serial.println("CAPTURAR");  // Avisar a Python
    estado=1;
}

  // Esperar respuesta de Python
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');

    if (comando == "OPEN") {
      digitalWrite(ledVerde, HIGH);
      digitalWrite(ledRojo, LOW);
      Serial.println("ACCESO OPEN");
      servo.write(90);   // abrir puerta
      delay(5000);
      servo.write(0);    // cerrar puerta
      digitalWrite(ledVerde, LOW);
    }
    if (comando == "DENY") {
      Serial.println("DENEGADO");
      digitalWrite(ledRojo, HIGH);
      digitalWrite(ledVerde, LOW);
      delay(5000);
      digitalWrite(ledRojo, LOW);
    }
  }
}
