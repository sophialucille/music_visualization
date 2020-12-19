from __future__ import print_function
from __future__ import division
import os

DEVICE = 'pi'
#GPIO pin connected to the LED strip pixels (must support PWM)
LED_PIN = 18

LED_FREQ_HZ = 800000

#DMA channel used for generating PWM signal (try 5)
LED_DMA = 5

BRIGHTNESS = 255

#Set True if using an inverting logic level converter
LED_INVERT = True

#Set to True because Raspberry Pi doesn't use hardware dithering
SOFTWARE_GAMMA_CORRECTION = True

