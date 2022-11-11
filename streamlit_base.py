import os
import re
import marqo
import numpy as np
import pandas as pd
import streamlit as st

from PIL import Image
from pprint import pprint
from typing import Any, Callable, Dict, List
from dotenv import load_dotenv
from marqo.errors import IndexAlreadyExistsError, IndexNotFoundError

from processing_base import CPUTaskSupports
from constants import DENSE_RETRIEVAL_MODELS, IMAGE_SEARCH_MODE, LEXICAL_SEARCH_MODE, SEARCH_MODE_OPTIONS, TENSOR_SEARCH_MODE, TEXT_SEARCH_MODE

load_dotenv()


class StreamlitDemoBase(CPUTaskSupports):
    DEFAULT_MARQO_API_ENDPOINT = os.environ["MARQO_API_ENDPOINT"]
    DEFAULT_MARQO_API_KEY = os.environ["MARQO_API_KEY"]
    DEFAULT_CSV_DATASET = "default.csv"
    DEFAULT_CSV_HEADER = []
    DEFAULT_INDEX_NAME = "default-v4mpnetbase"
    DEFAULT_PRE_FILTERING_OPTIONS = []
    DEFAULT_SEARCHABLE_ATTRS = []
    filter_attrs: List[Dict[str, str]] = [
        {"filter": "filter_name", "pattern": "filter_name:\[(.*?)\]"},
    ]
    fallback_img = ""
    tabs = []
    minimal = False  # all features if False

    def __init__(self, *args, **kwargs):
        self.api_key = None
        self.endpoint_url = None
        self.searchable_attrs_options = None
        self.csv_header = None
        self.csv_dataset = None
        self.index_name = None
        self.search_btn = None
        self.search_method = None
        self.search_image = None
        self.dense_retrieval_model = None
        self.search_image_url = None
        self.search_text = None
        self.index_size = None
        self.search_mode = None
        self.filtering = None
        self.pre_filtering_options = ""
        self.searchable_attrs = ""
        self.render_in_img_expanded_cols = True  # prettifies results ui into columns
        # Streamlit configuration settings
        st.set_page_config(
            page_title="Marqo Demo App",
            page_icon="favicon.png",
            layout="centered",
            initial_sidebar_state="expanded",
            menu_items={}
        )

        self._set_mq_client()
        self.cwd = os.getcwd()  # Get current working directory

    def _set_mq_client(self):
        _endpoint = self.endpoint_url.strip() \
            if self.endpoint_url and self.endpoint_url.strip() else self.DEFAULT_MARQO_API_ENDPOINT
        _api_key = self.api_key.strip() if self.endpoint_url and self.api_key.strip(
        ) else self.DEFAULT_MARQO_API_KEY

        if _api_key == "local":
            self.mq = marqo.Client(url=_endpoint)
        else:
            # Connection to Marqo Docker Container
            self.mq = marqo.Client(url=_endpoint, api_key=_api_key)

    def save_uploaded_file(self, uploaded_file):
        with open(os.path.join(self.cwd, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        return uploaded_file.name

    def reset_state(self):
        st.session_state["results"] = {}
        st.session_state["page"] = -1

    def create_filter_str(self, filter_list):
        filter_string = ""

        for field in filter_list:  #
            for attr in self.filter_attrs:
                if attr["filter"] in field:
                    if attr["filter"] in filter_string:
                        matches = re.finditer(attr["pattern"], filter_string)
                        * _, last_match = matches
                        filter_string = f"{filter_string[:last_match.span()[1]]} OR {field}{filter_string[last_match.span()[1]:]}"
                    else:
                        filter_string += f"{' AND ' if filter_string != '' else ''}({field})"
        print(filter_list)
        print(filter_string)
        return filter_string

    def clean_dataset(self, _csv_dataset, _csv_header):
        self.dataset = pd.read_csv(_csv_dataset).fillna(
            np.nan).replace([np.nan], [""]).head(self.index_size)[
            _csv_header].to_dict("records")

    def load_index(self):
        try:
            _index_name = self.get_index_name()
            self._set_mq_client()

            if self.minimal:
                st.success("Switched index.")

            else:
                _csv_dataset = self.csv_dataset if self.csv_dataset else self.DEFAULT_CSV_DATASET
                _csv_header = self.csv_header.split(",") if len(
                    self.csv_header) > 3 else self.DEFAULT_CSV_HEADER

                self.clean_dataset(_csv_dataset, _csv_header)
                with st.spinner("Adding documents..."):
                    self.mq.index(_index_name).add_documents(
                        self.dataset, client_batch_size=100, server_batch_size=50, processes=5)

                st.success("Successfully added documents.")

        except Exception as err:
            st.error(str(err))

    def create_index(self):
        try:
            settings = {
                # allows us to find an image file and index it
                "treat_urls_and_pointers_as_images": False,
                # "normalize_embeddings": False,
            }
            _index_name = self.get_index_name()

            if self.dense_retrieval_model != "default":
                settings["model"] = self.dense_retrieval_model

            self._set_mq_client()
            self.mq.create_index(_index_name, **settings)

            st.success("Index successfully created.")

        except IndexAlreadyExistsError:
            st.error("Index already exists.")

    def delete_index(self):
        try:
            self.mq.index(self.get_index_name()).delete()
            st.success("Index successfully deleted.")
        except IndexNotFoundError:
            st.error("Index does not exist.")

    def get_search_method(self):
        word_count = len(self.search_text.strip().split(" ")
                         ) if self.search_text else 0
        _search_mode = TENSOR_SEARCH_MODE if word_count > 1 else LEXICAL_SEARCH_MODE
        return _search_mode

    def minimal_sidebar(self):
        with st.sidebar:
            st.write("**Index Settings**")
            self.index_name = st.text_input("Index name")
            st.warning("The endpoint url must be hosted in the internet.\n\n"
                       "If this app and your endpoint is hosted on your local, input **__local__** as the Marqo API key.")
            switch_index_btn = st.button("Switch index")
            if switch_index_btn:
                self.load_index()

    def render_index_settings_ui(self):
        with st.sidebar:
            st.write("**Index Settings**")
            self.endpoint_url = st.text_input("Marqo endpoint url")
            self.api_key = st.text_input("Marqo API key")
            st.warning("The endpoint url must be hosted in the internet.\n\n"
                       "If this app and your endpoint is hosted on your local, input **__local__** as the Marqo API key.")
            st.markdown("""---""")
            self.index_name = st.text_input("Index name")
            self.index_size = st.number_input(
                "Index size", min_value=1, step=1)
            self.dense_retrieval_model = st.selectbox(
                "Dense retrieval model", options=DENSE_RETRIEVAL_MODELS, )
            self.csv_dataset = st.file_uploader(
                "Dataset in csv format", type=["csv"])
            self.csv_header = st.text_input(
                "CSV header separated using comma", )

            add_documents_btn = st.button("Add Documents")
            st.markdown("""---""")
            create_col, delete_col = st.columns([1, 1], gap="small")

            with create_col:
                create_btn = st.button("Create Index")

            with delete_col:
                delete_btn = st.button("Delete Index")

            if create_btn:
                self.create_index()

            if delete_btn:
                self.delete_index()

            if add_documents_btn:
                self.load_index()

    def render_settings_expander(self):
        _pre_filtering_options = self.DEFAULT_PRE_FILTERING_OPTIONS \
            if len(self.pre_filtering_options) < 3 else [optn.strip() for optn in self.pre_filtering_options.split(",")]
        _searchable_attrs_opts = self.DEFAULT_SEARCHABLE_ATTRS if len(
            self.searchable_attrs_options) < 3 else self.searchable_attrs_options.split(",")

        with st.expander("Search Settings", expanded=True):
            attr_col, filter_col = st.columns(2)
            with attr_col:
                self.searchable_attrs = st.multiselect("Searchable Attributes", self.DEFAULT_SEARCHABLE_ATTRS,
                                                       default=_searchable_attrs_opts)

            with filter_col:
                self.filtering = st.multiselect("Pre-filtering Options", _pre_filtering_options,
                                                default=_pre_filtering_options)

    def render_main_app_ui(self):
        logo = Image.open(f"{self.cwd}/marqo-logo.png")
        st.image(logo)

        _index_name = self.get_index_name()
        self.search_text, self.search_image_url, self.search_image = None, None, None
        text_search_col, search_mode_col = st.columns([4, 2])

        with text_search_col:
            self.search_text = st.text_input("Text Search")

        with search_mode_col:
            self.search_mode = st.radio("Search Mode", self.SEARCH_MODE_OPTIONS, horizontal=True,
                                        on_change=self.reset_state)

        if self.search_mode == TEXT_SEARCH_MODE:
            self.search_method = self.get_search_method().capitalize()

        else:
            image_input_col, image_type_col = st.columns([6, 1])

            with image_type_col:
                image_type = st.radio(
                    "Image type", ("Web",))  # ("Web", "Local")

            with image_input_col:
                if image_type == "Web":
                    self.search_image_url = st.text_input(
                        "Provide an Image URL")

                else:
                    self.search_image = st.file_uploader(
                        "Upload an Image", type=["jpg"])

        if not self.minimal:
            self.pre_filtering_options = st.text_input(
                "Pre-filtering options separated using comma")
            self.searchable_attrs_options = st.text_input(
                "Searchable attributes separated using comma")

        self.render_settings_expander()

        st.info(f"Searching **{_index_name}**\n\n"
                f"Search method: **{self.search_method}**", icon="ℹ️")

    def render_result_rows(self):
        for row in enumerate(st.session_state["results"]["hits"]):
            url = row[1].get("url", "")
            title = row[1].get("title", "")
            body = row[1].get("body", "")
            score = row[1].get("_score", "")
            highlights = row[1].get("_highlights", {})

            if type(highlights) == list:
                readable_highlights = None
            else:
                readable_highlights = list(highlights.values())[0] \
                    if self.search_method.upper() == TENSOR_SEARCH_MODE or \
                    self.search_mode == IMAGE_SEARCH_MODE else None

            if (row[0] >= st.session_state["page"] * 10) and (row[0] < (st.session_state["page"] * 10 + 10)):
                with st.expander(f"{row[0] + 1} - {title}", expanded=True):
                    st.info(f"Score: {score}\n\n**Highlights:** {readable_highlights}\n\n **[Go to page]({url})**",
                            icon="ℹ️")
                    st.write(body)

    def render_results_pagination(self):
        if st.session_state["page"] > -1:
            prev_col, page_col, next_col = st.columns([1, 9, 1])

            with prev_col:
                prev_btn = st.button("Prev")
                if prev_btn and (st.session_state["page"] > 0):
                    st.session_state["page"] -= 1

            with next_col:
                next_btn = st.button("Next")
                has_remaining_results = st.session_state["page"] is not None and (
                    (st.session_state["page"] + 1) * 10) < len(st.session_state["results"]["hits"])
                if next_btn and (st.session_state["page"] < 2) and has_remaining_results:
                    st.session_state["page"] += 1

            with page_col:
                page_no = str(st.session_state["page"] + 1)
                st.markdown(
                    f"<div style='text-align: center'> {page_no}</div>", unsafe_allow_html=True)

        if st.session_state["results"] not in [{}, {"hits": []}]:
            if st.session_state["results"]["hits"]:
                st.write("Results (Top 30):")
                if self.render_in_img_expanded_cols:
                    self.render_results_in_cols()
                else:
                    self.render_result_rows()
            else:
                st.write("No results")

    def get_index_name(self):
        return self.index_name if self.index_name else self.DEFAULT_INDEX_NAME

    def render_detail_w_img(self, params: dict, row_counter: int):
        """
        params: dict -> formatted row returned from result hits
        row_counter: int
        """
        score = params.get("_score", 0)
        highlights = params.get("_highlights", "")
        detail_title = params.get("detail_title", "")
        img = params.get("img", "")
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

    def format_detail_params(self, row: dict):
        """Override based on demo requirements."""

        _score = row[1]["_score"]
        _highlights = row[1]["_highlights"]
        _id = row[1]["_id"]
        formatted_params = {
            "_highlights": _highlights,
            "_score": _score,
            "detail_title": _id,
            "_id": _id
        }
        return formatted_params

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
                    i = self.render_detail_w_img(row=row, i=i)
            else:
                cols = st.columns(2)

                for col in cols:
                    with col:
                        row = hits[i]
                        i = self.render_detail_w_img(
                            params=self.format_detail_params(row), row_counter=i)

    def render_results(self):
        if self.search_btn:
            _index_name = self.get_index_name()
            self._set_mq_client()
            results = {"hits": []}

            if self.search_text and self.search_btn:
                results = self.mq.index(_index_name).search(
                    self.search_text.strip(),
                    filter_string=self.create_filter_str(self.filtering),
                    search_method=self.search_method.upper(),
                    searchable_attributes=[i.lower()
                                           for i in self.searchable_attrs],
                    limit=30
                )

            elif self.search_image_url:
                results = self.mq.index(_index_name).search(
                    self.search_image_url,
                    filter_string=self.create_filter_str(self.filtering),
                    searchable_attributes=[i.lower()
                                           for i in self.searchable_attrs],
                    limit=30
                )

            st.session_state["results"] = results

            if st.session_state["results"]["hits"]:
                st.session_state["page"] = 0
            else:
                st.session_state["page"] = -1

        self.render_results_pagination()

    def main(self):
        with open("styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

        # Streamlit state variables (this is to save the state of the session for pagination of Marqo query results)
        if "results" not in st.session_state:
            st.session_state["results"] = {}

        if "page" not in st.session_state:
            st.session_state["page"] = -1

        if self.minimal:
            self.minimal_sidebar()
        else:
            self.render_index_settings_ui()

        self.render_main_app_ui()
        self.search_btn = st.button("Search")
        self.render_results()
