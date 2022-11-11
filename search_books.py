import os

from pprint import pprint
from dotenv import load_dotenv

from constants import FIELDNAMES_SEARCH_BOOKS
from graphql_query import GraphQLQuery

load_dotenv()

TOKEN = os.environ["TOKEN"]


class SearchBooks(GraphQLQuery):
    DEFAULT_FALLBACK_RESPONSE = {
        "data": {
            "searchBookV2": []
        }
    }

    offset = 0
    limit = 40
    operation_name = "searchBookV2"
    body_search_book_v2_api = "query searchBookV2($query: String!) {\n  searchBookV2(query: $query) {\n    ...BookParts\n    __typename\n  }\n}\n\nfragment BookParts on Book {\n  id\n  slug\n  title\n  subtitle\n  description\n  isbn10\n  isbn13\n  language\n  pageCount\n  publishedDate\n  publisher\n  physicalFormat\n  cover\n  authors {\n    ...AuthorMini\n    __typename\n  }\n  gradientColors\n  workId\n  __typename\n}\n\nfragment AuthorMini on Author {\n  id\n  name\n  slug\n  __typename\n}\n"
    body_search_book_api = "query searchBook($query: String!, $language: String) {\n  searchBook(query: $query, language: $language) {\n    ...BookParts\n    __typename\n  }\n}\n\nfragment BookParts on Book {\n  id\n  slug\n  title\n  subtitle\n  description\n  isbn10\n  isbn13\n  language\n  pageCount\n  publishedDate\n  publisher\n  physicalFormat\n  cover\n  authors {\n    ...AuthorMini\n    __typename\n  }\n  gradientColors\n  workId\n  __typename\n}\n\nfragment AuthorMini on Author {\n  id\n  name\n  slug\n  __typename\n}\n"
    response_count = 0
    csv_output_file = "search_books_3.csv"
    author_csv = "save_authors_3.csv"
    author_count = 0
    ops = [
        {"name": "searchBookV2", "body": body_search_book_v2_api},
        {"name": "searchBook", "body": body_search_book_api},
    ]
    output_fieldnames = FIELDNAMES_SEARCH_BOOKS
    author_fieldnames = [
        "count",
        "from_query",
        "from_search_book_api",
        "id",
        "name",
        "slug",
        "__typename",
        "book_id",
        "book_title"
    ]

    def __init__(self, auth_token=TOKEN):
        super().__init__(auth_token=auth_token)

    def make_query(self):
        for op in self.ops:
            self.body = op["body"]
            self.operation_name = op["name"]

            for q in self.DEFAULT_QUERY_KEYWORDS:
                self.query = q
                _response = self.get_response()
                response = self.clean_bytes_response(_response)
                print(q)

                try:
                    _search_query = response["data"][self.operation_name]
                except AttributeError:
                    print("Stopping")
                else:
                    row_dicts = []

                    for result in _search_query:
                        self.response_count += 1
                        row_dicts.append(result)
                        row_dicts[-1]["count"] = self.response_count
                        row_dicts[-1]["from_query"] = q
                        row_dicts[-1]["from_search_book_api"] = self.operation_name
                        pprint(row_dicts)
                        self.save_authors(result["authors"], result["id"], result["title"],
                                          search_book_api=self.operation_name)

                    if len(row_dicts):
                        self.write_to_csv(fieldnames=self.output_fieldnames, rows=row_dicts)

    def save_authors(self, _authors, book_id, book_title, search_book_api):
        authors = [dict(_author) for _author in _authors]  # fresh copy of dictionaries, avoid mutation

        for author in authors:
            author["book_id"] = book_id
            author["book_title"] = book_title
            self.author_count += 1
            author["count"] = self.author_count
            author["from_query"] = self.query
            author["from_search_book_api"] = search_book_api

            print('\n\n\nSaving author: ...')
            pprint(author)

        self.write_to_csv(
            fieldnames=self.author_fieldnames,
            rows=authors,
            custom_filename=self.author_csv
        )


SearchBooks().make_query()
