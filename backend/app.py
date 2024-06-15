import time
import threading
import math
import random
from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

CORS(app)

client = MongoClient('mongodb+srv://myAtlasDBUser:H0nuE1gTiBYqFE9s@atlascluster.kydmpyp.mongodb.net/?retryWrites=true&w=majority&appName=AtlasCluster')
db = client.delivery_system

# CRUD operations for order
@app.route('/orders', methods=['GET'])
def get_orders():
    orders = list(db.orders.find())
    for order in orders:
        order["_id"] = str(order["_id"]) 
        if "driver_id" in order:
            order["driver_id"] = str(order["driver_id"])
    return jsonify(orders)

@app.route('/orders', methods=['POST'])
def add_order():
    try:
        start_location = request.json['start_location']
        end_location = request.json['end_location']
        start_lng, start_lat = map(float, start_location.split(','))
        end_lng, end_lat = map(float, end_location.split(','))
        
        order = {
            "start_location": {"type": "Point", "coordinates": [start_lng, start_lat]},
            "end_location": {"type": "Point", "coordinates": [end_lng, end_lat]},
            "status": "unassigned",
            "delivered": False
            
        }
        
        result = db.orders.insert_one(order)
        order["_id"] = str(result.inserted_id)
        
        return jsonify(order), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# fix
@app.route('/orders/<id>', methods=['DELETE'])
def delete_order(id):
    order = db.orders.find_one({"_id": ObjectId(id)})
    if order['status'] == "assigned":
        db.drivers.update_one(
            {"_id": order['driver_id']},
            {"$set": {"status": "free", "current_location": order["start_location"]}}
        )   
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

# scheduling

def finish_jobs():
    print("Finishing jobs...")
    orders_in_progress = list(db.orders.find({"status": "assigned"}))  # Convert cursor to list
    
    num_orders = len(orders_in_progress)
    half_num_orders = num_orders // 2
    if half_num_orders == 0:
        half_num_orders = 1
        
    if(num_orders > 1):
        orders_to_finish = random.sample(orders_in_progress, half_num_orders)
    
    for order in orders_to_finish:
        db.orders.delete_one({"_id": order["_id"]})
        # db.orders.update_one(
        #     {"_id": order["_id"]},
        #     {"$set": {"status": "unassigned", "delivered": True}}
        # )
        db.drivers.update_one(
            {"_id": order["driver_id"]},
            {"$set": {"status": "free", "current_location": order["end_location"]}}
        )
    
    print(f"Finished {len(orders_to_finish)} orders.")

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
    print("Assigning orders...")
    orders = list(db.orders.find({"status": "unassigned"}))
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
            
            print(f"Assigning order {order['_id']} to driver {nearest_driver['_id']}")
            db.orders.update_one(
                {"_id": order["_id"]},
                {"$set": {"status": "assigned", "driver_id": nearest_driver["_id"]}}
            )
            db.drivers.update_one(
                {"_id": nearest_driver["_id"]},
                {"$set": {"status": "busy", "current_location": order["start_location"]}}
            )
            drivers.remove(nearest_driver)
        else:
            break

scheduler = BackgroundScheduler()
scheduler.add_job(assign_orders, 'interval', seconds=60)
scheduler.add_job(finish_jobs, 'interval', seconds=30)
scheduler.start()

def flask_runner():
    app.run()

if __name__ == '__main__':
    flask_thread = threading.Thread(target=flask_runner)
    flask_thread.start()

    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        flask_thread.join() 


# more sophisticated location algorithm

# def update_driver_locations():
#     print("Updating driver locations...")
#     orders = db.orders.find({"status": "assigned"})
    
#     for order in orders:
#         driver = db.drivers.find_one({"_id": order["driver_id"]})
#         driver_location = driver["current_location"]
#         order_end_location = order["end_location"]
        
#         # Calculate distance between current driver location and order end location
#         distance = haversine((driver_location["coordinates"][1], driver_location["coordinates"][0]),
#                              (order_end_location["coordinates"][1], order_end_location["coordinates"][0]),
#                              unit=Unit.KILOMETERS)
#         print(f"Distance: {distance}")
#         if distance > 1:  # Only update if the distance is greater than 1 km
#             # Define latitude and longitude of current and end locations
#             lat1 = math.radians(driver_location["coordinates"][1])
#             lon1 = math.radians(driver_location["coordinates"][0])
#             lat2 = math.radians(order_end_location["coordinates"][1])
#             lon2 = math.radians(order_end_location["coordinates"][0])
            
#             # Calculate bearing
#             dlon = lon2 - lon1
#             bearing = math.atan2(math.sin(dlon) * math.cos(lat2),
#                                  math.cos(lat1) * math.sin(lat2) - 
#                                  math.sin(lat1) * math.cos(lat2) * 
#                                  math.cos(dlon))
            
#             # Calculate new latitude and longitude based on speed and bearing
#             speed = 150  # km/h
#             distance_to_move = (speed / 3600) * (distance * 1000) / 6371  # Convert km/h to km/s
#             new_lat = math.degrees(math.asin(math.sin(lat1) * math.cos(distance_to_move) +
#                                              math.cos(lat1) * math.sin(distance_to_move) * math.cos(bearing)))
#             new_lon = math.degrees(lon1 + math.atan2(math.sin(bearing) * math.sin(distance_to_move) * math.cos(lat1),
#                                                       math.cos(distance_to_move) - math.sin(lat1) * math.sin(lat2)))
            
#             # Update driver's current location in the database
#             db.drivers.update_one(
#                 {"_id": order["driver_id"]},
#                 {"$set": {"current_location": {"type": "Point", "coordinates": [new_lon, new_lat]}}}
#             )
#             print(f"Driver {driver._id} updated location to: {new_lat}, {new_lon}")


# def finish_jobs():
#     print("Finishing jobs...")
#     orders = db.orders.find({"status": "assigned"})

#     for order in orders:
#         driver = db.drivers.find_one({"_id": order["driver_id"]})
        
#         driver_location = driver["current_location"]
#         order_end_location = order["end_location"]
        
#         if haversine((driver_location["coordinates"][1], driver_location["coordinates"][0]), (order_end_location["coordinates"][1], order_end_location["coordinates"][0]), unit=Unit.KILOMETERS) <1:
#             print(order)
#             db.orders.update_one(
#                 {"_id": order["_id"]},
#                 {"$set": {"status": "unassigned", "delivered": True}}
#             )
#             db.drivers.update_one(
#                 {"_id": order["driver_id"]},
#                 {"$set": {"status": "free", "current_location": order["end_location"]}}
#             )
