import os

from dotenv import load_dotenv

from constants import SEARCH_CLUBS_OPS
from graphql_query import GraphQLQuery

load_dotenv()

TOKEN = os.environ["TOKEN"]


class SearchClubsQuery(GraphQLQuery):
    DEFAULT_FALLBACK_RESPONSE = {
        "data": {
            "searchClubs": []
        }
    }
    operation_name = "searchClubs"

    def __init__(self, auth_token=TOKEN):
        super().__init__(auth_token=auth_token)

    def reset_params(self):
        super().reset_params()
        self.body = SEARCH_CLUBS_OPS["body"]
        self.operation_name = SEARCH_CLUBS_OPS["name"]
        self.csv_output_file = SEARCH_CLUBS_OPS["csv"]
        self.output_fieldnames = SEARCH_CLUBS_OPS["fieldnames"]
        self.limit = 100

    def search_clubs(self):
        self.reset_params()
        data_available = True

        while data_available:
            _response = self.get_response()
            response = self.clean_bytes_response(_response)
            self.offset += self.limit

            try:
                _search_query = response["data"][self.operation_name]
            except AttributeError:
                print("Stopping")
                data_available = False
            else:
                row_dicts = []

                for result in _search_query:
                    self.response_count += 1
                    row_dicts.append(result)
                    del row_dicts[-1]["memberships"]
                    row_dicts[-1]["count"] = self.response_count
                    row_dicts[-1]["from_query"] = self.query
                    row_dicts[-1]["from_search_book_api"] = self.operation_name
                    print(
                        f"\n\n{self.response_count} - {row_dicts[-1]['name']}\n\n")

                if len(row_dicts):
                    self.write_to_csv(
                        fieldnames=self.output_fieldnames, rows=row_dicts)
                else:
                    data_available = False


SearchClubsQuery().search_clubs()
