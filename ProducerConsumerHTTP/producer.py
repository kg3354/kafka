import requests
import json
import datetime

def produce_message(topic_name, message):
    # Kafka REST Proxy URL configured to use the Ingress
    rest_proxy_url = f'http://kafka-plaintext.hsrn.nyu.edu/topics/{topic_name}'

    # Headers for the request indicating JSON content
    headers = {
        'Content-Type': 'application/vnd.kafka.json.v2+json',
    }

    # Append the current timestamp to the message
    timestamp = datetime.datetime.now().isoformat()
    message_with_timestamp = message + f" at {timestamp}"

    # The message payload
    data = {
        "records": [
            {"value": message_with_timestamp}
        ]
    }

    # Sending the message
    response = requests.post(rest_proxy_url, headers=headers, data=json.dumps(data))

    # Checking response status
    if response.status_code == 200:
        print("Message produced successfully")
    else:
        print(f"Failed to produce message: {response.text}")

if __name__ == "__main__":
    try:
        topic_name = input("Enter the topic name (or type 'exit' to quit): ")
        while True:
            message = input("Enter your message: ")
            produce_message(topic_name, message)
    except KeyboardInterrupt:
        print("\nDetected KeyboardInterrupt, exiting...")
