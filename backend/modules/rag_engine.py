import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings 
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from logger import logger

load_dotenv()
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
vector_store = PineconeVectorStore(index_name=PINECONE_INDEX_NAME, embedding=embeddings)
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0, max_tokens=1024)

prompt_template = """
You are HealthSideKick, an expert clinical guidelines assistant.
Answer the user's question using ONLY the provided context from the medical manual.
If the answer is not contained in the context, do not guess. Simply say: "I'm sorry, but I cannot find the answer to this in the provided clinical guidelines."

Context:
{context}

Question: 
{question}

Answer:"""

prompt = ChatPromptTemplate.from_template(prompt_template)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def ask_database(question: str, user_id: str):
    logger.info(f"🔍 Searching Pinecone specifically for {user_id}...")
    
    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": 5,
            "filter": {"user_id": user_id}  
        }
    )

    rag_chain = (
        {"question": RunnablePassthrough(), "context": retriever | format_docs} 
        | prompt 
        | llm 
        | StrOutputParser()
    )
    
    return rag_chain.invoke(question)