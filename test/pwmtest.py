#pwm
import wiringpi
wiringpi.wiringPiSetup()
wiringpi.pinMode(26, wiringpi.PWM_OUTPUT);
wiringpi.pwmSetMode(wiringpi.PWM_MODE_MS);
wiringpi.pwmSetRange(720);
wiringpi.pwmSetClock(1500);
wiringpi.pwmWrite(26, 35);
wiringpi.delay(500);
wiringpi.pwmWrite(26, 22);
wiringpi.delay(500);
