from llama_index import (
    SimpleDirectoryReader,
    GPTSimpleVectorIndex,
    LLMPredictor,
    PromptHelper,
    ServiceContext
)
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os


load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def construct_index(directory_path: str, model: str, temperature: float):
    documents = SimpleDirectoryReader(directory_path).load_data()
    llm_predictor = LLMPredictor(
        llm=ChatOpenAI(
            temperature=temperature,
            model_name=model
        )
    )
    service_context = ServiceContext.from_defaults(
        llm_predictor=llm_predictor,
        chunk_size_limit=512
    )
    index = GPTSimpleVectorIndex.from_documents(
        documents=documents,
        service_context=service_context
    )
    print(f"type(index)={type(index)}")
    index.save_to_disk('index.json')
    return index