#include <Ping.h>
#include "PinChangeInterrupt.h"
#include "motorControl.h"
 
/* programa que calcula la Velocidad del motor en Radianes por segundo.
 * 
 * En este programa se puede seleccionar cualquier motor por medio de la 
 * variable motorControlado.*/
// VARIABLES ULTRA SONIDO
Ping US1 = Ping(24);
Ping US2 = Ping(22);
// VARIABLES SENSOR SHARP
int sharp = A2;
float lectura, DSHR;

int piso = 25;
volatile int S_piso;

// VARIABLES Y CONSTANTES
int i;
int pinBateria = A1;
const int R = 1440;     // Resolución del encoder R = mH * s * r
const double ConstRad = (2*PI*1000)/(R); // 4.363323; // 2*pi*1000/1440 

// Tiempo de muestreo
unsigned long lastTime, sampleTime = 100;

// Instancia de objeto motor
motorControl motor0 (sampleTime);
motorControl motor1 (sampleTime);
motorControl motor2 (sampleTime);

// COMUNICACION SERIAL
String inputString = "";
boolean stringComplete = false;
const char separator = ',';
const int dataLenght = 3;// aumentar el rango
float data[dataLenght] = {0.0,0.0,0.0};//agregar a 6

// motor 0
int PWM0 = 7;
int DIR0 = 10;
int outValue0 = 0;

int EN0A = A10;  
int EN0B = A11;
volatile int n0 = 0;
volatile int ant0 = 0;
volatile int act0 = 0;

double w0 = 0.0;
double wRef0 = 0.0;

// motor 1
int PWM1 = 8;
int DIR1 = 11;

int EN1A = A12;  
int EN1B = A13;
int outValue1 = 0;
volatile int n1 = 0;
volatile int ant1 = 0;
volatile int act1 = 0;

double w1 = 0.0;
double wRef1 = 0.0;

// motor 2
int PWM2 = 9;
int DIR2 = 12;

int EN2A = A14;  
int EN2B = A15;
int outValue2 = 0;
volatile int n2 = 0;
volatile int ant2 = 0;
volatile int act2 = 0;

double w2 = 0.0;
double wRef2 = 0.0;

//////////////////////////////////////////////////////////////////////////
//int motorControlado = 0;///////////////////////////////////////////////////

// MOTORES
int motores[3] = {12, 48, 192};
/*{{PWM0, DIR0, EN0A, EN0B, 12},
 {PWM1, DIR1, EN1A, EN1B, 48},
 {PWM2, DIR2, EN2A, EN2B, 192}};
*/
void serialEvent(){
  while(Serial.available()){
    char inChar = (char)Serial.read();
    inputString += inChar;
    if(inChar == '\n') stringComplete = true;
  }
}

void ISR_sensor_piso(){ 
  S_piso = !S_piso;
}

///++//+////+/ 
double ufRobot = 0;
double ulRobot = 0;
double wRobot = 0;
double phi = 0;
double Radio = 0.0508; // 4" de diametro entre 2 para el radio
double L = 0.15; //15cm

