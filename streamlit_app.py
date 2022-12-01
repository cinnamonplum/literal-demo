import json
import streamlit as st

from dotenv import load_dotenv
from constants import IMAGE_SEARCH_MODE, TENSOR_SEARCH_MODE, TEXT_SEARCH_MODE
from streamlit_base import StreamlitDemoBase

load_dotenv()


class StreamlitApp(StreamlitDemoBase):
    SEARCH_MODE_OPTIONS = (TEXT_SEARCH_MODE,)
    minimal = True
    fallback_img = "https://pbs.twimg.com/profile_images/1371430883576717313/LyhsMxnf_400x400.jpg"
    DEFAULT_CSV_HEADER = [
        "id",
        "slug",
        "title",
        "subtitle",
        "description",
        "isbn10",
        "isbn13",
        "language",
        "pageCount",
        "publishedDate",
        "publisher",
        "physicalFormat",
        "cover",
        "authors",
        # shelves
        "owner",
        # clubs
        "name",
        "handle",
        "languages",
        "updatedAt",
        "createdAt",
        "image",
        # profiles
        "bio",
        "invitedByProfileId",
        # general
        "filter",
    ]
    DEFAULT_INDEX_NAME = "literal-data"
    DEFAULT_PRE_FILTERING_OPTIONS = [
        "filter:(profiles)",
        "filter:(shelves)",
        "filter:(books)",
        "filter:(clubs)",
        # "authors",
    ]
    DEFAULT_SEARCHABLE_ATTRS = [
        "title",
        "subtitle",
        "description",
        "isbn10",
        "isbn13",
        "language",
        # "publishedDate",
        "publisher",
        "authors",
        # "club_name",
    ]
    filter_attrs = [
        {"filter": "filter",
         "pattern": "filter:\((books|clubs|shelves|profiles)\)"},
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.searchable_attrs_options = "title"
        self.tabs = [
            "Books", "Clubs", "Shelves", "Profiles"
        ]
        self.render_in_img_expanded_cols = True

    def format_detail_params(self, row: dict):
        """Override based on demo requirements."""

        formatted_params = super().format_detail_params(row)
        raw_authors = row[1].get("authors", "")

        try:
            raw_authors = eval(raw_authors)
            authors = ", ".join([author.get("name", "")
                                for author in raw_authors])
        except Exception as err:
            authors = raw_authors
            print(err)

        formatted_params["authors"] = authors
        formatted_params["bio"] = row[1].get("bio", "")
        formatted_params["img"] = row[1].get("cover", "")
        formatted_params["createdAt"] = row[1].get("createdAt", "")
        formatted_params["description"] = row[1].get("description", "")
        formatted_params["filter"] = row[1].get("filter", "")
        formatted_params["handle"] = row[1].get("handle", "")
        formatted_params["id"] = row[1].get("id", "")
        formatted_params["image"] = row[1].get("image", "")
        formatted_params["invitedByProfileId"] = row[1].get(
            "invitedByProfileId", "")
        formatted_params["isbn10"] = row[1].get("isbn10", "")
        formatted_params["isbn13"] = row[1].get("isbn13", "")
        formatted_params["language"] = row[1].get("language", "")
        formatted_params["languages"] = row[1].get("languages", "")
        formatted_params["name"] = row[1].get("name", "")
        formatted_params["owner"] = row[1].get("owner", "")
        formatted_params["pageCount"] = row[1].get("pageCount", "")
        formatted_params["physicalFormat"] = row[1].get("physicalFormat", "")
        formatted_params["publishedDate"] = row[1].get("publishedDate", "")
        formatted_params["publisher"] = row[1].get("publisher", "")
        formatted_params["slug"] = row[1].get("slug", "")
        formatted_params["subtitle"] = row[1].get("subtitle", "")
        formatted_params["title"] = row[1].get("title", "")
        formatted_params["updatedAt"] = row[1].get("updatedAt", "")
        formatted_params["detail_title"] = row[1].get("title", "")
        return formatted_params

    def render_detail_w_img(self, params: dict, row_counter: int):
        """
        params: dict -> formatted row returned from result hits
        row_counter: int
        """
        score = params.get("_score", 0)
        highlights = params.get("_highlights", "")
        detail_title = params.get("detail_title", "")
        img = params.get("img", "")
        # del params["_id"]
        del params["bio"]
        del params["createdAt"]
        del params["filter"]
        del params["slug"]
        del params["updatedAt"]
        del params["languages"]
        del params["language"]
        del params["physicalFormat"]
        del params["publishedDate"]
        del params["invitedByProfileId"]
        del params["publisher"]
        del params["title"]
        del params["_score"]
        del params["_highlights"]
        del params["detail_title"]
        del params["img"]
        row_counter += 1

        if type(highlights) == list:
            readable_highlights = None
        else:
            readable_highlights = list(highlights.values())[0] if self.search_method.upper(
            ) == TENSOR_SEARCH_MODE or self.search_mode == IMAGE_SEARCH_MODE else None
        with st.expander(f"{detail_title}", expanded=True):
            if img:
                st.image(img)
            else:
                st.image(self.fallback_img)

            st.info(f"**{detail_title}**\n\nScore: {score}\n\n**Highlights:** {readable_highlights}",
                    icon="ℹ️")
            for param_key, param_value in params.items():
                st.write(f"{param_key}: {param_value}")

        return row_counter

    def render_results_in_cols(self):
        hits = list(enumerate(st.session_state["results"]["hits"]))
        starting_index = st.session_state["page"] * 10
        i = starting_index
        ending_index = starting_index

        if starting_index + 10 > len(hits) or (len(hits) - starting_index + 10) < 10:
            ending_index = len(hits)
        elif (len(hits) - starting_index + 10) > 10:
            ending_index = starting_index + 10

        while i < ending_index:
            if i == len(hits) or (i == len(hits) - 1 and len(hits) % 2 == 0):
                cols = []
            elif len(hits) == 1 or (len(hits) - i) == 1:
                single_col, _ = st.columns([6, 6])
                with single_col:
                    row = hits[i]
                    i = self.render_detail_w_img(row=row, row_counter=i)
            else:
                cols = st.columns(2)

                for col in cols:
                    with col:
                        row = hits[i]
                        i = self.render_detail_w_img(
                            params=self.format_detail_params(row), row_counter=i)


if __name__ == "__main__":
    StreamlitApp().main()
