import csv
import requests
import time
import json
import pandas as pd

from requests import Response
from json import JSONDecodeError

from processing_base import CPUTaskSupports


class GraphQLQuery(CPUTaskSupports):
    GRAPHQL_API_URL = "https://literal.club/graphql/"
    DEFAULT_FALLBACK_RESPONSE = {"data": {"searchQuery": []}}

    offset = 0
    limit = 40
    take = 100
    query = ""
    request_retries = 0
    operation_name = ""
    csv_output_file = ""
    error_csv = "error.csv"
    body = """"""
    response_count = 0
    author_count = 0
    output_fieldnames = []

    def __init__(self, auth_token):
        self.auth_token = auth_token
        self.DEFAULT_QUERY_KEYWORDS = GraphQLQuery.generate_query_keywords()

    @staticmethod
    def generate_query_keywords():
        extended_ascii_chars = [241]  # enye
        return [*[chr(letter) for letter in range(97, 123)],  #
                *[chr(number) for number in range(48, 58)],  # 0 to 9
                *[chr(extra_char) for extra_char in extended_ascii_chars]]

    @staticmethod
    def get_column_values(filename, column_name):
        csv_file = pd.read_csv(filename)
        return csv_file[column_name]

    def reset_params(self):
        """Resets offset, retries, and response_count"""
        self.offset = 0
        self.retries = 0
        self.response_count = 0

    def clean_bytes_response(self, content):
        try:
            return json.loads(content)

        except TypeError:
            # TypeError: the JSON object must be str, bytes or bytearray, not list
            return self.DEFAULT_FALLBACK_RESPONSE

        except JSONDecodeError:
            self.write_to_csv(
                fieldnames=["offset", "limit", "response_count",
                            "content", "operation_name"],
                rows=[],
                custom_filename="json_decode_error.csv",
                row_values={
                    "offset": self.offset,
                    "limit": self.limit,
                    "response_count": self.response_count,
                    "content": content,
                    "operation_name": self.operation_name
                }
            )
            return self.DEFAULT_FALLBACK_RESPONSE

        except Exception as err:
            self.write_to_csv(
                fieldnames=["offset", "limit", "response_count",
                            "content", "operation_name", "exception"],
                rows=[],
                custom_filename="other_errors.csv",
                row_values={
                    "offset": self.offset,
                    "limit": self.limit,
                    "response_count": self.response_count,
                    "content": content,
                    "exception": str(err),
                    "operation_name": self.operation_name
                }
            )
            return self.DEFAULT_FALLBACK_RESPONSE

    def log_error(self, response_status_code):
        self.write_to_csv(
            fieldnames=["offset", "limit", "response_code",
                        "retries", "operation_name"],
            rows=[],
            custom_filename=self.error_csv,
            row_values={
                "offset": self.offset,
                "limit": self.limit,
                "response_code": response_status_code,
                "retries": self.request_retries,
                "operation_name": self.operation_name
            }
        )

    def get_response(self):
        headers = {
            "content-type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        response: Response = requests.post(
            url=self.GRAPHQL_API_URL,
            headers=headers,
            json={
                "query": self.body,
                "variables": {
                    "query": self.query,
                    "limit": self.limit,
                    "offset": self.offset,
                    "take": self.take,
                    "clubId": self.club_id,
                    "shelfSlug": self.shelf_slug,
                    "shelfIds": self.shelf_ids,
                },
                "operationName": self.operation_name
            },
        )

        # print("response status code: ", response.status_code)

        if response.status_code == 200:
            return response.content

        elif response.status_code in [503, 502]:
            self.log_error(response_status_code=response.status_code)
            self.request_retries += 1

            if self.request_retries < 4:
                return self.get_response()
            else:
                self.request_retries = 0
                return self.DEFAULT_FALLBACK_RESPONSE

        else:
            print(f"oops! {response.status_code}")
            self.log_error(response_status_code=response.status_code)
            return self.DEFAULT_FALLBACK_RESPONSE

    def write_to_csv(self, fieldnames: list[str], rows: list[dict], custom_filename="", row_values=None) -> None:
        """
        Util for printing out dictionary values to a csv file
        """
        filename = custom_filename if custom_filename else self.csv_output_file

        with open(filename, "a", newline="") as out:
            _writer = csv.DictWriter(out, fieldnames=fieldnames, )

            if row_values:
                _writer.writerow(row_values)
            else:
                _writer.writerows(rowdicts=rows)

    def search(self, query_name="searchQuery"):
        # with limit?
        # dynamic query?
        _search_query = None
        data_available = True

        while data_available:
            _response = self.get_response()
            response = self.clean_bytes_response(_response)
            self.offset += self.limit

            try:
                _search_query = response["data"][query_name]
            except AttributeError:
                print("Stopping")
                data_available = False
            else:
                row_dicts = []

                for result in _search_query:
                    self.response_count += 1
                    row_dicts.append(result)
                    row_dicts[-1]["count"] = self.response_count

                if len(_search_query) < 1:
                    data_available = False

                else:
                    self.write_to_csv(
                        fieldnames=self.output_fieldnames, rows=row_dicts)

    def make_query(self):
        self.search()
