import os

from pprint import pprint
from dotenv import load_dotenv
from graphql_query import GraphQLQuery

load_dotenv()

TOKEN = os.environ["TOKEN"]


class SearchProfiles(GraphQLQuery):
    DEFAULT_FALLBACK_RESPONSE = {
        "data": {
            "searchProfiles": []
        }
    }

    offset = 0
    limit = 40
    operation_name = "searchProfiles"
    body = "query searchProfiles($query: String!, $limit: Int!, $offset: Int!) {\n  searchProfiles(query: $query, limit: $limit, offset: $offset) {\n    ...ProfileParts\n    __typename\n  }\n}\n\nfragment ProfileParts on Profile {\n  id\n  handle\n  name\n  bio\n  image\n  invitedByProfileId\n  __typename\n}\n"
    response_count = 0
    csv_output_file = "search_profiles.csv"
    output_fieldnames = [
        "count",
        "id",
        "handle",
        "name",
        "bio",
        "image",
        "invitedByProfileId",
        "__typename",
    ]

    def __init__(self, auth_token=TOKEN):
        super().__init__(auth_token=auth_token)

    def make_query(self):
        self.search(query_name=self.operation_name)


SearchProfiles().make_query()
