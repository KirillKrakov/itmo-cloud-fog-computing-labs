import paho.mqtt.client as mqtt
import os, json

BROKER = os.getenv("MQTT_BROKER", "mosquitto")
PORT = int(os.getenv("MQTT_PORT", 1883))
TOPIC = os.getenv("ALERT_TOPIC", "factory/cloud/alerts")
CLIENT_ID = "cloud-subscriber"

def on_connect(client, userdata, flags, rc):
    print("Connected with rc:", rc)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
    except Exception:
        payload = msg.payload.decode()
    print("ALERT received on", msg.topic, ":", payload)

client = mqtt.Client(CLIENT_ID)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.loop_forever()