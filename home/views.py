from django.shortcuts import render
import pymongo
import datetime

# Create your views here.

def connection():
    # Connect to the MongoDB, change the connection string per your MongoDB environment
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    print(client)

    # Set the db object to point to the business database
    db = client['test_db']
    collection = db['test_collection']

    dictionary = {'name': 'Test Name', 'age': 30, 'created_at': datetime.datetime.utcnow()}
    collection.insert_one(dictionary)

    # Showcasing the count() method of find, count the total number of documents in collection
    print('Total number of documents in collection: ', collection.count_documents({}))


def home(request):
    connection()
    return render(request, 'home.html')
