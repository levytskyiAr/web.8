import pika
from faker import Faker
from mongoengine import connect, Document, StringField, BooleanField
from bson import ObjectId

mongo_uri = "mongodb+srv://artur:7464383521@atlascluster.mzincq8.mongodb.net/"
database_name = "web8"

connect(host=mongo_uri, db=database_name)

class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)

def produce_contacts():
    fake = Faker()
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='email_queue')

    for _ in range(5):
        contact = Contact(
            full_name=fake.name(),
            email=fake.email()
        ).save()

        message = str(contact.id)
        channel.basic_publish(exchange='', routing_key='email_queue', body=message)

        print(f"Контакт створено: {contact.full_name}, Email: {contact.email}")

    connection.close()

if __name__ == "__main__":
    produce_contacts()