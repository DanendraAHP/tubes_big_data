from random import randrange
from time import sleep
from kafka import KafkaProducer


producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x:
                         x.encode('utf-8'))
test_values = [{
        'video_id':'abc',
        'description' : 'test_abc',
        'published_at' : '2020-02-23'
    },
    {
        'video_id':'def',
        'description' : 'test_def',
        'published_at' : '2020-02-23'
    },
    {
        'video_id':'ghi',
        'description' : 'test_ghi',
        'published_at' : '2020-02-23'
    },
    {
        'video_id':'jkl',
        'description' : 'test_jkl',
        'published_at' : '2020-02-23'
    },
    {
        'video_id':'mno',
        'description' : 'test_mno',
        'published_at' : '2020-02-23'
    }]

#loop till the end of time
while True:
    idx = randrange(len(test_values))
    message = test_values[idx]
    producer.send('test-api', value=message)
    sleep(2)