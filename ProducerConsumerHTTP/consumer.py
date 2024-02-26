import requests
import json
import uuid
import time

# Base URL for the Kafka REST Proxy via Ingress
base_url = 'http://kafka-plaintext.hsrn.nyu.edu'

def create_consumer(group_id, instance_id, format="json"):
    url = f"{base_url}/consumers/{group_id}"
    body = {
        "name": instance_id,
        "format": format,
        "auto.offset.reset": "earliest"
    }
    headers = {'Content-Type': 'application/vnd.kafka.v2+json',}
    response = requests.post(url, headers=headers, data=json.dumps(body))
    if response.status_code == 200:
        print("Consumer instance created successfully")
        return response.json()
    else:
        print(f"Failed to create consumer instance: {response.text}")
        return None

def subscribe_consumer(group_id, instance_id, topics):
    url = f"{base_url}/consumers/{group_id}/instances/{instance_id}/subscription"
    body = {"topics": topics}
    headers = {'Content-Type': 'application/vnd.kafka.v2+json',}
    response = requests.post(url, headers=headers, data=json.dumps(body))
    if response.status_code == 204:
        print("Subscribed to topic(s) successfully")
    else:
        print(f"Failed to subscribe to topic(s): {response.text}")

def poll_messages(group_id, instance_id):
    url = f"{base_url}/consumers/{group_id}/instances/{instance_id}/records"
    headers = {'Accept': 'application/vnd.kafka.json.v2+json',}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        messages = response.json()
        for message in messages:
            print(f"Received message: {message}")
    else:
        print(f"Failed to poll messages: {response.text}")

def delete_consumer(group_id, instance_id):
    url = f"{base_url}/consumers/{group_id}/instances/{instance_id}"
    response = requests.delete(url)
    if response.status_code == 204:
        print("Consumer instance deleted successfully")
    else:
        print(f"Failed to delete consumer instance: {response.text}")

# Main logic
if __name__ == "__main__":
    group_id = "my-consumer-group"
    instance_id = f"my-instance-{uuid.uuid4()}"
    topics = ["test"]

    consumer_info = create_consumer(group_id, instance_id)
    if consumer_info:
        subscribe_consumer(group_id, instance_id, topics)
        try:
            while True:
                poll_messages(group_id, instance_id)
                time.sleep(1)  # Adjust the sleep time as necessary
        except KeyboardInterrupt:
            print("\nDetected KeyboardInterrupt, deleting consumer instance and exiting...")
            delete_consumer(group_id, instance_id)
