from threading import Thread, local
from typing import Any, List
from queue import Queue


def add_marqo_doc(doc_list, i, mq, index_name):

    try:
        #  add docs
        mq.index(index_name).add_documents(
            doc_list[i:i+100], client_batch_size=100, server_batch_size=100, processes=6)

    except Exception as err:
        f = open("err.log", "a")
        f.write(str(err))
        f.close()

    else:
        print(f"\n\n{doc_list[-1]['id']}")


def test_print(i):
    print(f"Printing {i}")
