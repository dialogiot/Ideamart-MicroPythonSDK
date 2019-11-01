from network import WLAN
from network import STA_IF
from mqtt import MQTTClient
import machine
import time
import config


# Setup WiFi
sta_if = WLAN(STA_IF)
sta_if.active(True)


def setup_wifi():
    print("Connecting to Wifi "+config.SSID)
    sta_if.connect(config.SSID, config.PASSWORD)
    while not sta_if.isconnected():
        print("Retrying to connect "+config.SSID)
        time.sleep(1)
    if sta_if.isconnected():
        print("Connected to "+config.SSID)
        client_connect()
        #subscribe()


# Call back function for Subscribe
def sub_callback(topic, msg):
    json = msg.decode("utf-8")
    print(json)


# Setup up MQTT
client = MQTTClient(config.DEVICE_SERIAL, "52.221.141.22", user="rabbit", password="rabbit", port=1883)


def client_connect():
    client.set_callback(sub_callback)
    client.connect()
    print("Connected to Broker with Client ID : "+config.DEVICE_SERIAL)
    client.subscribe(topic=config.DEVICE_BRAND+"/"+config.DEVICE_SERIAL+"/+/sub")


# Subscribe to topic and check for messages
def subscribe():
    client.subscribe(topic=config.DEVICE_BRAND+"/"+config.DEVICE_SERIAL+"/+/sub")
    print("Subscribed to topic : " + config.DEVICE_BRAND+"/"+config.DEVICE_SERIAL+"/+/sub")
    while sta_if.isconnected():
        time.sleep(4)
        if sta_if.isconnected():
            print("checking")
            #client.wait_msg()
        else:
            print("else checking")
            setup_wifi()

setup_wifi()

# client.publish("Home/aaaa", "ON1")
