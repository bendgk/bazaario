from pymongo import MongoClient
import time

if __name__ == "__main__":
    #MongoDB setup
    client = MongoClient()
    #client = MongoClient('mongodb://python:!SuperPythonPassword@localhost:27017/')

    #bazaar listings
    db = client["bazaar"]
    bazaar = db["listings"]
    
    #price ticker   (10s, 1m, 5m, 15m, 30m, 1h, 4h, 12h, 1d)

    tickers = {
        '10s': (client["tickers_10s"], []),
        '1m': (client["tickers_1m"], []),
        '5m': (client["tickers_5m"], []),
        '15m': (client["tickers_15m"], []),
        '30m': (client["tickers_30m"], []),
        '1h': (client["tickers_1h"], []),
        '4h': (client["tickers_4h"], []),
        '12h': (client["tickers_12h"], []),
        '1d': (client["tickers_1d"], [])
    }

    u = input("Drop DBs? (y/n)")
    if u.lower() == "y":
        for k, v in tickers.items():
            print(f"Dropping {k}_db!")
            client.drop_database(v[0].name)
            print(v[0].name)
    
    doc = bazaar.find_one()

    #time setup
    time_started = time.time()
    last_updated = doc["lastUpdated"]

    if int(time_started) > last_updated + 15:
        print("Error: `ticker.py` is not running!\nexiting now...")
        exit()

    #todo pickup here
    while True:
        try:
            doc = bazaar.find_one()b


    while True:
        try:
            doc = bazaar.find_one()
            listings = doc["products"]

            if last_updated < doc["lastUpdated"]:
                last_updated = doc["lastUpdated"]
            else:
                time.sleep(.1)
                continue

            for product, data in listings.items():
                try:
                    d = {
                        "time": int(doc["lastUpdated"]/1000),
                        "bid_price": data["sell_summary"][0]["pricePerUnit"],
                        "ask_price": data["buy_summary"][0]["pricePerUnit"],
                        "sell_orders": data["quick_status"]["sellOrders"],
                        "buy_orders": data["quick_status"]["buyOrders"],
                        "sell_volume": data["quick_status"]["sellVolume"],
                        "buy_volume": data["quick_status"]["buyVolume"],
                    }
                except:
                    continue
                

                ticker_db[product].insert_one(d)

        except:
            pass

        time.sleep(1)
