# write a simple script to populate the database with some data in json files.
import json
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.delivery_system

# empty the db
db.orders.delete_many({})
db.drivers.delete_many({})

orders_addr = 'backend/orders.json'
drivers_addr = 'backend/drivers.json'
# populate the db
with open('orders.json') as f:
    orders = json.load(f)
    db.orders.insert_many(orders)
    
with open('drivers.json') as f:
    drivers = json.load(f)
    db.drivers.insert_many(drivers) 