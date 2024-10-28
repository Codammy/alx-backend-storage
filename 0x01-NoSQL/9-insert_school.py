#!/usr/bin/env python3
"""
Python function that
inserts a new document in a collection based on kwargs
"""
from pymongo.collection import Collection
from typing import Any, Dict


def insert_school(mongo_collection: Collection,
                  **kwargs: Dict[Any, Any]) -> str:
    """inserts a new document in a collection based on kwargs"""

    return mongo_collection.insert_one(kwargs).inserted_id
