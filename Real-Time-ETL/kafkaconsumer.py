from ensurepip import bootstrap
from kafka import KafkaConsumer
import json


if __name__ == "__main__":
    consumer = KafkaConsumer(
        "registered_user", bootstrap_servers='localhost:9092', auto_offset_reset='earliest')
    print("Consuming data.....")

    for msg in consumer:
        print("[Log: {}] end/next --->".format(json.loads(msg.value)))
