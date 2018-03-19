import json
import pika

class CloudAMQPClient:
    def __init__(self, cloud_amqp_url, queue_name):
        self.cloud_amqp_url = cloud_amqp_url
        self.queue_name = queue_name
        self.params = pika.URLParameters(cloud_amqp_url) # used by pika.BlockingConnection()
        self.params.socket_timeout = 3                   # further set the params for pika
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()         # open a channel whenever there comes a publisher/consumer
        self.channel.queue_declare( queue=queue_name )

    # send a message to a queue
    def sendMessage(self, message):
        self.channel.basic_publish(exchange='',
                                   routing_key = self.queue_name,
                                   body = json.dumps(message))
        print "[X] Sent message to %s : %s" % (self.queue_name, message)

    # get a message from queue
    def getMessage(self):
        method_frame, header_frame, body = self.channel.basic_get(self.queue_name)
        if method_frame is not None:
            print "[O] Received message from %s : %s" % (self.queue_name, body)
            self.channel.basic_ack(method_frame.delivery_tag) # ack the queue that the msg has been consumed, you can delete it
            return json.loads(body)
        else:
            print "No message returned"
            return None

    # sleep: used to control the visit-frequency of scraping
    def sleep(self, seconds):
        self.connection.sleep(seconds)
