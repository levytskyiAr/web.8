from mongoengine import Document, StringField, ReferenceField, ListField, connect
import json

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
        authors_data = json.load(file)
        for author_data in authors_data:
            Author(**author_data).save()

    # Завантаження цитат
    with open('C:\\Projects\\web.8\\first_task\\quotes.json', 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author_name = quote_data.pop('author')
            author = Author.objects.filter(fullname=author_name).first()
            if author is not None:
                quote_data['author'] = author
                Quote(**quote_data).save()
            else:
                print(f"Автор з ім'ям '{author_name}' не знайдений.")

def search_quotes():
    while True:
        command = input("Введіть команду: ").strip()

        if command.startswith("name:"):
            author_name = command.split(":")[1].strip()
            author = Author.objects.get(fullname=author_name)
            quotes = Quote.objects(author=author)
            for quote in quotes:
                print(quote)

        elif command.startswith("tag:"):
            tag = command.split(":")[1].strip()
            quotes = Quote.objects(tags=tag)
            for quote in quotes:
                print(quote)

        elif command.startswith("tags:"):
            tags = command.split(":")[1].strip().split(",")
            quotes = Quote.objects(tags__in=tags)
            for quote in quotes:
                print(quote)

        elif command == "exit":
            break

        else:
            print("Невідома команда. Спробуйте ще раз.")

if __name__ == "__main__":
    load_data_to_database()
    search_quotes()