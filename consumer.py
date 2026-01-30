import json
from confluent_kafka import Consumer, KafkaError, KafkaException
import sys

# Consumer Configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'python_example_group_1', # Consumers with the same ID share the load
    'auto.offset.reset': 'earliest'       # If no offset is saved, start from the beginning
}

consumer = Consumer(conf)
topic_name = 'test_topic'

def main():
    try:
        consumer.subscribe([topic_name])
        print(f"--- Starting Kafka Consumer listening on '{topic_name}' ---")
        print("Waiting for messages... (Press Ctrl+C to exit)")

        while True:
            # Poll(timeout): waits for messages for X seconds
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue
            
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition reached (this is not a critical error)
                    continue
                else:
                    raise KafkaException(msg.error())
            
            # Process message
            try:
                # Decode payload
                value = msg.value().decode('utf-8')
                key = msg.key().decode('utf-8') if msg.key() else None
                
                # JSON Parsing (optional, depends on what the producer sends)
                data = json.loads(value)
                
                print(f"Received [Key: {key}]: {data}")
                
            except Exception as e:
                print(f"Error parsing message: {e}")

    except KeyboardInterrupt:
        print("\nInterruption requested.")
    finally:
        # Cleanly close the connection and commit final offsets
        consumer.close()
        print("Consumer closed.")

if __name__ == '__main__':
    main()