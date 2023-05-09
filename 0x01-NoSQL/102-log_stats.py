#!/usr/bin/env python3
"""script that provides some stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient


if __name__ == "__main__":
    """script that provides some stats about Nginx logs stored in MongoDB"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    num_logs = logs_collection.count_documents({})
    print(f'{num_logs} logs')

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print('Methods:')
    for method in methods:
        method_count = logs_collection.count_documents({"method": method})
        print(f'\tmethod {method}: {method_count}')

    status = logs_collection.count_documents(
            {"method": "GET", "path": "/status"})
    print(f'{status} status check')
    print('IPs:')

    sorting_ip = logs_collection.aggregate([
        {"$group":
            {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
         },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}])
    for top in sorting_ip:
        ip = top.get("ip")
        count = top.get("count")
        print(f"\t{ip}: {count}")
