from confluent_kafka import Consumer, KafkaException
import json

# Kafka consumer configuration
consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'driver-assignment-group',
    'auto.offset.reset': 'earliest',
}

consumer = Consumer(consumer_config)
consumer.subscribe(['order-topic'])

def assign_driver(order_data):
    # Logic to assign a driver based on order details
    print(f"Assigning driver for order: {order_data}")
    # Example: Find a driver and send a notification
    # driver = find_available_driver(order_data)
    # send_notification_to_driver(driver, order_data)

try:
    while True:
        msg = consumer.poll(1.0)  # Timeout of 1 second

        if msg is None:
            continue

        if msg.error():
            if msg.error().code() == KafkaException._PARTITION_EOF:
                continue
            else:
                print(f"Consumer error: {msg.error()}")
                break

        order_data = json.loads(msg.value().decode('utf-8'))
        assign_driver(order_data)
finally:
    consumer.close()