void setup(){

 /* REGLAS DE AJUSTE FINO
  *  Aumentando la ganancia proporcional disminuye la estabilidad
  *  Disminuyendo el tiempo de integración el error decae mas rápido
  *  Disminuyendo el tiempo de integración disminuye la estabilidad
  *  Aumentando el tiempó derivativo mejora la estabilidad.
 */
  //double GainKp = 0.345, GainTi = 0.415, GainTd = 0.9275; // Valores de Modelo Cinemático
  //double GainKp = 0.125, GainTi = 0.201, GainTd = 0.211; // Valores de ajuste Phi
  double GainKp = 0.0125, GainTi = 0.202, GainTd = 0.415; // Valores de ajuste Phi


  Serial.begin(9600);  
     
  motor0.setGains(GainKp, GainTi, GainTd ); // parametros lambda: 0.17, 1.20, 0.12
  motor0.setCvLimits(0,255);
  motor0.setPvLimits (16,0); //max =15.9 ,min 0.80
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(EN0A), encoder0, CHANGE);
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(EN0B), encoder0, CHANGE);

  motor1.setGains(GainKp, GainTi, GainTd); // parametros lambda: 0.17, 1.20, 0.12
  motor1.setCvLimits(0,255);
  motor1.setPvLimits (16,0); //max = 15.9 ,min 0.80
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(EN1A), encoder1, CHANGE);
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(EN1B), encoder1, CHANGE);

  motor2.setGains(GainKp, GainTi, GainTd); // parametros lambda: 0.17, 1.20, 0.12
  motor2.setCvLimits(0,255);
  motor2.setPvLimits (16,0); //max = 15.9 ,min 0.80
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(EN2A), encoder2, CHANGE);
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(EN2B), encoder2, CHANGE);
  
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(piso), ISR_sensor_piso, CHANGE);
  

  

	for (i = A10; i<=A15; i++)pinMode(i, INPUT); // Pines de encoder como entradas
	for (i = 7; i <= 12; i++)pinMode(i, OUTPUT); 	// Señales  PWM y dirección como salidas
// motores apagados y dirección horaria
	for (i = 7; i <= 9; i++){analogWrite(i, 255); digitalWrite(i+3, LOW);} // Apagar motores
	
	lastTime = millis();
}

void loop(){
  bateria();
  attachInterrupt(0 , ISR_sensor_piso, RISING);
  if (stringComplete){
    for (int i = 0; i < dataLenght; i++){
      int index = inputString.indexOf(separator);
      data[i] = inputString.substring(0, index).toFloat();
      inputString = inputString.substring(index + 1);   
    }

   velocityMotor (data[0],data[1],data[2]);
    
    //wRef0 = data[0];
    //wRef1 = data[1];
    //wRef2 = data[2];
 
    inputString = "";
    stringComplete = false;
  }

  if(millis()-lastTime >= sampleTime){
    w0 = (ConstRad*n0)/(millis()-lastTime);
    w1 = (ConstRad*n1)/(millis()-lastTime);
    w2 = (ConstRad*n2)/(millis()-lastTime);
    
    lastTime = millis();        
    n0 = 0;
    n1 = 0;
    n2 = 0;
    velocityRobot (w2, w1, w0); // w0 y w2 se deben ajustar a la matriz 

    phi = phi + wRobot*0.1;
    
    
    //Serial.print("V. Frontal: ");
    Serial.println(ufRobot, 2);
    //Serial.println(outValue0, 2);
    //Serial.println("\tV. Lateral: ");
    Serial.println(ulRobot,2);
    //Serial.println(outValue1, 2);
    //Serial.println("\t V. angular: ");
    Serial.println(wRobot,2);
    //Serial.println(outValue1, 2);

    ultrasonido();
    sensor_sharp();
    Serial.println(S_piso);  

    
    outValue0 = motor0.compute(wRef0, w0);
    outValue1 = motor1.compute(wRef1, w1);
    outValue2 = motor2.compute(wRef2, w2);
    
    //elector de sentido de giro, velocidad y frenado
    wRef0 > 0 ? digitalWrite(DIR0, HIGH), analogWrite(PWM0, outValue0): digitalWrite(DIR0, LOW), analogWrite(PWM0, abs(outValue0));
    wRef1 > 0 ? digitalWrite(DIR1, HIGH), analogWrite(PWM1, outValue1): digitalWrite(DIR1, LOW), analogWrite(PWM1, abs(outValue1));
    wRef2 > 0 ? digitalWrite(DIR2, HIGH), analogWrite(PWM2, outValue2): digitalWrite(DIR2, LOW), analogWrite(PWM2, abs(outValue2));
    if(w0<0 &&  wRef0 == 0) digitalWrite(DIR0, HIGH) ;
    if(w1<0 &&  wRef1 == 0) digitalWrite(DIR1, HIGH) ;
    if(w2<0 &&  wRef2 == 0) digitalWrite(DIR2, HIGH) ;
    //limpiador de buffer
    motor0.reset();
    motor1.reset();
    motor2.reset();

  }
}

