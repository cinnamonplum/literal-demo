# import multiprocessing as mp

# import streamlit as st
import os
import time
import pandas as pd
import marqo
import numpy as np

from pprint import pprint
from PIL import Image
from typing import Any, List
from marqo.errors import IndexAlreadyExistsError, IndexNotFoundError
from dotenv import load_dotenv
from multiprocessing import Process
# multithreading
from threading import Thread, local
from requests.sessions import Session
from queue import Queue


load_dotenv()


CSV_DATASET = "literal-split-0.csv"
header = "id,slug,title,subtitle,description,isbn10,isbn13,language,pageCount,publishedDate,publisher,physicalFormat,cover,authors,filter,owner,name,handle,languages,updatedAt,createdAt,image,bio,invitedByProfileId".split(
    ",")
INDEX_SIZE = 1000000
DENSE_RETRIEVAL_MODELS = (
    "default",
    "flax-sentence-embeddings/all_datasets_v4_mpnet-base",
    "flax-sentence-embeddings/all_datasets_v4_MiniLM-L12",
    "flax-sentence-embeddings/all_datasets_v4_MiniLM-L6",
    "sentence-transformers/stsb-xlm-r-multilingual",
    "sentence-transformers/all-mpnet-base-v2",
    "sentence-transformers/all-MiniLM-L6-v2",
    "ViT-B/16",
)
INDEX_NAME = "literal-threaded"
MARQO_API_ENDPOINT = "http://i4v3alutrc.execute-api.us-east-1.amazonaws.com/prod"
MARQO_API_KEY = "CeKE4HNNUp1Q0SKDgm4Mk83E4jEMS15S89M5XBMl"
settings = {
    # allows us to find an image file and index it
    # "treat_urls_and_pointers_as_images": True,
    # "normalize_embeddings": False,
    "model": DENSE_RETRIEVAL_MODELS[1],
}
dtype = {
    "id": "string",
    "slug": "string",
    "title": "string",
    "subtitle": "string",
    "description": "string",
    "isbn10": "string",
    "isbn13": "string",
    "language": "string",
    "pageCount": "string",
    "publishedDate": "string",
    "publisher": "string",
    "physicalFormat": "string",
    "cover": "string",
    "authors": "string",
    "filter": "string",
    "owner": "string",
    "name": "string",
    "handle": "string",
    "languages": "string",
    "updatedAt": "string",
    "createdAt": "string",
    "image": "string",
    "bio": "string",
    "invitedByProfileId": "string"
}

df = pd.read_csv(CSV_DATASET)
dataset = df.head(
    INDEX_SIZE)[header].to_dict("records")
mq = marqo.Client(url=MARQO_API_ENDPOINT, api_key=MARQO_API_KEY)
# mq.create_index(INDEX_NAME, **settings)


class Threaded:
    def main(self):
        mq.index(INDEX_NAME).add_documents(dataset)


Threaded().main()
