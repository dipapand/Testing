import serial
import time

print('This is the simple_daq.py file')
print('simple_daq.py => __name__ = {}'.format(__name__))
#this changes if file is executed or imported

class SimpleDaq():
    DEFAULTS = {'write_termination' :'\n',
                'read_termination' :'\n',
                'encoding': 'ascii',
                'baudrate': 9600,
                'write_timeout': 1,
                'read_timeout': 1}

    def __init__(self, port):
        self.port = port

    def initialize(self):
        self.rsc = serial.Serial(port=self.port,
                                 baudrate=self.DEFAULTS['baudrate'],
                                 timeout=self.DEFAULTS['read_timeout'],
                                 write_timeout=self.DEFAULTS['write_timeout'])
        time.sleep(2)

    def write(self, message):
        msg = (message + self.DEFAULTS['write_termination']).encode(self.DEFAULTS['encoding'])
        self.rsc.write(msg)

    def read(self):
        line = "".encode(self.DEFAULTS['encoding'])
        read_termination = self.DEFAULTS['read_termination'].encode(self.DEFAULTS['encoding'])
        while True:
            new_char = self.rsc.read(size=1)
            line += new_char
            if new_char == read_termination:
                break
        return line.decode(self.DEFAULTS['encoding'])

    def query(self, message):
        self.write(message)
        return self.read()

    def finalize(self):
        if self.rsc is not  None:
            self.rsc.close()

    def id0(self):
        #self.rsc.write(b'ID0')
        #time.sleep(1)
        #return self.rsc.readline()
        write_string = 'ID0'
        return self.query(write_string)

    def set_pin_mode(self, pin, mode):
        #command = (''.join(('M', str(mode), str(pin)))).encode()
        #self.rsc.write(command)
        write_string = 'M{}{}'.format(mode, pin)
        self.write(write_string)

    def get_dig_val(self, pin):
        #command = (''.join(('R', 'D', str(pin)))).encode()
        #self.rsc.write(command)
        #return self.rsc.readline()
        write_string = 'RD{}'.format(pin)
        return self.query(write_string)

    def set_dig_val(self, pin, val):
        #command = (''.join(('W', 'D', str(pin), ':', str(val)))).encode()
        #self.rsc.write(command)
        write_string = 'WD{}:{}'.format(pin, val)
        self.write(write_string)

    def get_ana_val(self, pin):
        #command = (''.join(('R', 'A', str(pin)))).encode()
        #self.rsc.write(command)
        #return self.rsc.readline()
        write_string = 'RA{}'.format(pin)
        return self.query(write_string)


    def set_ana_val(self, pin, val):
        #command = (''.join(('W', 'A', str(pin), ':', str(val)))).encode()
        #self.rsc.write(command)
        write_string = 'WA{}:{}'.format(pin, val)
        self.write(write_string)

# variable __name__ is = '__main__' when the file simple_daq.py is executed by itself
# from pycharm click on RUN
# from DOS type from inside Controller folder: python simle_daq.py
# BUT if this file is imported by another file the if does not get executed
# This is to check code by running file by itself
# OR from DOS I can type
# python (from anywhere because PATH has the path for python.exe)
#from Controller import simple_daq (PYTHONPATH has the path for PythonForTheLab foder)
#dev = simple_daq.SimpleDaq('COM4')
#dev.initialize()
#dev.set_pin_mode(13, 'O')
#dev.set_dig_value(13, 1)
#dev.set_dig_value(13, 0)
#dev.finalize()
if __name__ == '__main__':
    print('This printed only from __main__')
    dev = SimpleDaq('COM4')
    dev.initialize()


    data2= dev.query('ID0')
    print('data = {}'.format(data2))

    dev.set_pin_mode(13, 'O')

    time.sleep(1)
    dev.set_dig_val(13, 0)
    time.sleep(0.5)
    data = dev.get_dig_val(13)
    print('data = {}'.format(data))

    time.sleep(1)
    dev.set_dig_val(13, 1)
    time.sleep(0.5)
    data = dev.get_dig_val(13)
    print('data = {}'.format(data))

    time.sleep(1)
    dev.set_ana_val(9, 150)

    for x in range(10):
        time.sleep(0.5)
        #print(x)
        data = dev.get_ana_val(5)
        print('data = {}'.format(data))

    dev.finalize()
