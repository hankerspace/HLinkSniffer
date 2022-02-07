#!/usr/bin/env python
import time
import serial
from paho.mqtt import client as mqtt_client
import json

broker = '192.168.86.40'
port = 1883
client_id = f'pac'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client, topic, msg):
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status != 0:
        print(f"Failed to send message to topic {topic}")

def processTrameNew(trame):
    splits = trame.split()

    tempStr = ""
    for i in range(len(splits)):
        value = splits[i]
        tempStr += value + "\t"
    print(tempStr)

    dictionary = {}
    for i in range(len(splits)):
        value = splits[i]
        publish(client, "/test2/" + str(i), value)
        dictionary[i] = int(value)
        tempStr += value + "\t"
    # print(tempStr)
    publish(client, "/PAC", json.dumps(dictionary, indent=4))


ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=9600
)
totalCounter = 0

client = connect_mqtt()
totalBytes = ""
while 1:
    totalCounter = totalCounter + 1
    byte = ser.read(1)
    if len(byte) > 0:
        converted = int.from_bytes(byte, "big", signed="True")
        totalBytes += str(converted) + " "
        if "33 0 " in totalBytes:
            if "41 1 1 1 0 -30 " in totalBytes and "33 0 " in totalBytes:
                trame = totalBytes[totalBytes.find("41 1 1 1 0 -30 "):totalBytes.find("33 0")]
                processTrameNew(trame)
            totalBytes = ""
