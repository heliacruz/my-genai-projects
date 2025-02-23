import streamlit as st
import config
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_community.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain

st.header("PDF Reader ChatBot By H.Cruz")
with st.sidebar:
    st.title("Upload your Document here")
    file = st.file_uploader("Upload a PDF file and ask your question", type="pdf")

if file is not None:
    # Extract text from all pages
    reader = PdfReader(file)
    content = ""
    for page in reader.pages:
        content += page.extract_text()

    # Break text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        separators="\n",
        chunk_size=1024,
        chunk_overlap=150,
        length_function=len
    )
    chunks = text_splitter.split_text(content)

    # Create embeddings and vector store using the API key from config
    embeddings = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)
    vector_store = FAISS.from_texts(chunks, embeddings)

    # Create a text input element for your query
    user_input = st.text_input("Enter your query:", key="query_input")

    if user_input:
        matches = vector_store.similarity_search(user_input)

        # Setup the LLM model using the API key from config
        llm = ChatOpenAI(
            openai_api_key=config.OPENAI_API_KEY,
            temperature=0,
            max_tokens=1000,
            model_name="gpt-3.5-turbo"
        )
        # Load QA chain and run the query
        chain = load_qa_chain(llm, chain_type="stuff")
        output = chain.run(input_documents=matches, question=user_input)
        st.write(output)
