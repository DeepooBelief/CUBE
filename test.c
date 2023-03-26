#include <stdio.h>
#include <wiringPi.h>

#define dir_pin 0

#define step_pin 2

#define sleep_pin 3

#define servo_pin 26

#define period 900

#define MOTOR_STEPS 200

#define resolution 2

void flip_cube(void){
	pwmWrite(servo_pin, 35);
	delay(300);
	pwmWrite(servo_pin, 21);
	delay(500);
}

void pwmsetup(void){
	pinMode(servo_pin, PWM_OUTPUT);
	pwmSetMode(PWM_MODE_MS);
	pwmSetRange(720);
	pwmSetClock(1500);
}

void rotate(int angle, int anti){
	digitalWrite(dir_pin, anti);
	for(int i = 0; i < angle * MOTOR_STEPS * resolution / 360; i++){
		digitalWrite(step_pin, HIGH);
		delayMicroseconds(period);
		digitalWrite(step_pin, LOW);
		delayMicroseconds(period);
	}
}

void motorsetup(){
	pinMode(step_pin, OUTPUT);
	pinMode(dir_pin, OUTPUT);
	pinMode(sleep_pin, OUTPUT);
	digitalWrite(step_pin, LOW);
	digitalWrite(sleep_pin, HIGH);
}

void releasePins(){
	pinMode(sleep_pin, INPUT);
	pinMode(step_pin, INPUT);
	pinMode(dir_pin, INPUT);
	pinMode(servo_pin, INPUT);
}

int main(void){
	wiringPiSetup();
	motorsetup();
	pwmsetup();
	delay(100);
	rotate(180, 1);
	delay(500);
	flip_cube();
	delay(500);
	rotate(360, 0);
	delay(50);
	releasePins();
	return 0;
}
