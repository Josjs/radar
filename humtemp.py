# pip install Adafruit_DHT
# enable w1 in raspi-config
# select correct w1-pin

import Adafruit_DHT

sensor = Adafruit_DHT.AM2302
pin = 23 #physical pin 16 

# Just a rename for simpler code
def read():
    return Adafruit_DHT.read_retry(sensor, pin)

