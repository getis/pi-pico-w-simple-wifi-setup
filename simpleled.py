# use web interface to control an LED

import utime
import network
import socket
import urequests
from machine import Pin
from NetworkCredentials import NetworkCredentials

ssid = NetworkCredentials.ssid
password = NetworkCredentials.password

# set WiFi to station interface
wlan = network.WLAN(network.STA_IF)
# activate the network interface
wlan.active(True)
# connect to wifi network
wlan.connect(ssid, password)

max_wait = 10
# wait for connection
while max_wait > 0:
    """
        0   STAT_IDLE -- no connection and no activity,
        1   STAT_CONNECTING -- connecting in progress,
        -3  STAT_WRONG_PASSWORD -- failed due to incorrect password,
        -2  STAT_NO_AP_FOUND -- failed because no access point replied,
        -1  STAT_CONNECT_FAIL -- failed due to other problems,
        3   STAT_GOT_IP -- connection successful.
    """
    if wlan.status() < 0 or wlan.status() >= 3:
        # connection successful
        break
    max_wait -= 1
    print('waiting for connection... ' + str(max_wait))
    utime.sleep(1)

# check connection
if wlan.status() != 3:
    # No connection
    raise RuntimeError('network connection failed')
else:
    # connection successful
    print('wlan connected')
    status = wlan.ifconfig()
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
