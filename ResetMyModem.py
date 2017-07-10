#!/usr/bin/python

import requests
import time
import RPi.GPIO as gpio

MODEM_RELE_GPIO = 11
STAY_OFF_FOR = 90

TIMEOUT_AT = 3
MAX_FAULT = 3
RESET_FAULTS_AT = 3

def is_connected():
    """
    Check if has Connection making a request to Google server using IP.
    """
    try:
        requests.get('http://216.58.194.78', timeout=TIMEOUT_AT)
        return True
    except: 
        return False

def reset_modem():
    """
    Reset the Modem turning the GPIO LOW (The module used requires this)
    """
    print("Reseting Modem... \nplease wait!")
    gpio.output(MODEM_RELE_GPIO, gpio.LOW)
    time.sleep(5)
    gpio.output(MODEM_RELE_GPIO, gpio.HIGH)
    time.sleep(STAY_OFF_FOR) #wait the modem reset
    print("Modem Reseted!")

def config_gpio():
    gpio.setmode(gpio.BOARD)
    gpio.setup(MODEM_RELE_GPIO, gpio.OUT)
    gpio.output(MODEM_RELE_GPIO, gpio.HIGH)

def main():
    """
    Program main function
    """
    failed_tests = 0
    success_tests = 0

    config_gpio()

    while True:
        try:            
            if is_connected():
                success_tests = success_tests + 1
                print("Connection OK!")
            else:
                print("Connection Fail!")
                failed_tests = failed_tests + 1

            if failed_tests == MAX_FAULT:
                reset_modem()
                success_tests = 0
                failed_tests = 0
                continue
            if success_tests == RESET_FAULTS_AT:
                success_tests = 0
                failed_tests = 0
            time.sleep(5)
        except KeyboardInterrupt:
            print("Closed By User")
            break
        
    print("Reseting GPIO states!")
    gpio.cleanup()
            
if  __name__ =='__main__':main()