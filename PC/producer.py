#!/usr/bin/env python3
from kafka import KafkaProducer
import json
from datetime import datetime
import logging
import os

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Initializing Kafka producer...")

# Read configurations from environment variables
bootstrap_servers = os.getenv('KAFKA_BROKER_LIST', 'kafka-test-controller-0.kafka-test-controller-headless.fenton-neuroscience.svc.cluster.local:9092,kafka-test-controller-1.kafka-test-controller-headless.fenton-neuroscience.svc.cluster.local:9092,kafka-test-controller-2.kafka-test-controller-headless.fenton-neuroscience.svc.cluster.local:9092')
sasl_mechanism = os.getenv('KAFKA_SASL_MECHANISM', 'PLAIN')
security_protocol = os.getenv('KAFKA_SECURITY_PROTOCOL', 'SASL_PLAINTEXT')  # Default to SASL_PLAINTEXT if not specified
sasl_username = os.getenv('KAFKA_SASL_USERNAME', 'user1')  # Use separate env var for username
sasl_password = os.getenv('KAFKA_SASL_PASSWORD', 'o7Aj0AWHeM')  # Use separate env var for password

# Kafka Producer Configuration using kafka-python
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers.split(','),
    security_protocol=security_protocol,
    sasl_mechanism=sasl_mechanism,
    sasl_plain_username=sasl_username,
    sasl_plain_password=sasl_password,
    value_serializer=lambda x: json.dumps(x).encode('utf-8')  # Serialize json messages to bytes
)

logging.info("Kafka producer initialized.")

# Function to send messages
def send_message(topic):
    # Send a message
    for i in range(21):
        data = {'value': i, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        producer.send(topic, data)
        producer.flush()
        
    logging.info(f"Message sent to topic {topic}: {message}")

# Example usage
if __name__ == "__main__":
    topic_name = os.getenv('KAFKA_TOPIC', 'test')  # Default to 'test' if not specified
    message = {'key': 'value'}  # Example message
    send_message(topic_name)
