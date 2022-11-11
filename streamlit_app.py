import streamlit as st

from dotenv import load_dotenv
from constants import TEXT_SEARCH_MODE
from streamlit_base import StreamlitDemoBase

load_dotenv()


class StreamlitApp(StreamlitDemoBase):
    SEARCH_MODE_OPTIONS = (TEXT_SEARCH_MODE,)
    render_in_img_expanded_cols = True
    minimal = True
    fallback_img = ""

    def format_detail_params(self, row: dict):
        """Override based on demo requirements."""

        formatted_params = super().format_detail_params(row)
        return formatted_params


if __name__ == "__main__":
    StreamlitApp().main()
