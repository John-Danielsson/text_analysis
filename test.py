from llama_index import (
    SimpleDirectoryReader,
    GPTListIndex,
    readers,
    GPTSimpleVectorIndex,
    LLMPredictor,
    PromptHelper,
    ServiceContext
)
from langchain import OpenAI
import sys
import os
from IPython.display import Markdown, display

def construct_index(directory_path):
    max_input_size = 4096
    num_outputs = 2000
    max_chunk_overlap = 20
    chunk_size_limit = 600
    prompt_helper = PromptHelper(
        max_input_size,
        num_outputs,
        max_chunk_overlap,
        chunk_size_limit=chunk_size_limit
    )
    llm_predictor = LLMPredictor(
        llm=OpenAI(
            temperature=0.5,
            model_name="text-davinci-003",
            max_tokens=num_outputs
        )
    )
    documents = SimpleDirectoryReader(directory_path).load_data()
    service_context = ServiceContext.from_defaults(
        llm_predictor=llm_predictor,
        prompt_helper=prompt_helper
    )
    index = GPTSimpleVectorIndex.from_documents(
        documents=documents,
        service_context=service_context
    )
    index.save_to_disk('index.json')
    # return index

# def ask_ai():
#     index = GPTSimpleVectorIndex.load_from_disk('index.json')
#     while True:
#         query = input("What do you want to ask? ")
#         response = index.query(query)
#         display(Markdown(f"Response: <b>{response.response}</b>"))

if __name__ == "__main__":
    index = construct_index("test_pdfs_zoltan")
    print('construct_index() success')
    answer = index.query("Write a summary of Zoltan's writings.")
    print('    index.query() success')
    print("answer:", answer)
