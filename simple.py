import serial
from time import sleep

device = serial.Serial(port='COM4',timeout=1)
sleep(1)
print(device.name)
device.write(b'ID0')
sleep(1)
answer = device.read(3)
sleep(1)
#answer = 'YES'
print('answer = {}'.format(answer))
sleep(1)
device.close()
