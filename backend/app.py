from eve import Eve

app = Eve(settings='settings.py')

if __name__ == '__main__':
    app.run(debug=True)

from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client.delivery_system

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

from apscheduler.schedulers.background import BackgroundScheduler
import time 

scheduler = BackgroundScheduler()
scheduler.add_job(assign_orders, 'interval', minutes=1)
scheduler.start()

try:
    while True:
        time.sleep(2)
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
