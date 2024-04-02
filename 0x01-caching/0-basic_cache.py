#!/usr/bin/env python3
""" Module for class BasicCache """

BaseCaching = __import__("base_caching").BaseCaching


class BasicCache(BaseCaching):
    """ A class that models a basic caching system """
    def __init__(self):
        """ Initilizes an instance of BasicCache class """
        super().__init__()

    def put(self, key, item):
        """ assign to the dictionary self.cache_data the item value
        for the key """
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """ returns the value in self.cache_data linked to key """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
