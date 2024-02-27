import pika
from mongoengine import connect, Document, StringField, BooleanField
from bson import ObjectId

mongo_uri = "mongodb+srv://artur:7464383521@atlascluster.mzincq8.mongodb.net/"
connect(host=mongo_uri)

class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)

def send_email_and_update_contact(contact_id):
    contact = Contact.objects.get(id=ObjectId(contact_id.decode()))
    print(f"Імітація надсилання електронної пошти на: {contact.email}")
    Contact.message_sent = True
    Contact.save()

def callback(body):
    print(f"Отримано повідомлення: {body}")
    send_email_and_update_contact(body)

def consume_messages():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='email_queue')

    channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

    print("Очікування повідомлень. Для виходу натисніть Ctrl+C")
    channel.start_consuming()

if __name__ == "__main__":
    consume_messages()