from confluent_kafka import Consumer, Producer, KafkaError
import os
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger(__name__).setLevel('INFO')

KAFKA_HOST = os.environ.get('KAFKA_HOST')

class BaseConsumer(Consumer):
    MAX_RETRIES = 3

    def __init__(self):
        self.KAFKA_HOST = KAFKA_HOST
        self.TOPICS = ['mytopic']
        settings = {
            'bootstrap.servers': KAFKA_HOST,
            'group.id': 'mygroup'
        }
        logging.info('initialize consumer')
        super().__init__(settings)

    def start(self):
        logging.info(f'Consuming messages from {self.KAFKA_HOST} topics: {self.TOPICS}')
        try:
            self.subscribe(self.TOPICS)
            while True:
                self.poll_for_messages()
        except Exception as e:
            logging.info(f'Error: {e}')

    def poll_for_messages(self):
        try:
            msg = self.poll(timeout=0.1)
        except Exception as e:
            logging.debug(f'Error: {e}')
            return

        if msg is None:
            return
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                logging.debug(f'End of partition reached {msg.topic()}/{msg.partition()}')
            else:
                logging.debug('Error')
            return

        return msg

    # TODO: Move this function to Producer
    def publish_message(self, topic, message, timeout=5):
        try:
            p = Producer({'bootstrap.servers': self.KAFKA_HOST})
            p.produce(topic, value=message)
            p.flush(timeout)
        except Exception as e:
            logging.info(f'Error: {e}')

if __name__ == "__main__":
    BaseConsumer().start()

