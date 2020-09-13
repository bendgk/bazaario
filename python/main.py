from pymongo import MongoClient
import time

if __name__ == "__main__":
    #MongoDB setup
    client = MongoClient()
    client = MongoClient('mongodb://localhost:27017/')
    db = client["bazaar"]

    bazaar = db["listings"]
    
    #price ticker   (5s, 30s, 1m, 5m, 15m, 30m, 1h, 4h, 12h, 1d)
    ticker_db = client["tickers"]
    last_updated = 0

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
                        "time": doc["lastUpdated"],
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

        time.sleep(.1)