import serial
from threading import Timer
from json import loads
import logging

module_logger = logging.getLogger('main.usb')


class USB(object):
    def __init__(self):
        self.port = ''
        self.baud = 9600
        self.serial = None
        self.timer = None
        self.connected = False
        self.c = 0.00
        self.f = 0.00
        self.h = 0.0

    def connect(self):
        try:
            self.serial = serial.Serial(self.port, self.baud, timeout=1)
            self.connected = True
        except serial.SerialException as e:
            module_logger.error('connect() failed: ' + str(e))
            raise Exception('Failed to connect')
        self.timer = Timer(1, self.listen)

    def close(self):
        if self.serial is not None:
            self.serial.close()
            self.serial = None
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None
        self.connected = False

    def listen(self):
        if self.serial is not None:
            try:
                data = self.serial.readline()
                s_data = data.decode().rstrip()
                if len(s_data) > 0:
                    module_logger.debug(f'listen(): {s_data}')
                j = loads(s_data)
                self.c = j['c']
                self.f = j['f']
                self.h = j['h']
                self.timer.start()
            except serial.SerialException:
                self.close()

    @property
    def c(self):
        return self.c

    @c.setter
    def c(self, val):
        self.c = val

    @property
    def f(self):
        return self.c

    @f.setter
    def f(self, val):
        self.f = val

    @property
    def h(self):
        return self.h

    @h.setter
    def h(self, val):
        self.h = val
