import math

import pandas as pd
import csv
import time

from constants import FIELDNAMES_BOOKS_BY_SHELF

dtype = {
    "count": "string",
    "from_query": "string",
    "from_search_book_api": "string",
    "id": "string",
    "slug": "string",
    "title": "string",
    "subtitle": "string",
    "description": "string",
    "isbn10": "string",
    "isbn13": "string",
    "language": object,
    "pageCount": "string",
    "publishedDate": "string",
    "publisher": "string",
    "physicalFormat": "string",
    "cover": "string",
    "authors": object,  # Author[] id, name, slug, __typename
    "gradientColors": object,  # List[str]
    "workId": "string",
    "__typename": "string",

    "shelf_slug": "string",
    "request_slug_offset": "string",
}
cleaned_dtype = {
    "id": "string",
    "slug": "string",
    "title": "string",
    "subtitle": "string",
    "description": "string",
    "isbn10": "string",
    "isbn13": "string",
    "language": object,
    "pageCount": "string",
    "publishedDate": "string",
    "publisher": "string",
    "physicalFormat": "string",
    "cover": "string",
    "authors": object,  # Author[] id, name, slug, __typename
}

combined_first_clean_count = 0


def clean_split_datasets():
    split_count = 1

    while split_count < 50:
        split_name = f"books_by_shelf/split-{split_count}.csv"
        cleaned_split_name = f"cleaned_books_by_shelf/cleaned-{split_count}.csv"

        # split_name = f"second_cleaning_books_by_shelf/combined-{split_count}-{split_count+3}.csv"
        # cleaned_split_name = f"second_cleaning_books_by_shelf/cleaned-combined-{split_count}-{split_count+3}.csv"

        df = pd.read_csv(split_name, dtype=dtype)

        # drop columns
        # columns_to_drop = ["gradientColors", "workId", "__typename", "shelf_slug",
        #                    "request_slug_offset", "count", "from_query", "from_search_book_api"]
        # df.drop(columns_to_drop, axis=1, inplace=True)

        # remove duplicates
        df.drop_duplicates(subset="id", keep="first", inplace=True)
        df.to_csv(cleaned_split_name, index=False)

        split_count += 1


def count_first_cleaned_splits():
    entry_count = 0
    split_count = 46
    total_unique_count = 0

    while split_count < 50:
        # cleaned_split_name = f"cleaned_books_by_shelf/cleaned-{split_count}.csv"
        cleaned_split_name = f"second_cleaning_books_by_shelf/combined-{split_count}-{split_count + 3}.csv"

        df = pd.read_csv(cleaned_split_name, dtype=dtype)
        entry_count += len(df["id"])
        total_unique_count += len(df["id"].unique())
        print(
            f"\n{cleaned_split_name} = {len(df['id'])} entries.\nTotal entry count: {entry_count}\n\n")  # 1,069,769

        # with open("count_first_cleaned_splits.csv", "a", newline="") as out:
        with open("count_combined_splits.csv", "a", newline="") as out:
            _writer = csv.DictWriter(
                out, fieldnames=["filename", "count", "unique", "total_unique_count"], )
            _writer.writerow({
                "filename": cleaned_split_name,
                "count": len(df["id"]),
                "unique": len(df["id"].unique()),
                "total_unique_count": total_unique_count
            })

        split_count += 4


def combine_first_cleaned_datasets():
    split_count = 46
    while split_count < 50:
        cleaned_split_name_1 = f"cleaned_books_by_shelf/cleaned-{split_count}.csv"
        cleaned_split_name_2 = f"cleaned_books_by_shelf/cleaned-{split_count + 1}.csv"
        cleaned_split_name_3 = f"cleaned_books_by_shelf/cleaned-{split_count + 2}.csv"
        cleaned_split_name_4 = f"cleaned_books_by_shelf/cleaned-{split_count + 3}.csv"
        # cleaned_split_name_5 = f"cleaned_books_by_shelf/cleaned-{split_count+4}.csv"
        combined_cleaned_name = f"second_cleaning_books_by_shelf/combined-{split_count}-{split_count + 3}.csv"

        df1 = pd.read_csv(cleaned_split_name_1, dtype=cleaned_dtype)
        df2 = pd.read_csv(cleaned_split_name_2, dtype=cleaned_dtype)
        df3 = pd.read_csv(cleaned_split_name_3, dtype=cleaned_dtype)
        df4 = pd.read_csv(cleaned_split_name_4, dtype=cleaned_dtype)
        # df5 = pd.read_csv(cleaned_split_name_5, dtype=cleaned_dtype)

        resulting_df = pd.concat([df1, df2, df3, df4]).to_csv(
            combined_cleaned_name, index=False)
        split_count += 4


