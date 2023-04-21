"""
python -m streamlit run test.py
"""
import os
from dotenv import load_dotenv
import streamlit as st
from index import construct_index
from llama_index import (
    SimpleDirectoryReader,
    GPTSimpleVectorIndex,
    LLMPredictor,
    PromptHelper,
    ServiceContext
)

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

doc_path = './data/'
index_file = 'index.json'

if 'response' not in st.session_state:
    st.session_state.response = ''

def send_click():
    st.session_state.response  = index.query(st.session_state.prompt)

index = None
st.title("DataChat")

sidebar_placeholder = st.sidebar.container()
uploaded_files = st.file_uploader(
    label="Upload files",
    type=["pdf","epub","txt","docx","html"],
    accept_multiple_files=True,
)


if len(uploaded_files) > 0:
    print("files present:")
    for file in uploaded_files:
        with open(os.path.join("data", file.name), "wb") as f:
            f.write(file.read())
        print(f"    {file.name}")
    index = construct_index("data")
    print("\ndone")

if index is not None:
    st.text_input("Ask something: ", key='prompt')
    st.button("Send", on_click=send_click)
    if st.session_state.response:
        st.subheader("Response: ")
        print("st.session_state.response", st.session_state.response)
        st.success(st.session_state.response, icon= "🤖")
# elif os.path.exists("index.json"):
#     index = GPTSimpleVectorIndex.load_from_disk("index.json")

# if index != None:
#     st.text_input("Ask something: ", key='prompt')
#     st.button("Send", on_click=send_click)
#     if st.session_state.response:
#         st.subheader("Response: ")
#         st.success(st.session_state.response, icon= "🤖")
