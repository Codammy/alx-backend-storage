#!/usr/bin/env python3
"""
Python function that lists all documents in a collection
"""
from pymongo import MongoClient
from typing import List, Dict


def list_all(mongo_collection) -> List[Dict]:
    """lists all documents in a collection"""

    all_doc = mongo_collection.find().to_list()
    return all_doc if len(all_doc) > 0 else []