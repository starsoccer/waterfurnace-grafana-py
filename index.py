from prometheus_client import start_http_server, Summary
from prometheus_client.core import GaugeMetricFamily
from prometheus_client import Gauge

from waterfurnace.waterfurnace import WaterFurnace
import os
import sys
import random
import time
import logging

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.WARN)

# REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request', ["unit"])

# Create a metric to track time spent and requests made.
#c = Counter('my_requests_total', 'HTTP Failures', ['method', 'endpoint'])

airflowcurrentspeed = Gauge(
    "wf_airflowcurrentspeed", "Current Air Speed", ["unit"])
auxpower = Gauge(
    "wf_auxpower", "Aux Heat Power in Watts", ["unit"])
compressorpower = Gauge(
    "wf_compressorpower", "Compressor Power Usage in Watts", ["unit"])
enteringwatertemp = Gauge("wf_enteringwatertemp", "Entering Water Tem (F)", ["unit"])
fanpower = Gauge("wf_fanpower", "Fan Power Usage in Watts", ["unit"])
leavingairtemp = Gauge("wf_leavingairtemp", "Leavin Air Temp (F)", ["unit"])
looppumppower = Gauge("wf_looppumppower", "Loop Pump Power in Watts", ["unit"])
modeofoperation = Gauge("wf_modeofoperation", "System current mode", ["unit"])
totalunitpower = Gauge("wf_totalunitpower", "Total Power Usage in Watts", ["unit"])
tstatactivesetpoint = Gauge("wf_tstatactivesetpoint", "Thermostat active set point (F)", ["unit"])
tstatcoolingsetpoint = Gauge("wf_tstatcoolingsetpoint", "Thermostat Cooling set point (F)", ["unit"])
tstatdehumidsetpoint = Gauge("wf_tstatdehumidsetpoint", "Thermostat Dehumidier set point (%)", ["unit"])
tstatheatingsetpoint = Gauge("wf_tstatheatingsetpoint", "Thermostat Heating set point (F)", ["unit"])
tstathumidsetpoint = Gauge("wf_tstathumidsetpoint", "Thermostat Humidifier set point (%)", ["unit"])
tstatrelativehumidity = Gauge("wf_tstatrelativehumidity", "Thermostat relevite humidity (%)", ["unit"])
tstatroomtemp = Gauge("wf_tstatroomtemp", "Thermostat Room Temp (F)", ["unit"])


class Settings(object):

    def __init__(self):
        self.username = os.environ.get('WF_USERNAME', False)
        self.password = os.environ.get('WF_PASSWORD', False)
        self.unit = os.environ.get('WF_UNIT', False)

# @REQUEST_TIME.time('placeholder')
def update_metrics(waterfurnace):
    """Fetch metrics from waterfurnace and add to metrics.

    Input:
      waterfurnace (object):  waterfurnace client.
    """

    data = waterfurnace.read()
    logger.debug("{}".format(data))
    unit = data.awlid

    airflowcurrentspeed.labels(unit).set(data.airflowcurrentspeed)
    auxpower.labels(unit).set(data.auxpower)
    compressorpower.labels(unit).set(data.compressorpower)
    enteringwatertemp.labels(unit).set(data.enteringwatertemp)
    fanpower.labels(unit).set(data.fanpower)
    leavingairtemp.labels(unit).set(data.leavingairtemp)
    looppumppower.labels(unit).set(data.looppumppower)
    modeofoperation.labels(unit).set(data.modeofoperation)
    totalunitpower.labels(unit).set(data.totalunitpower)
    tstatactivesetpoint.labels(unit).set(data.tstatactivesetpoint)
    tstatcoolingsetpoint.labels(unit).set(data.tstatcoolingsetpoint)
    tstatdehumidsetpoint.labels(unit).set(data.tstatdehumidsetpoint)
    tstatheatingsetpoint.labels(unit).set(data.tstatheatingsetpoint)
    tstathumidsetpoint.labels(unit).set(data.tstathumidsetpoint)
    tstatrelativehumidity.labels(unit).set(data.tstatrelativehumidity)
    tstatroomtemp.labels(unit).set(data.tstatroomtemp)


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8912)
    logger.debug("started server")
    settings = Settings()
    if not (settings.username and settings.password and settings.unit):
        sys.exit("You must set WF_USERNAME, WF_PASSWORD, WF_UNIT")

    wf = WaterFurnace(settings.username, settings.password, settings.unit)
    wf.login()
    logger.debug("logged into waterfurnace, we hope")
    # Generate some requests.
    while True:
        logger.debug("about to update metrics")
        update_metrics(wf)
        time.sleep(9)