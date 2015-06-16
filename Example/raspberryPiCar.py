# This project was first realised by modifying code by The Raspberry Pi Guy. Please check the link below for the original code.
# https://github.com/the-raspberry-pi-guy/Wiimote

# This program utilises the cwiid Python library in order to get input over bluetooth from a wiimote.
# The following code can be used to control a toy car with four pins, one for each forward, reverse, left and right.
# One PWM pin is used to regulate power given to the left/right turning motor which required lower operating voltage in my case.
# All outputs from the GPIO are given to a L298N IC.

import cwiid
import time
import RPi.GPIO as GPIO	

GPIO.setmode(GPIO.BOARD)	# Pins used are numbered by counting across and down from pin 1 at the top left (nearest to the SD card).

pinF = 23	# Forward
GPIO.setup(pinF, GPIO.OUT)

pinR = 24	# Reverse
GPIO.setup(pinR, GPIO.OUT)

pinL = 3	# Left
GPIO.setup(pinL, GPIO.OUT)

pinRi = 5	# Right
GPIO.setup(pinRi, GPIO.OUT)

pinPw = 8	# PWM to regulate power supplied to low powered front motor
GPIO.setup(pinPw, GPIO.OUT)
button_delay = 0.1

white = GPIO.PWM(pinPw, 100)	# Initialise PWM pin and set to 75% time on
white.start(75)

time.sleep(1)

print 'press 1+2'

# This code attempts to connect to your Wiimote and if it fails the program quits

for i in range(0, 3):	# This for loop is used to listen for connection thrice before exiting the program
    try:
        wii = cwiid.Wiimote()
        break
    except RuntimeError:
        print 'Cannot connect to your Wiimote. Run again and make sure you are holding buttons 1 + 2!'
        i = i + 1
        if i >= 3:		# No connection found after 3 attempts, exit performing all exit routines
            GPIO.output(pinF, 0)
            GPIO.output(pinR, 0)
            GPIO.output(pinL, 0)
            GPIO.output(pinRi, 0)
            white.stop()
            GPIO.cleanup()
            exit(wii)
            quit()

print 'Wiimote connection established!\n'
print 'Press PLUS and MINUS together to disconnect and quit.\n'
wii.rumble = 1	# Vibrate the remote for 1 second to show succssfull connection.
time.sleep(1)
wii.rumble = 0

time.sleep(3)
wii.rpt_mode = cwiid.RPT_BTN
flag = 0		# This variable is used to set forward or reverse pins once while the left/right values are changed continuously

# Main loop for checking input from the remote

while True:
    buttons = wii.state['buttons']

	# Detects whether + and - are held down and if they are it quits the program

    if buttons - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0:
        print '\nClosing connection ...'

    	# While exiting call all exit routines

        GPIO.output(pinF, 0)
        GPIO.output(pinR, 0)
        GPIO.output(pinL, 0)
        GPIO.output(pinRi, 0)
        white.stop()
        GPIO.cleanup()
        wii.rumble = 1  # Vibrate the remote for 1 second to indicate dissconection
        time.sleep(1)
        wii.rumble = 0
        exit(wii)
    wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC

	# The following code detects whether any of the Wiimotes buttons have been pressed and sets the appropritate pins

    if wii.state['buttons'] & cwiid.BTN_B:	# Check button B is pressed
        if not wii.state['buttons'] & cwiid.BTN_A:  # Chech button A is not pressed
            print 'Button B pressed'
            chk = 0
            while chk == 0:
                tilt = wii.state['acc'][0]
                time.sleep(0.01)
                if flag == 0:					# FORWARD
                    flag = 1
                    GPIO.output(pinF, 1)
                    GPIO.output(pinR, 0)
                if tilt < 115: 					# LEFT
                    GPIO.output(pinL, 1)
                    GPIO.output(pinRi, 0)
                elif tilt > 115 and tilt < 125:	# MIDDLE
                    GPIO.output(pinL, 0)
                    GPIO.output(pinRi, 0)
                elif tilt > 125:				# RIGHT
                    GPIO.output(pinL, 0)
                    GPIO.output(pinRi, 1)
                buttons = wii.state['buttons']

                if buttons - cwiid.BTN_B == -4:	# When button B is no longer pressed, exit while loop
                    chk = 5

            time.sleep(0.01)
    
    # No button pressed set all GPIO to zero
    
    flag = 0
    GPIO.output(pinF, 0)
    GPIO.output(pinR, 0)
    GPIO.output(pinL, 0)
    GPIO.output(pinRi, 0)

    if wii.state['buttons'] & cwiid.BTN_A:	# Button A is pressed
        if not wii.state['buttons'] & cwiid.BTN_B:  # Button B is not pressed
            print 'Button A pressed'
            chk = 0
            while chk == 0:
                time.sleep(0.01)
                tilt = wii.state['acc'][0]
                if flag == 0:					# REVERSE
                    flag = 1
                    GPIO.output(pinR, 1) 
                    GPIO.output(pinF, 0)
                if tilt < 115:					# LEFT
                    GPIO.output(pinL, 1)
                    GPIO.output(pinRi, 0)
                elif tilt > 115 and tilt < 125:	# MIDDLE
                	GPIO.output(pinL, 0)
                    GPIO.output(pinRi, 0)
                elif tilt > 125:				# RIGHT
                	GPIO.output(pinL, 0)
                    GPIO.output(pinRi, 1)
                if wii.state['buttons'] - cwiid.BTN_A == -8: # When button A is no longer pressed, exit while loop
                    chk = 5

            time.sleep(0.01)
    
    # No button pressed set all GPIO to zero
    
    flag = 0
    GPIO.output(pinF, 0)
    GPIO.output(pinR, 0)
    GPIO.output(pinL, 0)
    GPIO.output(pinRi, 0)

			
