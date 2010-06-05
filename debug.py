import time
from OSC import *

client = OSCClient()
client.connect(('localhost', 8080))

for y in range(8):
    for x in range(8):
        m = OSCMessage('/box/led')
        m.append([y, x, 1])
        client.send(m)
        time.sleep(0.3)
      
for y in range(8):
    for x in range(8):
        m = OSCMessage('/box/led')
        m.append([y, x, 0])
        client.send(m)
        time.sleep(0.3)
       
for y in range(8):
    m = OSCMessage('/box/led_col')
    m.append([y, 255])
    client.send(m)
    time.sleep(0.3)

for y in range(8):
    m = OSCMessage('/box/led_col')
    m.append([y, 1])
    client.send(m)
    time.sleep(0.3)

for y in range(8):
    m = OSCMessage('/box/led_col')
    m.append([y, 2])
    client.send(m)
    time.sleep(0.3)

for y in range(8):
    m = OSCMessage('/box/led_col')
    m.append([y, 4])
    client.send(m)
    time.sleep(0.3)

for y in range(8):
    m = OSCMessage('/box/led_col')
    m.append([y, 8])
    client.send(m)
    time.sleep(0.3)

for y in range(8):
    m = OSCMessage('/box/led_col')
    m.append([y, 16])
    client.send(m)
    time.sleep(0.3)

for y in range(8):
    m = OSCMessage('/box/led_col')
    m.append([y, 32])
    client.send(m)
    time.sleep(0.3)

for y in range(8):
    m = OSCMessage('/box/led_col')
    m.append([y, 127])
    client.send(m)
    time.sleep(0.3)

for y in range(8):
    m = OSCMessage('/box/led_col')
    m.append([y, 0])
    client.send(m)
    time.sleep(0.3)

for y in range(8):
    m = OSCMessage('/box/led_row')
    m.append([y, 255])
    client.send(m)
    time.sleep(0.3)

for y in range(8):
    m = OSCMessage('/box/led_row')
    m.append([y, 1])
    client.send(m)
    time.sleep(0.3)

for y in range(8):
    m = OSCMessage('/box/led_row')
    m.append([y, 2])
    client.send(m)
    time.sleep(0.3)

for y in range(8):
    m = OSCMessage('/box/led_row')
    m.append([y, 4])
    client.send(m)
    time.sleep(0.3)

for y in range(8):
    m = OSCMessage('/box/led_row')
    m.append([y, 8])
    client.send(m)
    time.sleep(0.3)

for y in range(8):
    m = OSCMessage('/box/led_row')
    m.append([y, 16])
    client.send(m)
    time.sleep(0.3)

for y in range(8):
    m = OSCMessage('/box/led_row')
    m.append([y, 127])
    client.send(m)
    time.sleep(0.3)
 
for y in range(8):
    m = OSCMessage('/box/led_row')
    m.append([y, 0])
    client.send(m)
    time.sleep(0.3)
    
m = OSCMessage('/box/frame')
m.append([1, 2, 4, 8, 16, 32, 64, 128, 255])
client.send(m)

m = OSCMessage('/box/frame')
m.append([255, 128, 64, 32, 16, 8, 4, 2, 1])
client.send(m)

m = OSCMessage('/box/clear')
m.append(1)
client.send(m)

m = OSCMessage('/box/clear')
m.append(0)
client.send(m)

m = OSCMessage('/sys/prefix')
m.append('new_prefix')
client.send(m)

m = OSCMessage('/sys/test')
m.append(1)
client.send(m)

m = OSCMessage('/sys/intensity')
m.append(0.5)
client.send(m)

m = OSCMessage('/sys/test')
m.append(1)
client.send(m)

m = OSCMessage('/sys/intensity')
m.append(1)
client.send(m)

m = OSCMessage('/sys/test')
m.append(1)
client.send(m)

