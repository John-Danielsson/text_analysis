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
    """
    Constructs an index from documents in a specified directory using a language model.

    This function reads documents from the given directory, initializes a language model
    predictor with specified parameters, and constructs an index for the documents using
    the language model. The index is then saved to disk.

    Parameters:
    ----------
    directory_path : str
        The path to the directory containing the documents to be indexed.
    model : str
        The name of the language model to be used for indexing.
    temperature : float
        The temperature setting for the language model, controlling the randomness
        of the model's responses.

    Returns:
    -------
    GPTSimpleVectorIndex
        The constructed index object for the given documents.
    """
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
