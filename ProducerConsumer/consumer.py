#!/usr/bin/env python3
from kafka import KafkaConsumer
from json import loads
import logging
import os

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Initializing Kafka consumer...")

# Read configurations from environment variables
bootstrap_servers = os.getenv('KAFKA_BROKER_LIST', 'kafka-test-controller-0.kafka-test-controller-headless.fenton-neuroscience.svc.cluster.local:9092,kafka-test-controller-1.kafka-test-controller-headless.fenton-neuroscience.svc.cluster.local:9092,kafka-test-controller-2.kafka-test-controller-headless.fenton-neuroscience.svc.cluster.local:9092')
sasl_mechanism = os.getenv('KAFKA_SASL_MECHANISM', 'PLAIN')  
security_protocol = os.getenv('KAFKA_SECURITY_PROTOCOL', 'SASL_PLAINTEXT')  # Default to SASL_PLAINTEXT if not specified
sasl_username = os.getenv('KAFKA_SASL_USERNAME', 'user1')  # Use separate env var for username
sasl_password = os.getenv('KAFKA_SASL_PASSWORD', 'o7Aj0AWHeM')  # Use separate env var for password

# Kafka Consumer Configuration using kafka-python
consumer = KafkaConsumer(
    os.getenv('KAFKA_TOPIC', 'test'),  # Default to 'test' if not specified
    bootstrap_servers=bootstrap_servers.split(','),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='python-consumer',
    value_deserializer=lambda x: loads(x.decode('utf-8')),
    security_protocol=security_protocol,
    sasl_mechanism=sasl_mechanism,
    sasl_plain_username=sasl_username,
    sasl_plain_password=sasl_password,
)

logging.info("Kafka consumer initialized. Listening for messages...")

# Open a file for writing in append mode
with open('/usr/src/app/consumer_output.txt', 'a') as output_file:
    for message in consumer:
        log_msg = f'Received message: {message.value}'
        print(log_msg)
        logging.info(log_msg)
        output_file.write(log_msg + '\n')
        output_file.flush()  # Flush data to disk after each write
