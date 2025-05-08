import time
import board
import adafruit_vl53l0x
import neopixel_spi as neopixel
import RPi.GPIO as GPIO
from gpiozero import RGBLED
from time import sleep #import libraries

# Set up the GPIO pins for the RGB LED
led1 = RGBLED(red=12, green=19, blue=26)
led2= RGBLED(red=6, green=22, blue = 27)
led3= RGBLED(red=18, green=23, blue=24)
                                                                                 
#setup sensor
i2c = board.I2C()
sensor = adafruit_vl53l0x.VL53L0X(i2c)
sensor.start_continuous()

#setup neopixel
NUM_PIXELS = 8
PIXEL_ORDER = neopixel.GRB
COLORS = (0xFF0000, 0x00FF00, 0x0000FF)
DELAY = 0.1
spi = board.SPI()
red= 0x100000
green=0x00FF00
orange=0xff5b00

pixels = neopixel.NeoPixel_SPI(spi,
                               NUM_PIXELS,
                               pixel_order=PIXEL_ORDER,
                               auto_write=True)
#start with all red                                                         
led1.color=(1,0,0)
led2.color=(1,0,0)
led3.color=(1,0,0)
pixels.fill(red)
def lightLoop():
    led1.color = (0,1,0)
    distance = sensor.range
    led2.color = (1,0,0)
    distance = sensor.range
    led3.color = (1,0,0)
    pixels.fill(red)
    distance = sensor.range
    sleep(5)
    distance = sensor.range
    led1.color = (1,0.15,0)
    distance = sensor.range
    sleep(4)
    distance = sensor.range
    led1.color = (1,0,0)
    distance = sensor.range
    led2.color = (0,1,0)
    distance = sensor.range
    sleep(5)
    distance = sensor.range
    led2.color = (1,0.15,0)
    sleep(4)
    distance = sensor.range
    led2.color = (1,0,0)
    led3.color = (0,1,0)
    sleep(5)
    distance = sensor.range
    led3.color = (1,0.15,0)
    sleep(4)
    distance = sensor.range
    led3.color = (1,0,0)
    pixels.fill(green)
    sleep(5)
    pixels.fill(orange)
    sleep(4)
    pixels.fill(red)
count = 0

while True:
    distance=sensor.range
    start = time.time()
    while count<4:
        distance = sensor.range #update distance
        if distance <= 25:
            count += 1
            start = time.time()
            print(count)
            sleep(1.5)
        end = time.time()
        if (end - start)>= 15 or count==4:
            lightLoop()
            count = 0
            start = time.time()
            
