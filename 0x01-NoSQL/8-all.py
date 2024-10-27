#!/usr/bin/env python3
"""
Python function that lists all documents in a collection
"""
from pymongo import MongoClient
from typing import List, Dict


def list_all(mongo_collection) -> List[Dict]:
    """lists all documents in a collection"""

    doc_lst = []
    all_doc = mongo_collection.find()
    for d in all_doc:
        doc_lst.append(d)
    return doc_lst if len(doc_lst) > 0 else []
