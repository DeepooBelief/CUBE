#include <stdio.h>
#include <wiringPi.h>

#define dir_pin 0

#define step_pin 2

#define sleep_pin 3

#define servo_pin 26

#define period 1600

#define MOTOR_STEPS 200

#define resolution 1

#define e 2.71828

#define final_period 1600

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

void rotate(int angle, int anti,double (*peri_deter)(int)){
	digitalWrite(dir_pin, anti);
	for(int i = 0; i < angle * MOTOR_STEPS * resolution / 360; i++){
		digitalWrite(step_pin, HIGH);
		delayMicroseconds((int)(peri_deter(i)));
		digitalWrite(step_pin, LOW);
		delayMicroseconds((int)(peri_deter(i)));
	}
}

double period_determine(int t)
{
	//uses the variable i (from the for loop in rotate function) to change every time's delay
	double period_ = 0;
	period_ = e ^ (0.02 * period * t);
	return period_;
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
	delay(1000);
	rotate(90, HIGH,period_determine);
	delay(100);
	flip_cube();
	delay(100);
	//rotate(90, LOW);
	//delay(100);
	releasePins();
	return 0;
}
