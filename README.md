![Robot pic](https://github.com/bmidgley/lodrive/raw/master/images/bot.jpg)

Use a raspberry pi zero w with camera and ssd1306 LCD to display the input from the camera and drive continuous servos.

The robot drives in the direction of the tip of the solid 22-degree wedge it finds using the camera.

GPIO13 (pin 33) and GPIO18 (pin 12) are control lines for the continuous servos. The servos use 5v from pin 2 and ground from pin 14.

The LCD is wired up:

* CS to pin 24
* DC to pin 16
* RES to pin 18
* D1 to pin 19
* D0 to pin 23
* VCC to 5v pin 2
* GND to gnd pin 6