def combine_n_clean_2nd_cleaned_datasets():
    combined_cleaned_name = "second_cleaning_books_by_shelf/combine_n_clean_2nd_cleaned_datasets.csv"

    name_count = 0
    filenames = []

    while name_count < 44:
        filenames.append(
            f"second_cleaning_books_by_shelf/cleaned-combined-{name_count + 1}-{name_count + 5}.csv")

        name_count += 5

    filenames.append(
        "second_cleaning_books_by_shelf/cleaned-combined-46-49.csv")

    # dfs = [pd.read_csv(fname, dtype=cleaned_dtype) for fname in filenames]
    # resulting_df = pd.concat(dfs).to_csv(combined_cleaned_name, index=False)

    resulting_df = pd.read_csv(
        "second_cleaning_books_by_shelf/combine_2nd_cleaned_datasets.csv", dtype=cleaned_dtype)
    ids = resulting_df['id']
    print(f"uniques: {len(ids.unique())}, rows: {len(ids)}")
    resulting_df.drop_duplicates(subset="id", keep="first", inplace=True)
    resulting_df.to_csv(combined_cleaned_name, index=False)


def combine_books():
    f1 = "combine_n_clean_2nd_cleaned_datasets.csv"
    f2 = "combined_search_books.csv"
    combined_name = "combined_books.csv"

    # ['id', 'slug', 'title', 'subtitle', 'description', 'isbn10', 'isbn13',
    # 'language', 'pageCount', 'publishedDate', 'publisher', 'physicalFormat',
    # 'cover', 'authors']
    # df1 = pd.read_csv(f1, dtype=cleaned_dtype)
    # print(df1.columns)

    # ['count', 'from_query', 'from_search_book_api', 'id', 'slug', 'title',
    # 'subtitle', 'description', 'isbn10', 'isbn13', 'language', 'pageCount',
    # 'publishedDate', 'publisher', 'physicalFormat', 'cover', 'authors',
    # 'gradientColors', 'workId', '__typename']
    # df2 = pd.read_csv(f2)
    # print(df2.columns)
    # columns_to_drop = ["count", "from_query", "from_search_book_api",
    #                    "gradientColors", "workId", "__typename", ]
    # df2.drop(columns_to_drop, axis=1, inplace=True)
    # print(df2.columns)

    # combine dataframes
    # resulting_df = pd.concat([df1, df2]).to_csv(combined_name, index=False)

    resulting_df = pd.read_csv(combined_name, dtype=cleaned_dtype)
    resulting_ids = resulting_df["id"]
    print(
        f"\n\nCombined books = {len(resulting_ids)}\nUnique count = {len(resulting_ids.unique())}")
    print(resulting_df.columns)

    # keeping last as results from searchBook and searchBookV2 APIs have publishers and publishedDate data
    cleaned = resulting_df.drop_duplicates(subset=["id"], keep="last").to_csv(
        "cleaned_books_combined.csv", index=False)

    cleaned = pd.read_csv("cleaned_books_combined.csv")["id"]
    print(len(cleaned))

    duplicated = pd.DataFrame(resulting_df.duplicated(
        ["id"], keep="last").values, columns=["isDuplicated"])
    print(duplicated.head())

    duplicated.to_csv("duplicated.csv")
    dup = resulting_df.copy(deep=True)
    dup["isDuplicated"] = duplicated["isDuplicated"].copy(deep=True)
    dup.to_csv("duplicated.csv")


