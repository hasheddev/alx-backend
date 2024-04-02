#!/usr/bin/env python3
""" Module for class LRUCache """

BaseCaching = __import__("base_caching").BaseCaching


class LRUCache(BaseCaching):
    """ A class that models a LRU caching system """
    def __init__(self):
        """ Initilizes an instance of LRUCache class """
        super().__init__()
        self.least_recent_used = {}
        self.maximum = 0

    def put(self, key, item):
        """ assign to the dictionary self.cache_data the item value
        for the key """
        if key is None or item is None:
            return
        self.cache_data[key] = item
        if key not in self.least_recent_used:
            self.set_time_max(key)
        else:
            self.least_recent_used[key] = self.maximum + 1
            self.maximum += 1
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            self.del_least_recent_time()

    def set_time_max(self, key):
        """ sets time for most recently accessd key """
        if len(self.least_recent_used) == 0:
            self.least_recent_used[key] = self.maximum = 0
            return
        self.least_recent_used[key] = self.maximum = self.maximum + 1

    def del_least_recent_time(self):
        """ Deletes least recently used data in a cache """
        minimum = self.maximum
        min_key = None
        for key, value in self.least_recent_used.items():
            if value < minimum:
                minimum = value
                min_key = key
        del self.least_recent_used[min_key]
        del self.cache_data[min_key]
        print(f"DISCARD: {min_key}")

    def get(self, key):
        """ returns the value in self.cache_data linked to key """
        if key is None or key not in self.cache_data:
            return None
        self.least_recent_used[key] = self.maximum = self.maximum + 1
        return self.cache_data[key]
