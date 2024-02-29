# #!/usr/bin/env python3
# from kafka import KafkaConsumer
# from json import loads
# import logging
# import os

# # Setup basic logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# logging.info("Initializing Kafka consumer...")

# # Read configurations from environment variables
# #bootstrap_servers = os.getenv('KAFKA_BROKER_LIST', 'kafka-test-controller-0.kafka-test-controller-headless.fenton-neuroscience.svc.cluster.local:9092,kafka-test-controller-1.kafka-test-controller-headless.fenton-neuroscience.svc.cluster.local:9092,kafka-test-controller-2.kafka-test-controller-headless.fenton-neuroscience.svc.cluster.local:9092')
# bootstrap_servers = os.getenv('KAFKA_BROKER_LIST', '10.32.250.16:30858,10.32.250.16:31436,10.32.250.16:32281')
# sasl_mechanism = os.getenv('KAFKA_SASL_MECHANISM', 'PLAIN')  
# security_protocol = os.getenv('KAFKA_SECURITY_PROTOCOL', 'SASL_PLAINTEXT')  # Default to SASL_PLAINTEXT if not specified
# sasl_username = os.getenv('KAFKA_SASL_USERNAME', 'user1')  # Use separate env var for username
# sasl_password = os.getenv('KAFKA_SASL_PASSWORD', 'o7Aj0AWHeM')  # Use separate env var for password

# # Kafka Consumer Configuration using kafka-python
# consumer = KafkaConsumer(
#     os.getenv('KAFKA_TOPIC', 'test'),  # Default to 'test' if not specified
#     bootstrap_servers=bootstrap_servers.split(','),
#     auto_offset_reset='earliest',
#     enable_auto_commit=True,
#     group_id='python-consumer',
#     value_deserializer=lambda x: loads(x.decode('utf-8')),
#     security_protocol=security_protocol,
#     sasl_mechanism=sasl_mechanism,
#     sasl_plain_username=sasl_username,
#     sasl_plain_password=sasl_password,
# )

# logging.info("Kafka consumer initialized. Listening for messages...")

# # Open a file for writing in append mode
# # with open('/usr/src/app/consumer_output.txt', 'a') as output_file:
# #     for message in consumer:
# #         log_msg = f'Received message: {message.value}'
# #         print(log_msg)
# #         logging.info(log_msg)
# #         output_file.write(log_msg + '\n')
# #         output_file.flush()  # Flush data to disk after each write
# for message in consumer:
#     log_msg = f'Received message: {message.value}'
#     print(log_msg)
#     #logging.info(log_msg)
#     #output_file.write(log_msg + '\n')
#     #output_file.flush()  # Flush data to disk after each write

import time
import logging
from confluent_kafka import Consumer, KafkaError

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure and create a Consumer with your specific settings
consumer = Consumer({
    'bootstrap.servers': '10.32.250.20:32597,10.32.250.21:30136,10.32.250.16:30879',
    'group.id': 'python-consumer',
    'auto.offset.reset': 'earliest',
    'security.protocol': 'SASL_PLAINTEXT',
    'sasl.mechanism': 'SCRAM-SHA-256',
    'sasl.username': 'user1',
    'sasl.password': 'B2XdUZHpWB'
})

# Subscribe to your topic
consumer.subscribe(['test'])

logging.info("Kafka consumer initialized. Listening for messages...")

try:
    while True:
        # Poll for a message with a timeout
        message = consumer.poll(1.0)  # 1.0 second timeout for polling

        # If no message was returned, message is None
        if message is None:
            time.sleep(5)  # Sleep for 5 sec if no message is available
            continue

        # Check for errors
        if message.error():
            # End of partition event is not an error in this context
            if message.error().code() == KafkaError._PARTITION_EOF:
                logging.info(f"End of partition reached {message.topic()}/{message.partition()}")
            else:
                logging.error(f"Consumer error: {message.error()}")
            continue

        # Successfully received a message
        logging.info(f"Received message: {message.value().decode('utf-8')}")

except KeyboardInterrupt:
    # Handle graceful exit on KeyboardInterrupt (Ctrl+C)
    logging.info("Detected KeyboardInterrupt, exiting...")
except Exception as e:
    # Handle any other exception
    logging.error(f"Unexpected error: {e}")
finally:
    # Cleanly close the consumer on exit
    consumer.close()
    logging.info("Consumer closed. Goodbye.")
