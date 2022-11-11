import os

from dotenv import load_dotenv

from constants import SEARCH_SHELVES
from graphql_query import GraphQLQuery

load_dotenv()

TOKEN = os.environ["TOKEN"]


class SearchShelvesLiteQuery(GraphQLQuery):
    """
        Takes out books and __typename from the query.
        Only gets basic shelf details and shelf owner details.
    """

    DEFAULT_FALLBACK_RESPONSE = {
        "data": {
            "searchShelves": []
        }
    }
    operation_name = "searchShelves"

    def __init__(self, auth_token=TOKEN):
        super().__init__(auth_token=auth_token)

    def reset_params(self):
        super().reset_params()
        self.body = SEARCH_SHELVES["body"]
        self.operation_name = SEARCH_SHELVES["name"]
        self.csv_output_file = SEARCH_SHELVES["csv"]
        self.output_fieldnames = SEARCH_SHELVES["fieldnames"]
        self.limit = 100
        self.take = 100

    def search_shelves(self):
        self.reset_params()

        while self.retries < 4:
            _response = self.get_response()
            response = self.clean_bytes_response(_response)

            if self.retries == 0:
                self.offset += self.limit

            try:
                _search_query = response["data"][self.operation_name]

            except (AttributeError, TypeError, KeyError):
                print("Stopping")
                print(response["data"])

            else:
                row_dicts = []

                for result in _search_query:
                    self.response_count += 1
                    row_dicts.append(result)
                    row_dicts[-1]["count"] = self.response_count
                    row_dicts[-1]["from_query"] = self.query
                    print(
                        f"\n\n{self.response_count} - {row_dicts[-1]['slug']}\n\n")

                if len(row_dicts):
                    self.write_to_csv(
                        fieldnames=self.output_fieldnames, rows=row_dicts)
                    self.retries = 0
                else:
                    self.retries += 1


SearchShelvesLiteQuery().search_shelves()
