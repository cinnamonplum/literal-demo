import marqo
import pandas as pd
import os

from dotenv import load_dotenv

load_dotenv()

DEFAULT_MARQO_API_ENDPOINT = os.environ["MARQO_API_ENDPOINT"]
DEFAULT_MARQO_API_KEY = os.environ["MARQO_API_KEY"]
index_name = "cookidoo-vivien-v4mpnetbase"
dataset = pd.read_csv(
    "get_recipe_details_by_id.csv")[1560:].to_dict("records")
settings_dict = {
    "index_defaults": {
        "model": "flax-sentence-embeddings/all_datasets_v4_mpnet-base",
        # "text_preprocessing": {
        #     "split_length": 1,
        #     "split_overlap": 0,
        #     "split_method": "sentence"
        # }
    },
    "number_of_shards": 5
}
mq = marqo.Client(api_key=DEFAULT_MARQO_API_KEY,
                  url=DEFAULT_MARQO_API_ENDPOINT)
# mq.create_index(index_name, settings_dict=settings_dict)
mq.index(index_name).add_documents(dataset, non_tensor_fields=[
    "devices", "difficulty", "img", "total_time", "prep_time", "num_reviews", "proportions", "rating"], client_batch_size=5, device="cuda")
mq.index(index_name).refresh()
