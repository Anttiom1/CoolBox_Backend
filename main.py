import datetime
import json
import certifi
import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv
from sqlalchemy import text

from dp import get_db

load_dotenv()

myClient = os.getenv('client')
myHost = os.getenv('host')
myUsername = os.getenv('myUsername')
myPassword = os.getenv('myPassword')

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    #print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(myClient)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload)
        ts_in_sec = payload["ts"] // 1000
        dt = datetime.datetime.fromtimestamp(ts_in_sec)
        device = tuple(payload["d"].keys())[0]
        sensor_data = payload["d"][device]
        sensor_id = tuple(sensor_data.keys())[0]
        value = sensor_data[sensor_id]["v"]
        if sensor_id not in ["L1", "L2", "L3"]:
            print(sensor_id, value)
    except Exception as e:
        print(e)
    

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.username_pw_set(myUsername, myPassword)
mqttc.tls_set(certifi.where())
mqttc.connect(myHost, 8883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc.loop_forever()