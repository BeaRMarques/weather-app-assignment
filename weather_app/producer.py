"""
Creates kakfa topic and sets up producer.
A new API call is made every 60 seconds to simulate streaming.
"""

import json
import logging
import sys
import time

import requests
from constants import (
    KAFKA_BOOTSTRAP_SERVER,
    KAFKA_REPLICATION_FACTOR,
    KAFKA_TOPIC_NAME,
    KAKFA_NUMBER_PARTITIONS,
    LOCATIONS,
)
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import NoBrokersAvailable, NodeNotReadyError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


for n in range(5):
    try:
        admin_client = KafkaAdminClient(bootstrap_servers=KAFKA_BOOTSTRAP_SERVER)
        break
    except (NoBrokersAvailable, NodeNotReadyError):
        logging.warning("Kafka not ready.")
        time.sleep((3**n) + 1)
else:
    logging.error("Could not connect to kafka.")


existing_topics = admin_client.list_topics()
if KAFKA_TOPIC_NAME not in existing_topics:
    topic_list = [
        NewTopic(
            name=KAFKA_TOPIC_NAME,
            num_partitions=KAKFA_NUMBER_PARTITIONS,
            replication_factor=KAFKA_REPLICATION_FACTOR,
        )
    ]
    admin_client.create_topics(new_topics=topic_list, validate_only=False)
    logger.info(f"Topic `{KAFKA_TOPIC_NAME}` was created.")
else:
    logger.info(f"Topic `{KAFKA_TOPIC_NAME}` already exists.")


producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

while True:
    for lat, lon in LOCATIONS:
        try:
            response = requests.get(
                f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=hourly,daily,current&units=metric&appid=87600d4493f574b1d19f7cf6c247a6eb"
            )
            response.raise_for_status()
            data = response.json()

            producer.send(KAFKA_TOPIC_NAME, value=data)
            producer.flush()

        except Exception as e:
            raise Exception(f"Error sending data to topic: {e}.")

    logger.debug("Waiting 60 seconds.")
    time.sleep(60)
