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
TEXT_SEARCH_MODE = "Text"
IMAGE_SEARCH_MODE = "Image"
SEARCH_MODE_OPTIONS = (TEXT_SEARCH_MODE, IMAGE_SEARCH_MODE)
TENSOR_SEARCH_MODE = "TENSOR"
LEXICAL_SEARCH_MODE = "LEXICAL"
SEARCH_TEXT_MODE_OPTIONS = ("Tensor", "Lexical")
RESULT_TABLE_HEADERS = [
    {"key_no": 0, "title": "Result No."},
    {"key_no": 1, "title": "Details"},
    {"key_no": 2, "title": "Score"},
]
DOCKER_INTERNAL = "http://host.docker.internal:8222/"
