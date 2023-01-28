# use web interface to control an LED

import utime
import network
import socket
import urequests
from machine import Pin
from NetworkCredentials import NetworkCredentials

ssid = 'PiPicoAp'
password = 'password'

ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)

# wait for wifi to go active
wait_counter = 0
while ap.active() == False:
    print("waiting " + str(wait_counter))
    time.sleep(0.5)
    pass

print('WiFi active')
status = ap.ifconfig()
pico_ip = status[0]
print('ip = ' + status[0])

# Open socket
# addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
addr = (pico_ip, 80)
s = socket.socket()
s.bind(addr)
s.listen(1)
print('listening on', addr)

led = Pin(28, Pin.OUT)
led.off()
led_state = False

# main loop
while True:
    client, client_addr = s.accept()
    raw_request = client.recv(1024)
    # translate byte string to normal string variable
    raw_request = raw_request.decode("utf-8")
    print(raw_request)

    # break request into words (split at spaces)
    request_parts = raw_request.split()
    http_method = request_parts[0]
    request_url = request_parts[1]

    if request_url.find("/ledon") != -1:
        # turn LED on
        led_state = True
        led.on()
    elif request_url.find("/ledoff") != -1:
        # turn LED off
        led_state = False
        led.off()
    else:
        # do nothing
        pass

    led_state_text = "OFF"
    if led_state:
        led_state_text = "ON"

    file = open("simpleled.html")
    html = file.read()
    file.close()

    html = html.replace('**ledState**', led_state_text)
    client.send(html)
    client.close()
