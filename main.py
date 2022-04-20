import logging
import os

from flask import Flask
from usb import USB
# from temp_sensor import TempSensor
from properties import ip, port

app = Flask(__name__)

# create logger with 'spam_application'
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('log.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

usb = USB()
#sensor = TempSensor()
url = ""


def get_temp_f(temp):
    return temp*1.8+32


@app.route('/')
def get_app():
    link = f'{url}/getTemp'
    return f'Welcome to Temperature Service<br>Use <a href="{link}">{link}</a> for temperature readings.', 200


@app.route('/getTemp')
def get_temp():
    ret = {"temp": usb.c,
           "temp_f": usb.f,
           "humidity": usb.h}
    if not usb.connected:
        ret['humidity'] = -1
    return ret, 200


if __name__ == '__main__':
    try:
        stream = os.popen('hostname -I')
        host_name = stream.read().strip()
    except IOError and OSError as e:
        logger.error('__main__ error' + str(e))
        host_name = ip
    logger.info("machine host_name[" + host_name + "]")
    usb.connect()
    usb.listen()
    url = f'http://{host_name}:{port}'
    app.run(host=host_name, port=port)
