import logging
import sys
import threading
import smbus
import time

bus = smbus.SMBus(1)
config = [0x08, 0x00]

module_logger = logging.getLogger('main.program')


class TempSensor(object):
    def __init__(self):
        self._temp = 0.0
        self._humidity = 0.0
        self._running = False

    def read_sensor(self):
        try:
            bus.write_i2c_block_data(0x38, 0xE1, config)
            byt = bus.read_byte(0x38)
            measure_cmd = [0x33, 0x00]
            bus.write_i2c_block_data(0x38, 0xAC, measure_cmd)
            time.sleep(0.5)
            data = bus.read_i2c_block_data(0x38, 0x00)
            temp_raw = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
            temp_c = ((temp_raw * 200) / 1048576) - 50
            humid_raw = ((data[1] << 16) | (data[2] << 8) | data[3]) >> 4
            humid = humid_raw * 100 / 1048576
            self._temp = round(temp_c, 2)
            self._humidity = round(humid, 1)
        except all:
            e = sys.exc_info()[0]
            logging.error('read_sensor() error' + str(e))
        if self._running:
            timer = threading.Timer(15, self.read_sensor)
            timer.start()

    def start(self):
        self._running = True
        self.read_sensor()

    def stop(self):
        self._running = True

    @property
    def temp(self):
        return self._temp

    @property
    def humidity(self):
        return self._humidity
