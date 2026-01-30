# Apache Kafka with Python: Introductory Example

This repository contains a complete development environment for experimenting with Apache Kafka. It includes the infrastructure (via Docker) and Python scripts to produce and consume messages.

## Key Concepts

Before starting, here is a quick review of the fundamental concepts:

- Broker: The Kafka server itself. It receives, stores, and distributes messages.

- Topic: A category or feed where messages are stored (similar to a table in a database or a folder in a filesystem).

- Producer: The application that sends (publishes) messages to a Kafka topic.

- Consumer: The application that reads (subscribes to) messages from a topic.

- Partition: A topic is divided into partitions to parallelize work. Kafka guarantees message order only within a single partition.

- Offset: A unique sequential identifier assigned to each message within a partition. The Consumer tracks its "offset" to know which messages it has already read.

- Consumer Group: A group of consumers that work together to read a topic. If you have 3 partitions and 3 consumers in the same group, each consumer will read from only one partition.

## Prepare the environment

### Prerequisites

Docker and Docker Compose installed.

Python 3.8+ installed.

### Install Python Dependencies

It is recommended to create a virtual environment:

#### Create env
    
    python -m venv kafka_env
#### Activate env (Windows)
    kafka_env\Scripts\activate
#### Activate env (Mac/Linux)
    source kafka_env/bin/activate

#### Install library
    python -m pip install -r requirements.txt

## Star the Example

### Start Kafka

Start Zookeeper, Kafka, and the management UI with a single command:

    docker-compose up -d

Verify: With docker ps you should see the kafka, zookeeper, and kafka-ui containers in "Up" state

### Kafka UI

Once the containers are started, open your browser at the address to access Kafka-UI:

    http://localhost:8080

Here you will find Kafka UI, a powerful dashboard where you can:

- See created Topics and create new ones.

- Explore Messages within topics in real-time.

- Check the state of Consumer Groups.

### Run the Scripts

Open another Terminal (The Producer) start the producer to generate traffic.

    python producer.py


You will see the producer sending JSON messages.

Open a Terminal (The Consumer) start the consumer first so it is ready to receive.

    python consumer.py


You will see the consumer , almost instantly, receiving and printing them to the screen in the first terminal.

## Shutting town things 

To stop everything and remove volumes (complete cleanup of Kafka data):

docker-compose down -v


## What's happening in the code?

The Producer serializes a Python dictionary into JSON format, converts it to bytes, and sends it to the test_topic.

The Consumer is configured with auto.offset.reset='earliest', which means that if it is connecting for the first time, it will read all available messages from the beginning of the topic's history.