#!/usr/bin/env python3
"""function that changes all topics of a school document based on the name"""


def update_topics(mongo_collection, name, topics):
    """
    mongo_collection - pymongo collection object
    name (string) - school name to update
    topics (list of strings) - topics approached in the school
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
