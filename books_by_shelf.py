import os
import requests
import time
import pandas as pd
import math

from pprint import pprint
from typing import List, Any
from dotenv import load_dotenv
from constants import BOOKS_BY_SHELF
from graphql_query import GraphQLQuery

load_dotenv()

TOKEN = os.environ["TOKEN"]


class BookByShelfQuery(GraphQLQuery):
    DEFAULT_FALLBACK_RESPONSE = {
        "data": {
            "booksByShelf": []
        }
    }
    # shelf_slug,request_slug_offset, count, from_query, from_search_book_api id,slug,title,subtitle,description,isbn10,isbn13,language,pageCount,publishedDate,publisher",
    #     "physicalFormat",
    #     "cover",
    #     "authors",  # Author[] id, name, slug, __typename
    #     "gradientColors",  # List[str]
    #     "workId",
    #     "__typename"

    offset = 0
    limit = 100
    operation_name = "booksByShelf"
    response_count = 0
    author_count = 0
    output_fieldnames = []

    def __init__(self, auth_token=TOKEN):
        super().__init__(auth_token=auth_token)

    def search_books_by_shelf_slug(self):
        session = self.get_session()
        self.response_count = 0
        file_count = 0

        while True:
            # get slug from queue until no slug left
            slug = self.queue.get()
            headers = {
                "content-type": "application/json",
                "Authorization": f"Bearer {self.auth_token}"
            }

            data_available = True
            offset = 0

            while data_available:
                with session.post(
                        url=self.LITERAL_API,
                        headers=headers,
                        json={
                            "query": self.body,
                            "variables": {
                                "limit": self.limit,
                                "offset": offset,
                                "shelfSlug": slug,
                            },
                            "operationName": self.operation_name
                        },
                ) as _response:
                    response = self.clean_bytes_response(_response.content)
                    offset += self.limit

                    try:
                        _search_query = response["data"][self.operation_name]

                    except (AttributeError, TypeError, KeyError):
                        print("Stopping")
                        data_available = False

                    else:
                        row_dicts = []

                        for result in _search_query:
                            self.response_count += 1
                            row_dicts.append(result)
                            row_dicts[-1]["count"] = self.response_count
                            row_dicts[-1]["shelf_slug"] = slug
                            row_dicts[-1]["request_slug_offset"] = offset
                            row_dicts[-1]["from_search_book_api"] = self.operation_name
                            print(
                                f"\n\n{self.response_count} - {row_dicts[-1]['slug']}\n\n")

                        if len(row_dicts):
                            custom_filename = f"books_by_shelf/split-{math.ceil(result['count']/50000)}.csv"
                            self.write_to_csv(
                                fieldnames=self.output_fieldnames, rows=row_dicts, custom_filename=custom_filename)
                        else:
                            data_available = False

            self.queue.task_done()

    def books_by_shelf(self):
        self.body = BOOKS_BY_SHELF["body"]
        self.operation_name = BOOKS_BY_SHELF["name"]
        self.csv_output_file = "nov19_books_by_shelf.csv"
        self.output_fieldnames = BOOKS_BY_SHELF["fieldnames"]
        self.offset = 0
        self.response_count = 0

        slugs = GraphQLQuery.get_column_values(
            filename="search_shelves.csv", column_name="slug")
        shelf_slugs = list(slugs)
        self.multithread_process(
            items=shelf_slugs, target_function=self.search_books_by_shelf_slug)


BookByShelfQuery().books_by_shelf()
