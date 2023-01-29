# Access point interface

import network
import time

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
print('IP address = ' + status[0])
print('subnet mask = ' + status[1])
print('gateway  = ' + status[2])
print('DNS server = ' + status[3])
