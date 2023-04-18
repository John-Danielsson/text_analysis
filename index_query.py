from llama_index import (
    SimpleDirectoryReader,
    GPTSimpleVectorIndex,
    LLMPredictor,
    PromptHelper,
    ServiceContext
)
from langchain import OpenAI
import openai
from dotenv import load_dotenv
from os import getenv
from textwrap import wrap


class IndexQuery:
    def __init__(self, directory_path: str):
        self.directory_path = directory_path
        load_dotenv()
        openai.api_key = getenv("OPENAI_API_KEY")
        # set maximum input size
        max_input_size = 4096
        # set number of output tokens
        num_outputs = 2000
        # set maximum chunk overlap
        max_chunk_overlap = 20
        # set chunk size limit
        chunk_size_limit = 600
        # define prompt helper
        prompt_helper = PromptHelper(
            max_input_size,
            num_outputs,
            max_chunk_overlap,
            chunk_size_limit=chunk_size_limit
        )
        # define LLM
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
            documents,
            service_context=service_context
        )
        index.save_to_disk('index.json')
        self.vector_index = GPTSimpleVectorIndex.load_from_disk('index.json')



    def __str__(self) -> str:
        return f"IndexQuery(\"{self.directory_path}\")"

    def ask(self, question: str) -> str:
        return self.vector_index.query(question).response


if __name__ == "__main__":
    pass
    # index = IndexQuery("test_files")
    # answer = index.ask("Write a TL;DR of Zoltan's writing.")
    # print(answer)

"""Zoltan's writing discusses the concept of
operating leverage in the military domain, and how
it applies to the current situation in which the
U.S. is facing a two-front war. He argues that the
U.S. needs protection from Pax Americana in order
to maintain the global supply chain and order, and
suggests that the challenge should be dealt with
quickly and decisively, in the spirit of the
Powell Doctrine. He also mentions that Tim
Geithner's advice on how to deal with crises such
as the Asian financial crisis and the potential
vulnerabilities of the U.S. banking system should
be considered. He further notes that the U.S.
needs to be aware of its capacity to produce,
referencing Simon Kuznets' work to develop the
U.S. national accounts to gauge the capacity to
fight WWII, and suggests using technology
sanctions to shape future outcomes, such as
slowing progress to buy time and preserve the
balance of technological power in favor of the
U.S. He also mentions the potential of using
measures such as limiting shipments of chipmaking
equipment to producers of memory chips in China,
as a negotiating tool to force Seoul to reconsider
its stance, and suggests considering the
inflationary consequences of Russia and China
challenging the U.S. hegemon. He argues that the
West needs to pour trillions into four types of
projects to overcome the risks posed by our
commodities, re-arm to defend the world order, re-
shore to get around blockades, re-stock and invest
in commodities, and re-wire the grid for an energy
transition. He suggests that this is the tab for
the currently unfolding Great Crisis of
Globalization, and that the EU is also busy
funding fabs to regain industrial sovereignty. He
emphasizes the need for governments to commit to
re-wiring the grid and to build inventories of
commodities to cover residential and industrial
needs for the next three years. He suggests that
if Tim Geithner was in charge, a lot of money
would be put in the window to show that the global
order is at stake, and that any investor should be
mindful of the need to re-arm, re-shore, re-stock
and re-wire the electric grid as the defining aims
of industrial policy over the next five years."""