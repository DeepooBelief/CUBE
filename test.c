#include <stdio.h>
#include <wiringPi.h>

#define dir_pin 0

#define step_pin 2

#define sleep_pin 3

#define servo_pin 26

#define period 2000

#define MOTOR_STEPS 200

#define resolution 1

void flip_cube(void){
	for(int i = 20; i < 38; i+=2){
		pwmWrite(servo_pin, i);
		delay(10);
	}
	delay(300);
	for(int i = 35; i > 21; i-=2){
		pwmWrite(servo_pin, i);
		delay(50);
	}
	pwmWrite(servo_pin, 20);
	delay(50);
	delay(200);
}

void pwmsetup(void){
	pinMode(servo_pin, PWM_OUTPUT);
	pwmSetMode(PWM_MODE_MS);
	pwmSetRange(720);
	pwmSetClock(1500);
	pwmWrite(servo_pin, 21);
}

void rotate(int angle, int anti){
	digitalWrite(dir_pin, anti);
	int start_period = 4000;
	for(int i = 0; i < angle * MOTOR_STEPS * resolution / 360; i++){
		//printf("%d\n", start_period);
		digitalWrite(step_pin, HIGH);
		delayMicroseconds(start_period);
		digitalWrite(step_pin, LOW);
		delayMicroseconds(start_period);
		if(start_period > period)
			start_period -= 100;
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
	delay(2000);
	rotate(3600, HIGH);
	delay(100);
	flip_cube();
	delay(100);
	//rotate(90, LOW);
	//delay(100);
	releasePins();
	return 0;
}