void encoder0(){
	ant0 = act0;
	act0 = PINK & motores[0];
	
	if(ant0 == motores[0]*0 && act0 == motores[0]/3) n0--;
	else if(ant0 == motores[0]/3 && act0 == motores[0]/1) n0--;
	else if(ant0 == motores[0]/1.5 && act0 == motores[0]*0) n0--;
	else if(ant0 == motores[0]/1 && act0 == motores[0]/1.5) n0--;
	
	if(ant0 == motores[0]*0 && act0 == motores[0]/1.5) n0++;
	else if(ant0 == motores[0]/3 && act0 == motores[0]*0) n0++;
	else if(ant0 == motores[0]/1.5 && act0 == motores[0]/1) n0++;
	else if(ant0 == motores[0]/1 && act0 == motores[0]/3) n0++;
}

void encoder1(){
  ant1 = act1;
  act1 = PINK & motores[1];
  
  if(ant1 == motores[1]*0 && act1 == motores[1]/3) n1--;
  else if(ant1 == motores[1]/3 && act1 == motores[1]/1) n1--;
  else if(ant1 == motores[1]/1.5 && act1 == motores[1]*0) n1--;
  else if(ant1 == motores[1]/1 && act1 == motores[1]/1.5) n1--;
  
  if(ant1 == motores[1]*0 && act1 == motores[1]/1.5) n1++;
  else if(ant1 == motores[1]/3 && act1 == motores[1]*0) n1++;
  else if(ant1 == motores[1]/1.5 && act1 == motores[1]/1) n1++;
  else if(ant1 == motores[1]/1 && act1 == motores[1]/3) n1++;
}

void encoder2(){
  ant2 = act2;
  act2 = PINK & motores[2];
  
  if(ant2 == motores[2]*0 && act2 == motores[2]/3) n2--;
  else if(ant2 == motores[2]/3 && act2 == motores[2]/1) n2--;
  else if(ant2 == motores[2]/1.5 && act2 == motores[2]*0) n2--;
  else if(ant2 == motores[2]/1 && act2 == motores[2]/1.5) n2--;
  
  if(ant2 == motores[2]*0 && act2 == motores[2]/1.5) n2++;
  else if(ant2 == motores[2]/3 && act2 == motores[2]*0) n2++;
  else if(ant2 == motores[2]/1.5 && act2 == motores[2]/1) n2++;
  else if(ant2 == motores[2]/1 && act2 == motores[2]/3) n2++;
}

void ultrasonido(){
  US1.fire();
  Serial.println(US1.centimeters());
  US2.fire();
  Serial.println(US2.centimeters());/*distancia = duracion(t) * velocidad del sonido(cm/us)*/
}

void sensor_sharp(){
  lectura = analogRead(sharp);
  DSHR = pow(3027.4/lectura, 1.2134); /*eleva el resultado a una constante para obtener la medida en cm*/
  Serial.println(DSHR);
}

void bateria(){
  double voltaje ;
  voltaje = analogRead(pinBateria) * (18.65/1023.0);
  if(voltaje < 11.0){
    digitalWrite(13, LOW);
    //Serial.println("\t\t\t\tBateria baja");
  }else{
    digitalWrite(13, HIGH);
    //Serial.print("\t\t\t\tVoltaje=  ");
    //Serial.println(voltaje);
  }
}

void velocityRobot (double w1, double w2, double w3){
  // w1 = w2; w2 = w1; w3 = w0
  ufRobot = (0.5774*Radio)*(w2-w3);//0
  ulRobot = -(Radio/3)*(w2-(2*w1)+w3);//0
  wRobot = -(Radio/(3*L))*(w1+w2+w3);//
}

void velocityMotor (double uf, double ul, double w){
  wRef2 = (ul-(L*w))/Radio;
  wRef1 = -(ul+(2*L*w)-1.7321*uf)/(2*Radio);
  wRef0 = -(ul+(2*L*w)+1.7321*uf)/(2*Radio);
  }