def make_demo_dataset():
    # DEFAULT_CSV_HEADER = [
    #     "id",
    #     "slug",
    #     "title",
    #     "subtitle",
    #     "description",
    #     "isbn10",
    #     "isbn13",
    #     "language",
    #     "pageCount",
    #     "publishedDate",
    #     "publisher",
    #     "physicalFormat",
    #     "cover",
    #     "authors",
    #     # shelves
    #     "owner",
    #     # clubs
    #     "name",
    #     "handle",
    #     "languages",
    #     "updatedAt",
    #     "createdAt",
    #     "image",
    #     # profiles
    #     "bio",
    #     "invitedByProfileId",
    #     # general
    #     "filter",
    # ]

    # Index(['id', 'slug', 'title', 'subtitle', 'description', 'isbn10', 'isbn13',
    # 'language', 'pageCount', 'publishedDate', 'publisher', 'physicalFormat',
    # 'cover', 'authors'],
    #     dtype = 'object')
    books = pd.read_csv("cleaned_books_combined.csv", dtype=cleaned_dtype)
    books["filter"] = "books"

    # count, from_query, id, slug, title, description, profileId, owner
    shelves = pd.read_csv("search_shelves.csv")
    shelves.drop(["count", "from_query", "profileId"], inplace=True, axis=1)
    shelves["filter"] = "shelves"

    # count,from_query,from_search_book_api,id,name,handle,description,languages,updatedAt,createdAt,image,__typename
    clubs = pd.read_csv("clean_search_clubs.csv")
    clubs.drop(
        ["count", "from_query", "from_search_book_api", "__typename"], inplace=True, axis=1)
    clubs["filter"] = "clubs"

    # count,id,handle,name,bio,image,invitedByProfileId,__typename
    profiles = pd.read_csv("clean_search_profiles.csv")
    profiles.drop(["count", "__typename"], inplace=True, axis=1)
    profiles["filter"] = "profiles"

    literal_demo_dataset = pd.concat([books, shelves, clubs, profiles]).to_csv(
        "literal_demo_data.csv", index=False)
    literal_demo_dataset = pd.read_csv("literal_demo_data.csv")
    # 583364
    print(len(literal_demo_dataset["id"]))
    # Index(['id', 'slug', 'title', 'subtitle', 'description', 'isbn10', 'isbn13',
    #        'language', 'pageCount', 'publishedDate', 'publisher', 'physicalFormat',
    #        'cover', 'authors', 'filter', 'owner', 'profileId', 'name', 'handle', 'languages',
    #        'updatedAt', 'createdAt', 'image', 'bio',
    #        'invitedByProfileId'],
    #       dtype='object')
    print(literal_demo_dataset.columns)


def split_dataset():
    # read csv
    df = pd.read_csv("dataset-split-1.csv")
    data_len = len(df["id"])
    cols = ["id", "slug", "title", "subtitle", "description", "isbn10", "isbn13", "language", "pageCount",
            "publishedDate", "publisher", "physicalFormat", "cover", "authors", "filter", "owner", "name", "handle",
            "languages", "updatedAt", "createdAt", "image", "bio", "invitedByProfileId"]
    # id,slug,title,subtitle,description,isbn10,isbn13,language,pageCount,publishedDate,publisher,physicalFormat,cover,authors,filter,owner,name,handle,languages,updatedAt,createdAt,image,bio,invitedByProfileId
    count = 0
    batch_size = 50000
    # while count < data_len - 1:
    #     df.iloc[count:count + batch_size].to_csv(f"literal-split-{math.ceil(count / batch_size)}.csv", index=False,
    #                                              columns=cols)
    #     count += batch_size
    df.iloc[:500].to_csv("cute-chunk.csv", index=False, columns=cols)


# combine_n_clean_2nd_cleaned_datasets()
# clean_split_datasets()
# count_first_cleaned_splits()
# combine_first_cleaned_datasets()
# combine_books()
# make_demo_dataset()
split_dataset()
