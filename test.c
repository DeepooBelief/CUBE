#include <stdio.h>
#include <wiringPi.h>

#define dir_pin 0

#define step_pin 2

#define sleep_pin 3

#define servo_pin 26

#define period 1400

#define MOTOR_STEPS 200

#define resolution 1

#define released_angle 38

#define locked_angle 28

void flip_cube(void){
	for(int i = 38; i < 60; i+=2){
		pwmWrite(servo_pin, i);
		delay(8);
	}
	delay(300);
	for(int i = 60; i > 38; i-=2){
		pwmWrite(servo_pin, i);
		delay(10);
	}
	//pwmWrite(servo_pin, 40);
	//delay(50);
	delay(200);
}

void pwmsetup(void){
	pinMode(servo_pin, PWM_OUTPUT);
	pwmSetMode(PWM_MODE_MS);
	pwmSetRange(720);
	pwmSetClock(1500);
	pwmWrite(servo_pin, released_angle);
}

void lock(){
	pwmWrite(servo_pin, locked_angle);
	delay(500);
}

void unlock(){
	pwmWrite(servo_pin, released_angle);
	delay(500);
}

void cam_pos(){
	pwmWrite(servo_pin, 31);
	delay(500);
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
	//motorsetup();
	pwmsetup();
	delay(1000);
	cam_pos();
	//lock();
	//rotate(90, HIGH);
	//delay(100);
	//for(int i = 0; i < 10; i++)
	//flip_cube();
	//delay(1000);
	//unlock();
	delay(100);
	//rotate(90, LOW);
	//delay(100);
	releasePins();
	return 0;
}
