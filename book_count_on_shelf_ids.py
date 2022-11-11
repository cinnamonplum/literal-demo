import os
import pandas as pd

from queue import Queue
from pprint import pprint
from typing import List, Any
from dotenv import load_dotenv

from constants import BOOKS_GET_BOOKS_ON_SHELF_COUNT
from graphql_query import GraphQLQuery

load_dotenv()

TOKEN = os.environ["TOKEN"]


class BookCountOnShelvesQuery(GraphQLQuery):
    DEFAULT_FALLBACK_RESPONSE = {
        "data": {
            "getBooksOnShelfCountsByShelfIds": []
        }
    }

    offset = 0
    limit = 40
    operation_name = "getBooksOnShelfCountsByShelfIds"
    response_count = 0
    author_count = 0
    output_fieldnames = []

    def __init__(self, auth_token=TOKEN):
        super().__init__(auth_token=auth_token)

    def get_overall_book_count(self):
        df = pd.read_csv("book_count_on_shelves.csv")
        book_count = 0

        for row in df["bookCount"]:
            book_count += row

        print(f"\n\n\nbook_count: {book_count}")
        return book_count

    def get_book_count_from_shelves(self):
        self.body = BOOKS_GET_BOOKS_ON_SHELF_COUNT["body"]
        self.operation_name = BOOKS_GET_BOOKS_ON_SHELF_COUNT["name"]
        self.csv_output_file = BOOKS_GET_BOOKS_ON_SHELF_COUNT["csv"]
        self.output_fieldnames = BOOKS_GET_BOOKS_ON_SHELF_COUNT["fieldnames"]
        self.limit = 100
        self.offset = 0
        self.take = 100
        self.response_count = 0

        _shelf_ids = list(GraphQLQuery.get_column_values(
            filename="search_shelves.csv", column_name="id"))

        _count = 0
        df = pd.read_csv("search_shelves.csv")
        _constant = int(len(list(df["id"])) / 4)
        book_count = 0

        while _count < len(_shelf_ids) - 1:
            self.shelf_ids = list(df["id"].iloc[_count:_count + _constant])
            _count += _constant
            print(_count)

            print(self.shelf_ids.__len__(), "\n\n\n")

            _response = self.get_response()
            response = self.clean_bytes_response(_response)

            try:
                _search_query = response["data"][self.operation_name]

            except (AttributeError, TypeError):
                print("Stopping")

            else:
                row_dicts = []

                for result in _search_query:
                    self.response_count += 1
                    row_dicts.append(result)
                    del row_dicts[-1]["__typename"]
                    row_dicts[-1]["count"] = self.response_count
                    book_count += result["bookCount"]
                    print(book_count)

                if len(row_dicts):
                    self.write_to_csv(
                        fieldnames=self.output_fieldnames, rows=row_dicts)


BookCountOnShelvesQuery().get_overall_book_count()
