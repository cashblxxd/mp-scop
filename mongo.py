import pymongo
from pprint import pprint
import secrets


def user_exist(username, password):
    client = pymongo.MongoClient("mongodb+srv://dbUser:qwep-]123p=]@cluster0-ifgr4.mongodb.net/Cluster0?retryWrites=true&w=majority")
    return not (client.users.usernames.find_one({
        'username': username,
        'password': password
    }) is None)


def user_create(username, password):
    client = pymongo.MongoClient("mongodb+srv://dbUser:qwep-]123p=]@cluster0-ifgr4.mongodb.net/Cluster0?retryWrites=true&w=majority")
    data = {
        'username': username,
        'password': password,
        "ozon_apikey": "",
        "client_id": ""
    }
    client.users.usernames.insert_one(data)
    data.pop("_id")
    return True, data


def username_taken(username):
    client = pymongo.MongoClient("mongodb+srv://dbUser:qwep-]123p=]@cluster0-ifgr4.mongodb.net/Cluster0?retryWrites=true&w=majority")
    return not (client.users.usernames.find_one({
        'username': username,
    }) is None)


def get_data(username):
    client = pymongo.MongoClient("mongodb+srv://dbUser:qwep-]123p=]@cluster0-ifgr4.mongodb.net/Cluster0?retryWrites=true&w=majority")
    return not (client.users.user_data.find_one({
        'username': username
    }) is None)


def put_confirmation_token(username, password):
    token = secrets.token_urlsafe()
    client = pymongo.MongoClient("mongodb+srv://dbUser:qwep-]123p=]@cluster0-ifgr4.mongodb.net/Cluster0?retryWrites=true&w=majority")
    client.users.confirmation_tokens.insert_one({
        'token': token,
        'username': username,
        'password': password
    })
    return token


def get_confirmation_token(token):
    client = pymongo.MongoClient("mongodb+srv://dbUser:qwep-]123p=]@cluster0-ifgr4.mongodb.net/Cluster0?retryWrites=true&w=majority")
    data = client.users.confirmation_tokens.find_one({
        'token': token
    })
    if data is None:
        return False, 'Not found'
    username, password = data["username"], data["password"]
    client.users.confirmation_tokens.delete_one(data)
    return True, (username, password)
'''
def
db = client["Database0"]
collection = db["Collection0"]
inserted_id = collection.insert_one({
    "user_id": 2,
    "client_id": 836,
    "api_key": "y72g8e87q3us8f9es-dawdyduyegus"
}).inserted_id
print(db.list_collection_names())
pprint(collection.find_one())
pprint(collection.find_one({"_id": inserted_id}))'''