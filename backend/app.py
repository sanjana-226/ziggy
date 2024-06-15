from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
# app.config['DEBUG'] = True
# app.config['SECRET_KEY'] = 'your_secret_key'

# Enable CORS for all domains on all routes
CORS(app)

from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client.delivery_system

# initialize driver set
# ????

# CRUD operations for order
@app.route('/orders', methods=['GET'])
def get_orders():
    orders = list(db.orders.find())
    for order in orders:
        order["_id"] = str(order["_id"]) 
    return jsonify(orders)

@app.route('/orders', methods=['POST'])
def add_order():
    order = {
        "start_location": request.json['start_location'],
        "end_location": request.json['end_location'],
        "status": "unassigned",
        "delivered": False
    }
    result = db.orders.insert_one(order)
    order["_id"] = str(result.inserted_id)
    return jsonify(order)

# @app.route('/orders/<id>', methods=['PUT'])
# def update_order(id):
#     updated_data = request.json  # Assuming JSON data is sent in the request body
#     del updated_data['_id']
#     db.orders.update_one(
#         {"_id": ObjectId(id)},
#         {"$set": updated_data}
#     )
#     order = db.orders.find_one({"_id": ObjectId(id)})
#     order["_id"] = str(order["_id"])
#     return jsonify(order)

@app.route('/orders/<id>', methods=['DELETE'])
def delete_order(id):
    db.orders.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Order deleted successfully"})

# CRUD operations for drivers
from flask import request, jsonify

@app.route('/drivers', methods=['GET'])
def get_drivers():
    drivers = list(db.drivers.find())
    for driver in drivers:
        driver["_id"] = str(driver["_id"])
    return jsonify(drivers)

@app.route('/drivers', methods=['POST'])
def add_driver():
    driver = {
        "name": request.json['name'],
        "phone": request.json['phone'],
        "current_location": request.json['current_location'],
        "status": "free"
    }
    result = db.drivers.insert_one(driver)
    driver["_id"] = str(result.inserted_id)
    return jsonify(driver)

@app.route('/drivers/<id>', methods=['PUT'])
def update_driver(id):
    db.drivers.update_one(
        {"_id": ObjectId(id)},
        {"$set": request.json}
    )
    driver = db.drivers.find_one({"_id": ObjectId(id)})
    driver["_id"] = str(driver["_id"])
    return jsonify(driver)

@app.route('/drivers/<id>', methods=['DELETE'])
def delete_driver(id):
    db.drivers.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Driver deleted successfully"})


# Assign orders to drivers
import math

def haversine(point1, point2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified as GeoJSON Point objects)
    """
    lon1, lat1 = point1['coordinates']
    lon2, lat2 = point2['coordinates']

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    km = 6371 * c
    return km

def assign_orders():
    orders = db.orders.find({"status": "unassigned"})
    drivers = list(db.drivers.find({"status": "free"}))

    for order in orders:
        if drivers:
            min_distance = None
            nearest_driver = None

            for driver in drivers:
                driver_location = driver["current_location"]
                order_start_location = order["start_location"]

                distance = haversine(driver_location, order_start_location)

                if min_distance is None or distance < min_distance:
                    min_distance = distance
                    nearest_driver = driver

            db.orders.update_one(
                {"_id": order["_id"]},
                {"$set": {"status": "assigned", "driver_id": nearest_driver["_id"]}}
            )
            db.drivers.update_one(
                {"_id": nearest_driver["_id"]},
                {"$set": {"status": "busy"}}
            )
            drivers.remove(nearest_driver)
        else:
            break

# from apscheduler.schedulers.background import BackgroundScheduler
# import time 

# scheduler = BackgroundScheduler()
# scheduler.add_job(assign_orders, 'interval', minutes=1)
# scheduler.start()

# try:
#     while True:
#         time.sleep(2)
# except (KeyboardInterrupt, SystemExit):
#     scheduler.shutdown()


if __name__ == '__main__':
    app.run()