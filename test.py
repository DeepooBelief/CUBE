from ctypes import *
test = CDLL('./test.dll')
test.wiringPiSetup()
test.motorsetup()
test.rotate(180, True)
test.delay(50)
test.releasePins()
