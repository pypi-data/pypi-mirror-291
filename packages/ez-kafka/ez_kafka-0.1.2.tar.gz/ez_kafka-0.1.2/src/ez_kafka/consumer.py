import sys
from types import FunctionType

from confluent_kafka import Consumer, KafkaError, KafkaException


KAFKA_CONFIG = {
    'bootstrap.servers': 'localhost:9094',
    'auto.offset.reset': 'smallest',
    'group.id': 'user_group'
}

class EZ_Consumer:
    def __init__(self, filter_by_key: str|None, topics: list, runner: FunctionType) -> None:
        self.filter_by_key = filter_by_key
        self.topics = topics
        self.consumer = Consumer(KAFKA_CONFIG)
        self.consumer.subscribe(self.topics)
        self.runner = runner

    def listen(self):
        print('Listening...')
        try:
            self._run()
        finally:
            self.consumer.close()

    def _run(self):
        while True:
            message = self.consumer.poll(timeout=1.0)
            if message is None: 
                continue
            if message.error():
                if not message.error().code() == KafkaError._PARTITION_EOF:
                    raise KafkaException(message.error())
                # end of partition event
                sys.stderr.write(f'{message.topic()} [{message.partition()}] reached end at offset {message.offset()}\n')
            else:
                key = message.key().decode('utf-8')
                if self.filter_by_key is not None and key != self.filter_by_key:
                    continue
                message = message.value().decode('utf-8')
                self.runner(key, message)
