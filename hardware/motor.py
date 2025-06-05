import RPi.GPIO as GPIO
import atexit
from config import MOTOR_PINS, PWM_FREQ, PWM_DUTY

IN1 = MOTOR_PINS["IN1"]
IN2 = MOTOR_PINS["IN2"]
ENA = MOTOR_PINS["ENA"]

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

# PWM 설정
pwm = GPIO.PWM(ENA, PWM_FREQ)
pwm.start(0)

def motor_control(on: bool):
    if on:
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        pwm.ChangeDutyCycle(PWM_DUTY)
        # print(f"모터 ON ({PWM_DUTY}%)")
    else:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        pwm.ChangeDutyCycle(0)
        # print("모터 OFF")

# print => 계속 출력될 가능성이 있어서 일단 주석처리함

def cleanup_gpio():
    pwm.stop()
    GPIO.cleanup()

# 종료 시 자동 정리
atexit.register(cleanup_gpio)



