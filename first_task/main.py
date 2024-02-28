from mongoengine import Document, StringField, ReferenceField, ListField, connect
import json
from mongoengine.errors import NotUniqueError

class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    quote = StringField(required=True)
    tags = ListField(StringField())
    author = ReferenceField(Author)

def load_data_to_database():
    mongo_uri = "mongodb+srv://artur:7464383521@atlascluster.mzincq8.mongodb.net/"
    database_name = "2web8"

    connect(host=mongo_uri, db=database_name)

    # Завантаження авторів
    with open('C:\\Projects\\web.8\\first_task\\authors.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        for el in data:
            try:
                author = Author(fullname=el.get('fullname'), born_date=el.get('born_date'),
                                born_location=el.get('born_location'), description=el.get('description'))
                author.save()
            except NotUniqueError:
                print(f"Автор вже існує {el.get('fullname')}")

    # Завантаження цитат
    with open('C:\\Projects\\web.8\\first_task\\quotes.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        for el in data:
            author, *_ = Author.objects(fullname=el.get('author'))
            quote = Quote(quote=el.get('quote'), tags=el.get('tags'), author=author)
            quote.save()

def search_quotes():
    while True:
        command = input("Введіть команду: ").strip()

        if command.startswith("name:"):
            author_name = command.split(":")[1].strip()
            author = Author.objects.get(fullname=author_name)
            quotes = Quote.objects(author=author)
            for quote in quotes:
                print((f"Автор: {quote.author.fullname}, Цитата: {quote.quote}"))

        elif command.startswith("tag:"):
            tag = command.split(":")[1].strip()
            quotes = Quote.objects(tags=tag)
            for quote in quotes:
                print(f"Теги: {tag}, Цитата: {quote.quote}")

        elif command.startswith("tags:"):
            tags = command.split(":")[1].strip().split(",")
            quotes = Quote.objects(tags__in=tags)
            for quote in quotes:
                print(f"Теги: {tags}, Цитата: {quote.quote}")

        elif command == "exit":
            break

        else:
            print("Невідома команда. Спробуйте ще раз.")

if __name__ == "__main__":
    load_data_to_database()
    search_quotes()