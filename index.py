from llama_index import (
    SimpleDirectoryReader,
    GPTSimpleVectorIndex,
    LLMPredictor,
    PromptHelper,
    ServiceContext
)
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os


load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def construct_index(directory_path: str, model: str, temperature: int):
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
        llm=ChatOpenAI(
            temperature=temperature,
            model_name=model,
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
    print(f"type(index)={type(index)}")
    index.save_to_disk('index.json')
    return index