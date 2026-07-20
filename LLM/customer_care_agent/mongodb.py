from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017")
db = client["token_meter"]
collection = db["data"]

def insert_order(data: dict):
    result = collection.insert_one(data)
    print(f"inserted data to ID: {result.inserted_id}")
    return str(result.inserted_id)
def delete_order(order_id: str) -> str:    
    result = collection.delete_one({"order_id": order_id})
    return(f"Deleted {result.deleted_count} document(s) with order_id: {order_id}")