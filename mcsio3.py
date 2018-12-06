#!/usr/bin/python
import sys
import time
import Adafruit_DHT
import httplib, urllib
import json
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(24,GPIO.IN,pull_up_down=GPIO.PUD_UP)
deviceId = "DaqpJ9pk"
deviceKey = "FtZyZYF7b0Ho8drT"
def post_to_mcs(payload):
        headers = {"Content-type": "application/json", "deviceKey": deviceKey}
        not_connected = 1
        while (not_connected):
                try:
                        conn = httplib.HTTPConnection("api.mediatek.com:80")
                        conn.connect()
                        not_connected = 0
                except (httplib.HTTPException, socket.error) as ex:
                        print ("Error: %s" % ex)
                         # sleep 10 seconds
        conn.request("POST", "/mcs/v2/devices/" + deviceId + "/datapoints", json.dumps(payload), headers)
        response = conn.getresponse()
        print( response.status, response.reason, json.dumps(payload), time.strftime("%c"))
        data = response.read()
        conn.close()
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
else:
    print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number>')
    print('Example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO pin #4')
    sys.exit(1)

while True:
        SwitchStatus = GPIO.input(24)
        h0,t0=Adafruit_DHT.read_retry(sensor,pin)
        if h0 is not None and t0 is not None:
                if(SwitchStatus == 1):
                        print('Button pre')
                else:
                        print('Button release')
                print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(t0,h0))
		payload = {"datapoints":[{"dataChnId":"Humidity","values":{"value":h0}},{"dataChnId":"Temperature","values":{"value":t0}},{"dataChnId":"SwitchStatus","values":{"value":SwitchStatus}}]}
        	post_to_mcs(payload)
                time.sleep(10)
	else:
                print('Failed to get reading. Try again!')
                sys.exit(1)
