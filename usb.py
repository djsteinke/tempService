import serial
from threading import Timer
from json import loads
import logging

module_logger = logging.getLogger('main.usb')


class USB(object):
    def __init__(self, port='/dev/ttyACM0'):
        self.port = port
        self.baud = 9600
        self.serial = None
        self.timer = None
        self.connected = False
        self._c = 0.00
        self._f = 0.00
        self._h = 0.0

    def connect(self):
        try:
            self.serial = serial.Serial(self.port, self.baud, timeout=1)
            self.connected = True
        except serial.SerialException as e:
            module_logger.error('connect() failed: ' + str(e))
            raise Exception('Failed to connect')
        self.timer = Timer(0.1, self.listen)
        self.timer.start()

    def close(self):
        if self.serial is not None:
            self.serial.close()
            self.serial = None
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None
        self.connected = False

    def listen(self):
        while self.connected:
            if self.serial is not None:
                try:
                    data = self.serial.readline()
                    s_data = data.decode().rstrip()
                    if len(s_data) > 0:
                        module_logger.debug(f'listen(): {s_data}')
                        j = loads(s_data)
                        self._c = j['c']
                        self._f = j['f']
                        self._h = j['h']
                    self.timer.start()
                except serial.SerialException as e:
                    module_logger.error(f'listen() ERROR: {str(e)}')
                    self.close()

    @property
    def c(self):
        return self._c

    @property
    def f(self):
        return self._f

    @property
    def h(self):
        return self._h
