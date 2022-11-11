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
BODY_SEARCH_CLUBS = "query searchClubs($query: String!, $limit: Int!, $offset: Int!) {\n  searchClubs(query: $query, limit: $limit, offset: $offset) {\n    ...ClubPreview\n    __typename\n  }\n}\n\nfragment ClubPreview on Club {\n  ...ClubParts\n  memberships(first: 1) {\n    ...ClubMembershipParts\n    profile {\n      ...ProfileParts\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment ClubParts on Club {\n  id\n  name\n  handle\n  description\n  languages\n  updatedAt\n  createdAt\n  image\n  __typename\n}\n\nfragment ClubMembershipParts on ClubMembership {\n  profileId\n  role\n  clubId\n  updatedAt\n  createdAt\n  __typename\n}\n\nfragment ProfileParts on Profile {\n  id\n  handle\n  name\n  bio\n  image\n  invitedByProfileId\n  __typename\n}\n"
BODY_SEARCH_SHELVES = "query searchShelves($query: String!, $limit: Int!, $offset: Int!) {\n  searchShelves(query: $query, limit: $limit, offset: $offset) {\n    ...ShelfFull\n  }\n}\n\nfragment ShelfFull on Shelf {\n  ...ShelfParts\n  owner {\n    ...ProfileParts\n  }\n}\n\nfragment ShelfParts on Shelf {\n  id\n  slug\n  title\n  description\n  profileId\n}\n\nfragment ProfileParts on Profile {\n  id\n  handle\n  name\n  bio\n  image\n  invitedByProfileId\n}\n"
BODY_REC_BOOKS = "query recBooks {\n  recBooks {\n    ...BookParts\n    __typename\n  }\n}\n\nfragment BookParts on Book {\n  id\n  slug\n  title\n  subtitle\n  description\n  isbn10\n  isbn13\n  language\n  pageCount\n  publishedDate\n  publisher\n  physicalFormat\n  cover\n  authors {\n    ...AuthorMini\n    __typename\n  }\n  gradientColors\n  workId\n  __typename\n}\n\nfragment AuthorMini on Author {\n  id\n  name\n  slug\n  __typename\n}\n"
BODY_GET_CLUB_BOOKS = "query getClubBooks($clubId: String!, $limit: Int!, $offset: Int!) {\n  getClubBooks(clubId: $clubId, limit: $limit, offset: $offset) {\n    ...BookParts\n    __typename\n  }\n}\n\nfragment BookParts on Book {\n  id\n  slug\n  title\n  subtitle\n  description\n  isbn10\n  isbn13\n  language\n  pageCount\n  publishedDate\n  publisher\n  physicalFormat\n  cover\n  authors {\n    ...AuthorMini\n    __typename\n  }\n  gradientColors\n  workId\n  __typename\n}\n\nfragment AuthorMini on Author {\n  id\n  name\n  slug\n  __typename\n}\n"
BODY_BOOKS_BY_SHELF = "query booksByShelf($limit: Int!, $offset: Int!, $shelfSlug: String!, $search: String, $sortBy: BookSorting, $sortDirection: SortDirection) {\n  booksByShelf(\n    limit: $limit\n    offset: $offset\n    shelfSlug: $shelfSlug\n    search: $search\n    sortBy: $sortBy\n    sortDirection: $sortDirection\n  ) {\n    ...BookParts\n  }\n}\n\nfragment BookParts on Book {\n  id\n  slug\n  title\n  subtitle\n  description\n  isbn10\n  isbn13\n  language\n  pageCount\n  publishedDate\n  publisher\n  physicalFormat\n  cover\n  authors {\n    ...AuthorMini\n  }\n}\n\nfragment AuthorMini on Author {\n  id\n  name\n  slug\n}\n"
BODY_BOOKS_BY_AUTHOR = "query booksByAuthor($limit: Int!, $offset: Int!, $authorId: String!) {\n  booksByAuthor(limit: $limit, offset: $offset, authorId: $authorId) {\n    ...BookParts\n    __typename\n  }\n}\n\nfragment BookParts on Book {\n  id\n  slug\n  title\n  subtitle\n  description\n  isbn10\n  isbn13\n  language\n  pageCount\n  publishedDate\n  publisher\n  physicalFormat\n  cover\n  authors {\n    ...AuthorMini\n    __typename\n  }\n  gradientColors\n  workId\n  __typename\n}\n\nfragment AuthorMini on Author {\n  id\n  name\n  slug\n  __typename\n}\n"
BODY_AUTHOR_BY_SLUG_OR_ID = "query authorBySlugOrId($slugOrId: String!) {\n  authorBySlugOrId(slugOrId: $slugOrId) {\n    ...AuthorParts\n    __typename\n  }\n}\n\nfragment AuthorParts on Author {\n  id\n  name\n  slug\n  aliases\n  description\n  image\n  updatedAt\n  __typename\n}\n"
BODY_GET_BOOKS_ON_SHELF_COUNT = "query getBooksOnShelfCountsByShelfIds($shelfIds: [String!]!) {\n  getBooksOnShelfCountsByShelfIds(shelfIds: $shelfIds) {\n    shelfId\n    bookCount\n    __typename\n  }\n}\n"

