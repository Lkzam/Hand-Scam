#include <Servo.h>

Servo servo; // Cria um objeto Servo
unsigned long lastCommandTime = 0; // Armazena o momento do último comando
const unsigned long timeout = 3000; // Tempo limite sem comandos (em milissegundos)

void setup() {
  servo.attach(9); // Conecta o servo ao pino 9
  servo.write(30); // Posição inicial do servo (soltar os cabos)
  Serial.begin(9600); // Inicia a comunicação serial
  lastCommandTime = millis(); // Define o momento inicial
}

void loop() {
  // Verifica se há dados na porta serial
  if (Serial.available() > 0) {
    char comando = Serial.read(); // Lê o comando enviado pelo Python
    lastCommandTime = millis(); // Atualiza o momento do último comando
    
    if (comando == 'F') { // Mão fechada
      if (!servo.attached()) { 
        servo.attach(9); // Reconecta o servo se necessário
      }
      servo.write(120); // Move o servo para 120° (puxar os cabos com força)
    } else if (comando == 'A') { // Mão aberta
      if (!servo.attached()) { 
        servo.attach(9); // Reconecta o servo se necessário
      }
      servo.write(30); // Move o servo para 30° (soltar os cabos suavemente)
    }
  }

  // Verifica se já passou o tempo limite sem comandos
  if (millis() - lastCommandTime > timeout && servo.attached()) {
    servo.detach(); // Desconecta o servo do pino para evitar força desnecessária
  }
}
