#!/usr/bin/env python3
"""function that lists all documents in a collection"""


def list_all(mongo_collection):
    """Lists all documents"""
    return mongo_collection.find()
