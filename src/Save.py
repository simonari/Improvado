import os

import json
from typing import IO
from contextlib import contextmanager
from collections import OrderedDict


class Save:
    """
    Class to save data in specified formats.\n
    """
    # TODO: Might add generator initialization support
    data_ext = None
    _context_manager = None
    _adder = None
    _saver = None

    def __init__(self, _path: str):
        """
        Initialize instance with a path to save data.
        :param _path: Path to save data.
        """
        self.path_to_save = _path
        self._set_ext()
        self._set_saver()
        self._clear_existing()
        self._create_report()

    def _set_ext(self):
        """
        Set data extension.
        """
        self.data_ext = os.path.splitext(self.path_to_save)[-1]

    def _set_saver(self):
        """
        Set data saver.
        """
        config = {
            ".csv": self._save_as_csv,
            ".tsv": self._save_as_tsv,
            ".json": self._save_as_json
        }

        self._saver = config[self.data_ext]

    def _clear_existing(self):
        """
        Clear existing reports from a root path and path, where a user points to.
        """
        cwd = os.getcwd()
        paths_std = ["report.tsv", "report.csv", "report.json"]
        paths_std = [os.path.join(cwd, path) for path in paths_std]

        for path in paths_std:
            if os.path.exists(path):
                os.remove(path)

        # Clearing an existing report from a save path
        path = self.path_to_save
        if os.path.exists(path):
            os.remove(path)

    def _create_report(self):
        """
        Create a report file.
        """
        open(self.path_to_save, "w", encoding="utf-8").close()

    @contextmanager
    def _open_as_csv(self) -> IO:
        """
        Context manager to open a file in .csv extension.
        Also, write the headers to the file.
        :return: Context manager, that you can open with "with open" statement.
        """
        f = open(self.path_to_save, "a", encoding="utf-8")
        delimiter = ","

        fields = ["First Name", "Last Name", "Country", "City", "Birthdate", "Sex"]
        for i, field in fields:
            f.write(field)
            f.write(delimiter if i != 5 else "\n")

        try:
            yield f
        finally:
            f.close()

    @staticmethod
    def _add_chunk_to_csv(f: IO, chunk: dict | OrderedDict):
        """
        Add a chunk of data to the end of .csv file.
        :param f: Context manager _open_as_csv.
        :param chunk: Chunk of data to write.
        """
        delimiter = ","
        while chunk:
            friend = chunk.pop(0)
            for i, field in enumerate(friend):
                f.write(str(friend[field]))
                f.write(delimiter if i != 5 else "\n")

    def _save_as_csv(self, data: dict | OrderedDict):
        """
        TODO: Add generator support
        Save data in .csv format.\n
        :param data: All data to save.
        :return:
        """
        with self._open_as_csv() as f:
            self._add_chunk_to_csv(f, data)

    @contextmanager
    def _open_as_tsv(self) -> IO:
        """
        Context manager to open a file in .tsv extension.
        Also, write the headers to the file.
        :return: Context manager, that you can open with "with open" statement.
        """
        f = open(self.path_to_save, "a", encoding="utf-8")
        delimiter = "\t"

        fields = ["First Name", "Last Name", "Country", "City", "Birthdate", "Sex"]
        for i, field in fields:
            f.write(field)
            f.write(delimiter if i != 5 else "\n")

        try:
            yield f
        finally:
            f.close()

    @staticmethod
    def _add_chunk_to_tsv(f: IO, chunk: dict | OrderedDict):
        """
        Add a chunk of data to the end of .tsv file.
        :param f: Context manager _open_as_tsv.
        :param chunk: Chunk of data to write.
        """
        delimiter = "\t"
        while chunk:
            friend = chunk.pop(0)
            for i, field in enumerate(friend):
                f.write(str(friend[field]))
                f.write(delimiter if i != 5 else "\n")

    def _save_as_tsv(self, data: dict | OrderedDict):
        """
        TODO: Add generator support
        Save data in .tsv format.\n
        :param data: All data to save.
        :return:
        """
        with self._open_as_tsv() as f:
            self._add_chunk_to_tsv(f, data)

    @contextmanager
    def _open_as_json(self) -> IO:
        """
        Context manager to open a file in .json extension.
        :return: Context manager, that you can open with "with open" statement.
        """
        f = open(self.path_to_save, "ab")

        try:
            yield f
        finally:
            f.close()

    @staticmethod
    def _add_chunk_to_json(f: IO, chunk: dict | OrderedDict):
        """
        Add a chunk of data to the end of .json file.
        :param f: Context manager _open_as_json.
        :param chunk: Chunk of data to write.
        """
        # set caveat to eof
        f.seek(0, 2)
        # if a file is empty, dump data
        if f.tell() == 0:
            f.write(json.dumps([chunk], indent=2).encode())
        # else: put caveat one symbol back, delete "]" and write extra data
        else:
            f.seek(-1, 2)
            f.truncate()
            f.write(' , '.encode())
            f.write(json.dumps(chunk, indent=2).encode())
            f.write("]".encode())

    def _save_as_json(self, data: dict | OrderedDict):
        """
        TODO: Add generator support
        Save data in .json format.\n
        :param data: All data to save.
        :return:
        """
        with self._open_as_json() as f:
            self._add_chunk_to_json(f, data)

    def save(self, data):
        """
        TODO: Add generator support
        Function to save data.\n
        Chooses saver function from configuration of instance.
        :param data: All data to save
        """
        self._saver(data)
