# raspberryPiCar
This repository contains an installation file and necessary code to make a simple remote controlled toy car using a raspberryPi, Nintendo Wiimote and some hardware.

This code is a modification of the code written by The Raspberry Pi Guy to test the wiimote( https://github.com/the-raspberry-pi-guy/Wiimote ). What was added was to use the button inputs to trigger the GPIO pins.

# Wiimote 
Please check the video by The Raspberry Pi Guy to understand.
https://www.youtube.com/watch?v=bO5-FjLe5xE&list=UUfY8sl5Q6VKndz0nLaGygPw

# Working
Press and hold button B for forward movement
  - Tilt to left, left movement with forward movement
  - Tilt to right, right movement with forward movement

Press and hold button A for reverse movement
  - Tilt to left, left movement with reverse movement
  - Tilt to right, right movement with reverse movement

L298N - Was the motor driver IC used. The PWM output pin was given to one of the enable pins for the turn motor. The otherenable pin was given direct 3.3V for the forward/reverse motor.

# Issues
The code is poorly structured( I did not know python well at that time ).
The motor used for turning will only be activated when either the forward or reverse action is active simultaneusly. 

For any issues or extra information contact me by email found on by GitHub profile.

