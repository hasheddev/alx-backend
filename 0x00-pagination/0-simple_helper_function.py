#!/usr/bin/env python3
""" Module for helper function index_range """
from typing import Tuple


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
