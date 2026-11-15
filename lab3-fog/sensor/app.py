import random, time, os
import paho.mqtt.client as mqtt
import json

BROKER = os.getenv("MQTT_BROKER", "mosquitto")
PORT = int(os.getenv("MQTT_PORT", 1883))
TOPIC = os.getenv("SENSOR_TOPIC", "factory/sensor/1")
DEVICE_ID = os.getenv("DEVICE_ID", "sensor-1")

client = mqtt.Client(DEVICE_ID)
client.connect(BROKER, PORT, 60)
client.loop_start()

try:
    while True:
        temp = round(random.uniform(60, 95), 2)  # генерация температуры
        payload = json.dumps({"device": DEVICE_ID, "temp": temp, "ts": int(time.time())})
        client.publish(TOPIC, payload, qos=0)
        print("Published:", payload)
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    client.loop_stop()
    client.disconnect()