#!/usr/bin/env python3
""" Module for class MRUCache """

BaseCaching = __import__("base_caching").BaseCaching


class MRUCache(BaseCaching):
    """ A class that models a MRU caching system """
    def __init__(self):
        """ Initilizes an instance of MRUCache class """
        super().__init__()
        self.recent_key = None

    def put(self, key, item):
        """ assign to the dictionary self.cache_data the item value
        for the key """
        if key is None or item is None:
            return
        if key in self.cache_data:
            self.cache_data[key] = item
            self.recent_key = key
        else:
            self.cache_data[key] = item
            if len(self.cache_data) > BaseCaching.MAX_ITEMS:
                print(f"DISCARD: {self.recent_key}")
                del self.cache_data[self.recent_key]
            self.recent_key = key

    def get(self, key):
        """ returns the value in self.cache_data linked to key """
        if key is None or key not in self.cache_data:
            return None
        self.recent_key = key
        return self.cache_data[key]
