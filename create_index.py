import os

from dotenv import load_dotenv, find_dotenv
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from llama_index.core import Document
from llama_index.readers.file.markdown.base import MarkdownReader
# from llama_index.core.node_parser import TokenTextSplitter, MarkdownNodeParser
# from llama_index.readers.file import FlatReader
from llama_index.core import ServiceContext
from pathlib import Path

from configs import Configs

load_dotenv(find_dotenv())

def metadata_extractor(file_name):
    file_name = file_name.split("\\")[-1]
    page_url = "https://" + "/".join(file_name[:-3].split("-"))
    print(page_url)
    metadata = {
        "page_url": page_url,
        "topics": [],
        "image_links": [],
    }
    with open(os.path.join(Configs.DATA_DIR, file_name), encoding="utf8") as f:
        for idx, line in enumerate(f.readlines()):
            if line.startswith("# "):
                if idx == 0:
                    metadata["title"] = line[2:-1]
                metadata["topics"].append(line[2:-1])
            if line.startswith("![]("):
                metadata["image_links"].append(line[4:-2])
    return metadata


def create_or_load_index():
    # check if storage already exists
    if not os.path.exists(Configs.PERSIST_DIR):
        # load the documents and create the index
        documents = SimpleDirectoryReader(
            input_dir=Configs.DATA_DIR,
            required_exts=[".md"],
            file_extractor={".md": MarkdownReader()},
            filename_as_id=True,
            file_metadata=metadata_extractor,
        ).load_data()
        service_context = ServiceContext.from_defaults(chunk_size=1500, chunk_overlap=30)
        index = VectorStoreIndex.from_documents(documents, service_context=service_context)

        # store it for later
        index.storage_context.persist(persist_dir=Configs.PERSIST_DIR)
        print('Index Created!')
    else:
        # load the existing index
        storage_context = StorageContext.from_defaults(persist_dir=Configs.PERSIST_DIR)
        index = load_index_from_storage(storage_context)

    return index

# retriever = index.as_retriever(
#     vector_store_query_mode="mmr",
#     similarity_top_k=3,
#     vector_store_kwargs={"mmr_threshold": 0.1},
# )
# nodes = retriever.retrieve(
#     "Explain edge routed mode with a single-homed gateway??"
# )


# for n in nodes:
#     print(n)

# metadata_extractor('docs.aryaka.com-space-TBW-1639471.md')