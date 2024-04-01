from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.core.schema import QueryBundle
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from create_index import create_or_load_index
from templates import template

index = create_or_load_index()

def get_relevant_nodes_from_retreiver(query):
    reranker = SentenceTransformerRerank(top_n=5)

    retriever = index.as_retriever()
    nodes = retriever.retrieve(query)

    nodes = reranker.postprocess_nodes(nodes, QueryBundle(query))
    print(nodes)
    texts = [node.node.text for node in nodes]
    metadata = [node.node.metadata for node in nodes]


    # for n in nodes:
    #     print(n)

    return texts, metadata


def get_query_response(query):
    texts, metadata = get_relevant_nodes_from_retreiver(query)
    model = ChatOpenAI(temperature=0)

    prompt = ChatPromptTemplate.from_template(template)

    chain = prompt | model

    response = chain.stream({
        "docs": texts,
        "query": query,
        "metadata": metadata
    })

    return response
    




# get_query_response("Where is Aryaka's software stack hosted on?")