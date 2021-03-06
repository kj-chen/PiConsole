import RPi.GPIO as GPIO
import time
from django.http import HttpResponse
from django.shortcuts import redirect

"""
 * |==================================================|
 * |======This code created by K.J. Chen(陳冠儒)======|
 * |=Copyright © 2019 K.J. Chen | All Rights Reserved=|
 * |==================================================|
"""


class CarRun:
    def __init__(self, dt = 3):
        self.dt = dt # Delaytime
        global IN
        IN = [20, 21, 19, 26]
        global EN_A
        EN_A = 16
        global EN_B
        EN_B = 13
        """
        global key
        key = 8
        """
        global AvoidSensorLeft
        AvoidSensorLeft = 12
        global AvoidSensorRight
        AvoidSensorRight = 17

    #def __new__(self, dt = 1):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    # def __call__(self):
    #     return redirect("javascript:window.close();")
    #     #return HttpResponse(' ')

    def motor_init(self):
        global pwm_EN_A
        global pwm_EN_B

        for i in range(4):
            GPIO.setup(IN[i], GPIO.OUT, initial = 0)

        GPIO.setup(EN_A, GPIO.OUT, initial = 1)
        pwm_EN_A = GPIO.PWM(EN_A, 2000)
        pwm_EN_A.start(0)

        GPIO.setup(EN_B, GPIO.OUT, initial = 1)
        pwm_EN_B = GPIO.PWM(EN_B, 2000)
        pwm_EN_B.start(0)

        #GPIO.setup(key,GPIO.IN)
        GPIO.setup(AvoidSensorLeft,GPIO.IN)
        GPIO.setup(AvoidSensorRight,GPIO.IN)

    @staticmethod
    def brake(dt = 1):
        for i in range(4):
            GPIO.output(IN[i], 0)

        pwm_EN_A.ChangeDutyCycle(80)
        pwm_EN_B.ChangeDutyCycle(80)

        time.sleep(dt)

    # Go Advance
    def advance(self, request, b_k = 0):
        dt = self.dt
        for i in range(4):
            t = i%2 == 0
            #t = 1
            GPIO.output(IN[i], t)

        pwm_EN_A.ChangeDutyCycle(80)
        pwm_EN_B.ChangeDutyCycle(80)

        time.sleep(self.dt)
        if b_k == 0:
            self.brake()
        return HttpResponse("Go Advance")
        #self.request = request

    # Go Back
    def back(self, request, b_k = 0):
        for i in range(4):
            t = i%2 == 1
            # t = 0
            GPIO.output(IN[i], t)

        pwm_EN_A.ChangeDutyCycle(80)
        pwm_EN_B.ChangeDutyCycle(80)

        time.sleep(self.dt)
        if b_k == 0:
            self.brake()
        return HttpResponse("Go Back")
        #self.request = request

    # Turn Left
    def left(self, request, b_k = 0):
        for i in range(4):
            t = i == 2
            GPIO.output(IN[i], t)

        pwm_EN_A.ChangeDutyCycle(80)
        pwm_EN_B.ChangeDutyCycle(80)

        time.sleep(self.dt)
        if b_k == 0:
            self.brake()
        return HttpResponse("Turn Left")
        #self.request = request

    # Turn Right
    def right(self, request, b_k = 0):
        for i in range(4):
            t = i == 0
            GPIO.output(IN[i], t)

        pwm_EN_A.ChangeDutyCycle(80)
        pwm_EN_B.ChangeDutyCycle(80)

        time.sleep(self.dt)
        if b_k == 0:
            self.brake()
        return HttpResponse("Turn Right")
        #self.request = request

    # Turn Left in Situ
    def situ_left(self, request, b_k = 0):
        for i in range(4):
            t = i in [1, 2]
            GPIO.output(IN[i], t)

        pwm_EN_A.ChangeDutyCycle(80)
        pwm_EN_B.ChangeDutyCycle(80)

        time.sleep(self.dt)
        if b_k == 0:
            self.brake()
        return HttpResponse("Turn Left in Situ")
        #self.request = request

    # Turn Right in Situ
    def situ_right(self, request, b_k = 0):
        for i in range(4):
            t = i in [0, 3]
            GPIO.output(IN[i], t)

        pwm_EN_A.ChangeDutyCycle(80)
        pwm_EN_B.ChangeDutyCycle(80)

        time.sleep(self.dt)
        if b_k == 0:
            self.brake()
        return HttpResponse("Turn Right in Situ")
        #self.request = request

    # Infrared Avoid
    # def infrared_avoid(self, request):
    #     i = None
    #     while i == None:
    #         LeftSensorValue  = GPIO.input(AvoidSensorLeft)
    #         RightSensorValue = GPIO.input(AvoidSensorRight)
    #
    #         if LeftSensorValue == True and RightSensorValue == True:
    #             run()
    #         elif LeftSensorValue == False and RightSensorValue == True:
    #             spin_right()
    #         time.sleep(0.002)
    #         elif LeftSensorValue == True and RightSensorValue == False:
    #             spin_left()
    #         time.sleep(0.002)
    #     return HttpResponse("Infrared Avoid")

    # Stop to Run the Car
    def stop_run(self, request):
        self.brake()
        return HttpResponse("Stop to Run the Car")
        #self.request = request

    # End Control
    def all_stop(self, request):
        self.request = request
        pwm_EN_A.stop()
        pwm_EN_A.stop()

        GPIO.cleanup()
        return HttpResponse("End Control")
