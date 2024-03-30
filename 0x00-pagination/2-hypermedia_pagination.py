#!/usr/bin/env python3
""" Module for class server that implemens pagination """
from typing import Tuple, List
import csv
import math


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """  return a tuple of size two containing a start index and an end index
    corresponding to the range of indexes to return in a list for givrn input
    parameters
    Args:
        page (int): page number to return starts from 1
        page)size (int): size of page
    Return:
        tuple(int, int): contains list index for input value range"""
    start_index = (page - 1) * page_size
    end_index = page * page_size
    return start_index, end_index


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """ instnace init function """
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """ find the correct indexes to paginate the dataset correctly and
        return the appropriate page of the dataset """
        assert type(page) is int and page > 0
        assert type(page_size) is int and page_size > 0
        data = self.dataset()
        length = len(data)
        try:
            index_tuple = index_range(page, page_size)
            return data[index_tuple[0]:index_tuple[1]]
        except IndexError as err:
            return []

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """ returns a dictionary containing the following
            key-value pairs using get page function
            page_size: the length of the returned dataset page
            page: the current page number
            data: the dataset page (equivalent to return from previous task)
            next_page: number of the next page, None if no next page
            prev_page: number of the previous page, None if no previous page
            total_pages: the total number of pages in the dataset as an integer
        """
        data = self.get_page(page, page_size)
        data_set_length = len(self.dataset())
        pages = data_set_length / page_size
        pages = int(pages) if pages % 1 == 0 else int(pages) + 1
        length = len(data)
        return {
                "page_size": length, "page": page, "data": data,
                "next_page": page + 1 if page < pages else None,
                "prev_page": page - 1 if page > 1 else None,
                "total_pages": pages
                }
