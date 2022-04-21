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
        Timer(1, self.listen).start()
        module_logger.debug('connect(): complete')

    def close(self):
        if self.serial is not None:
            self.serial.close()
            self.serial = None
        self.connected = False
        module_logger.debug('close(): complete')

    def listen(self):
        first = True
        module_logger.debug('listen(): started')
        while self.connected:
            if first:
                module_logger.debug('listen(): connected')
            if self.serial is not None:
                if first:
                    module_logger.debug('listen(): serial')
                try:
                    data = self.serial.readline()
                    s_data = data.decode().rstrip()
                    if len(s_data) > 0:
                        module_logger.debug(f'listen(): {s_data}')
                        j = loads(s_data)
                        self._c = j['c']
                        self._f = j['f']
                        self._h = j['h']
                except serial.SerialException as e:
                    module_logger.error(f'listen() ERROR: {str(e)}')
                    self.close()
                first = False

    @property
    def c(self):
        return self._c

    @property
    def f(self):
        return self._f

    @property
    def h(self):
        return self._h
