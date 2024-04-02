#!/usr/bin/env python3
""" Module for class FIFOCache """

BaseCaching = __import__("base_caching").BaseCaching


class FIFOCache(BaseCaching):
    """ A class that models a FIFO caching system """
    def __init__(self):
        """ Initilizes an instance of FIFOCache class """
        super().__init__()
        self.cache_keys = []

    def put(self, key, item):
        """ assign to the dictionary self.cache_data the item value
        for the key """
        if key is None or item is None:
            return
        self.cache_data[key] = item
        length = len(self.cache_data)
        if length > BaseCaching.MAX_ITEMS:
            print(f"DISCARD: {self.cache_keys[0]}")
            del self.cache_data[self.cache_keys[0]]
            self.cache_keys.remove(self.cache_keys[0])
        if key in self.cache_keys:
            self.cache_keys.remove(key)
        self.cache_keys.append(key)

    def get(self, key):
        """ returns the value in self.cache_data linked to key """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
