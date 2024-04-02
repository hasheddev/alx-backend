#!/usr/bin/env python3
""" Module for class LFUCache """

BaseCaching = __import__("base_caching").BaseCaching


class LFUCache(BaseCaching):
    """ A class that models a LFU caching system """
    def __init__(self):
        """ Initilizes an instance of LFUCache class """
        super().__init__()
        self.least_recent_used = {}
        self.frequency = {}
        self.maximum = 0
        self.max_freq = 0

    def put(self, key, item):
        """ assign to the dictionary self.cache_data the item value
        for the key """
        if key is None or item is None:
            return
        if key in self.cache_data:
            self.cache_data[key] = item
            self.least_recent_used[key] = self.maximum = self.maximum + 1
            self.frequency[key] += 1
            if self.frequency[key] > self.max_freq:
                self.max_freq = self.frequency[key]
        else:
            self.cache_data[key] = item
            self.frequency[key] = 0
            self.set_time_max(key)
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            self.del_least_frequent(key)

    def del_least_frequent(self, recent_key):
        """ Deletes least frequently used item from cache """
        frequency = self.max_freq
        min_frequency = 0
        least_accessed = []
        for key, value in self.frequency.items():
            if key != recent_key and value < frequency:
                min_frequency = value
        for key, value in self.frequency.items():
            if key != recent_key and value == min_frequency:
                least_accessed.append(key)
        if len(least_accessed) == 1:
            del self.cache_data[least_accessed[0]]
            del self.frequency[least_accessed[0]]
            del self.least_recent_used[least_accessed[0]]
            print(f"DISCARD: {least_accessed[0]}")
        else:
            self.del_least_recent_time(least_accessed)

    def set_time_max(self, key):
        """ sets time for most recently accessd key """
        if len(self.least_recent_used) == 0:
            self.least_recent_used[key] = self.maximum = 0
            return
        self.least_recent_used[key] = self.maximum = self.maximum + 1

    def del_least_recent_time(self, least_accessed):
        """ Deletes least recently used data in a cache """
        minimum = self.least_recent_used[least_accessed[0]]
        min_key = least_accessed[0]
        for key in least_accessed:
            if self.least_recent_used[key] < minimum:
                minimum = value
                min_key = key
        del self.least_recent_used[min_key]
        del self.cache_data[min_key]
        del self.frequency[min_key]
        print(f"DISCARD: {min_key}")

    def get(self, key):
        """ returns the value in self.cache_data linked to key """
        if key is None or key not in self.cache_data:
            return None
        self.least_recent_used[key] = self.maximum = self.maximum + 1
        self.frequency[key] += 1
        if self.max_freq < self.frequency[key]:
            self.max_freq = self.frequency[key]
        return self.cache_data[key]
