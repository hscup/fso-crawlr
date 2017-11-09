import csv
import os
from enum import Enum


class FileStatus(Enum):
    FILE_EMPTY = 0
    FILE_NOT_EMPTY = 1


class CsvHelper():
    def __init__(self, filename='data.csv', mode='w', encoding=None,  headers=None):
        self.status = FileStatus.FILE_EMPTY
        self.filename = filename
        self.mode = mode
        self.headers = headers
        self.encoding = encoding

    def set_headers(self, headers):
        self.headers = headers

    def save_to_csv(self, *args, **kwargs):
        # Only check file status if it is initial empty
        if self.status == FileStatus.FILE_EMPTY \
                and os.path.isfile(self.filename)    \
                and os.stat(self.filename).st_size != 0:
            self.status = FileStatus.FILE_NOT_EMPTY

        if hasattr(kwargs, 'headers'):
            self.headers = list(kwargs.get('headers'))

        with open(self.filename, mode=self.mode, newline='', encoding=self.encoding) as csvfile:
            writer = csv.writer(csvfile)
            if self.status == FileStatus.FILE_EMPTY and bool(self.headers):
                writer.writerow(self.headers)

            for row in args:
                writer.writerow(row)
