import time
import json
from confluent_kafka import Producer
import socket

# Producer Configuration
conf = {
    'bootstrap.servers': 'localhost:9092',  # Kafka Broker Address
    'client.id': socket.gethostname()
}

# Create Producer instance
producer = Producer(conf)

topic_name = 'test_topic'

def delivery_callback(err, msg):
    """
    Callback called once the message has been successfully delivered (or failed).
    """
    if err:
        print(f'Message delivery error: {err}')
    else:
        print(f'Message sent to: {msg.topic()} [Partition: {msg.partition()}] @ offset {msg.offset()}')

def main():
    print(f"--- Starting Kafka Producer for topic '{topic_name}' ---")
    print("Press Ctrl+C to stop.")

    counter = 0
    try:
        while True:
            # Create an example message (JSON)
            data = {
                'id': counter,
                'message': f'This is message number {counter}',
                'timestamp': time.time()
            }
            
            # Serialize to JSON and encode to bytes
            value_bytes = json.dumps(data).encode('utf-8')
            key_bytes = str(counter).encode('utf-8') # The key determines the partition

            # Asynchronous send
            producer.produce(
                topic_name, 
                key=key_bytes, 
                value=value_bytes, 
                callback=delivery_callback
            )

            # Poll serves to handle delivery callbacks
            producer.poll(0)
            
            counter += 1
            time.sleep(2) # Send a message every 2 seconds

    except KeyboardInterrupt:
        print("\nInterruption requested by user.")
    finally:
        # Ensure all queued messages are sent before closing
        print("Waiting for remaining messages to be sent...")
        producer.flush()
        print("Producer closed.")

if __name__ == '__main__':
    main()