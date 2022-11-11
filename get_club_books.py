import os

from dotenv import load_dotenv

from constants import GET_CLUB_BOOKS, CLEAN_CLUB_CSV
from graphql_query import GraphQLQuery

load_dotenv()

TOKEN = os.environ["TOKEN"]


class GetClubBooksQuery(GraphQLQuery):
    DEFAULT_FALLBACK_RESPONSE = {
        "data": {
            "getClubBooks": []
        }
    }

    offset = 0
    limit = 40
    operation_name = "getClubBooks"
    response_count = 0
    author_count = 0
    output_fieldnames = []

    def __init__(self, auth_token=TOKEN):
        super().__init__(auth_token=auth_token)

    def reset_params(self):
        super().reset_params()
        self.body = GET_CLUB_BOOKS["body"]
        self.operation_name = GET_CLUB_BOOKS["name"]
        self.csv_output_file = GET_CLUB_BOOKS["csv"]
        self.output_fieldnames = GET_CLUB_BOOKS["fieldnames"]
        self.limit = 20
        self.take = 100

    def get_club_books(self):
        self.reset_params()

        # read csv file and
        # get club ids
        club_ids = GraphQLQuery.get_column_values(
            filename=CLEAN_CLUB_CSV, column_name="id")

        for _club in club_ids:
            self.club_id = _club
            print(f"\n\n{_club}\n\n")
            data_available = True
            self.offset = 0

            while data_available:
                _response = self.get_response()
                response = self.clean_bytes_response(_response)
                self.offset += self.limit

                try:
                    _search_query = response["data"][self.operation_name]

                except (AttributeError, TypeError):
                    print("Stopping")
                    # private club
                    data_available = False

                else:
                    row_dicts = []

                    for result in _search_query:
                        self.response_count += 1
                        row_dicts.append(result)
                        row_dicts[-1]["count"] = self.response_count
                        row_dicts[-1]["from_query"] = self.query
                        row_dicts[-1]["from_search_book_api"] = self.operation_name
                        print(f"{self.response_count} - {result['slug']}")

                    if len(row_dicts):
                        self.write_to_csv(
                            fieldnames=self.output_fieldnames, rows=row_dicts)
                    else:
                        data_available = False


GetClubBooksQuery().get_club_books()