FIELDNAMES_AUTHOR = [
    "count",
    "from_query",
    "from_search_book_api",
    "id",
    "name",
    "slug",
    "__typename",
    "book_id",
    "book_title"
]
FIELDNAMES_REC_BOOKS = [
    "count",
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
    "gradientColors",
    "workId",
    "__typename",
]
FIELDNAMES_SEARCH_SHELVES = [
    "count",
    "from_query",
    "id",
    "slug",
    "title",
    "description",
    "profileId",
    "owner",
]
FIELDNAMES_SEARCH_CLUBS = [
    "count",
    "from_query",
    "from_search_book_api",
    "id",
    "name",
    "handle",
    "description",
    "languages",
    "updatedAt",
    "createdAt",
    "image",
    "__typename",
    # "memberships", # not necessary
]
FIELDNAMES_GET_CLUB_BOOKS = [
    "count",
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
    "gradientColors",
    "workId",
    "__typename",
]
FIELDNAMES_SEARCH_BOOKS = [
    "count",
    "from_query",
    "from_search_book_api",
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
    "authors",  # Author[] id, name, slug, __typename
    "gradientColors",  # List[str]
    "workId",
    "__typename"
]
FIELDNAMES_AUTHOR_BY_SLUG_OR_ID = [
    "count",
    "id",
    "name",
    "slug",
    "aliases",
    "description",
    "image",
    "updatedAt",
    "__typename"
]
FIELDNAMES_GET_BOOKS_ON_SHELF_COUNT = [
    "count",
    "shelfId",
    "bookCount",
]
FIELDNAMES_BOOKS_BY_SHELF = [
    *FIELDNAMES_SEARCH_BOOKS,
    "shelf_slug",
    "request_slug_offset"
]

#
# operations
#

SEARCH_CLUBS_OPS = {
    "name": "searchClubs",
    "body": BODY_SEARCH_CLUBS,
    "csv": "search_clubs.csv",
    "fieldnames": FIELDNAMES_SEARCH_CLUBS
}
GET_CLUB_BOOKS = {
    "name": "getClubBooks",
    "body": BODY_GET_CLUB_BOOKS,
    "csv": "get_club_books.csv",
    "fieldnames": FIELDNAMES_SEARCH_BOOKS
}
SEARCH_SHELVES = {
    "name": "searchShelves",
    "body": BODY_SEARCH_SHELVES,
    "csv": "search_shelves.csv",
    "fieldnames": FIELDNAMES_SEARCH_SHELVES
}
BOOKS_BY_SHELF = {
    "name": "booksByShelf",
    "body": BODY_BOOKS_BY_SHELF,
    "csv": "books_by_shelf.csv",
    "fieldnames": FIELDNAMES_BOOKS_BY_SHELF
}
BOOKS_BY_AUTHOR = {
    "name": "booksByAuthor",
    "body": BODY_BOOKS_BY_AUTHOR,
    "csv": "books_by_author.csv",
    "fieldnames": FIELDNAMES_SEARCH_BOOKS
}
BOOKS_AUTHOR_BY_SLUG_OR_ID = {
    "name": "authorBySlugOrId",
    "body": BODY_AUTHOR_BY_SLUG_OR_ID,
    "csv": "author_by_slug_or_id.csv",
    "fieldnames": FIELDNAMES_AUTHOR_BY_SLUG_OR_ID
}
BOOKS_GET_BOOKS_ON_SHELF_COUNT = {
    "name": "getBooksOnShelfCountsByShelfIds",
    "body": BODY_GET_BOOKS_ON_SHELF_COUNT,
    "csv": "book_count_on_shelves.csv",
    "fieldnames": FIELDNAMES_GET_BOOKS_ON_SHELF_COUNT
}
CSV_DATASET = "literal-split-0.csv"
CSV_HEADER = "id,slug,title,subtitle,description,isbn10,isbn13,language,pageCount,publishedDate,publisher,physicalFormat,cover,authors,filter,owner,name,handle,languages,updatedAt,createdAt,image,bio,invitedByProfileId"
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

CLEAN_CLUB_CSV = "clean_search_clubs.csv"
