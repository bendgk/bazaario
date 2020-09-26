import requests, time
from pymongo import MongoClient

__API_KEY = "aadf262b-1aa4-4e77-9d3b-060afccf6fff"
__URL = "https://api.hypixel.net"

def get_bazar_listings():
    while True:
        try:
            r = requests.get( __URL + "/skyblock/bazaar", params = {"key": __API_KEY} )
            return r.json()
        except:
            continue

if __name__ == "__main__":
    #MongoDB setup
    client = MongoClient()
    client = MongoClient('mongodb://python:!SuperPythonPassword@localhost:27017/')

    db = client["bazaar"]
    bazaar = db["listings"]

    if "listings" not in db.list_collection_names():
        #initial listing
        listings = get_bazar_listings()
        doc_id = bazaar.insert_one(listings).inserted_id
    
    else:
        doc_id = bazaar.find_one()['_id']

    prev_listings = None

    while True:
        time.sleep(1)
        listings = get_bazar_listings()
        
        if listings != prev_listings
            bazaar.find_one_and_replace({"_id": doc_id}, listings)
            prev_listings = listings
