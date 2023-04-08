from pymongo import MongoClient



def get_mongodb_collection(collection: str):
    
    myclient = MongoClient("mongodb://localhost:27017/")

    db = myclient["twitter"]
    mongodb_collection = db[collection]

    return mongodb_collection