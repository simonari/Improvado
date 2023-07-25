import os

import csv
import json
from datetime import datetime

from collections import OrderedDict
from types import GeneratorType


class Process:
    """
    Class to process data chunks of friends list.\n
    Processes data in specified by VK.API format and returns data represented in OrderedDict.\n
    You can initialize instance with a list or generator and call\n
    clean() method once that will return generator with cleaned data.
    """
    _data = None
    _cleaner = None

    def __init__(self, _data: list | GeneratorType):
        """
        Initialize instance with data.\n
        Data can be list or generator of lists in specified by VK.API format.
        :param _data: Data to process.
        """
        if isinstance(_data, GeneratorType):
            self._cleaner = self.clean_generator
        if isinstance(_data, list):
            self._cleaner = self.clean_single

        self._data = _data

    def clean_single(self, data: list) -> list[OrderedDict | dict]:
        """
        Cleans data chunk by deleting redundant fields.\n
        Also makes all items ordered in the right way.
        :return: Cleaned chunk of data.
        """
        keys = ["first_name", "last_name", "country", "city", "bdate", "sex"]
        for i, friend in enumerate(data):
            # Replace empty values with None
            for k in keys:
                friend[k] = friend.get(k)

            self.city_country_titles_rearrangement(friend)

            friend["bdate"] = self.bdate_to_iso(friend["bdate"])

            friend["sex"] = "Female" if friend["sex"] == 1 else "Male"

            data[i] = self.dict_to_ord(friend)

        return data

    def clean_generator(self, _data: list) -> list[OrderedDict | dict]:
        """
        Cleans data chunk by deleting redundant fields.\n
        Also makes all items ordered in the right way.
        :return: Generator if lists with cleaned data.
        """
        for data in _data:
            yield self.clean_single(data)

    def clean(self) -> list[OrderedDict | dict]:
        return self._cleaner(self._data)

    @staticmethod
    def city_country_titles_rearrangement(friend: dict) -> None:
        """
        Replace {"city": {"id": ..., "title": ...}} with {"city": "title"}.\n
        Doing the same operation for "country" key.
        :param friend: Friend data.
        """
        for k in ["country", "city"]:
            if friend[k] is not None:
                friend[k] = friend[k]["title"]

    @staticmethod
    def bdate_to_iso(bdate: str):
        """
        Function to convert date to ISO format.
        :param bdate: Date of format <dd.mm.YYYY> or <dd.mm>.
        :return: Date is ISO format: YYYY-mm-dd.
        If year is not presented, year part is replaced with "1900" value.
        """
        if bdate is None:
            return None

        try:
            bdate = datetime.strptime(bdate, "%d.%m.%Y").isoformat(sep="T").split("T")[0]
        except ValueError:
            bdate = datetime.strptime(bdate, "%d.%m").isoformat(sep="T").split("T")[0]

        return bdate

    @staticmethod
    def dict_to_ord(_dict: dict) -> OrderedDict:
        """
        Function to convert dict to OrderedDict with specific order of fields.
        :param _dict: Dictionary to convert.
        :return: OrderedDict with data from original dict.
        """
        keys = ["first_name", "last_name", "country", "city", "bdate", "sex"]
        to_ord = [(k, _dict[k]) for k in keys]

        return OrderedDict(to_ord)
