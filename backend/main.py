import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings 
from langchain_pinecone import PineconeVectorStore
from langchain_groq import ChatGroq
from langchain_core.prompts  import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

def format_docs(docs):

    return "\n\n".join(doc.page_content for doc in docs)

def setup_rag_chain():

    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

    vector_store = PineconeVectorStore(
        index_name=PINECONE_INDEX_NAME,
        embedding=embeddings
    )

    retriever = vector_store.as_retriever(search_kwargs={"k": 5})

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
        max_tokens=1024
    )

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

    rag_chain = (
        {"question": RunnablePassthrough(), "context": retriever | format_docs} | prompt | llm | StrOutputParser())
    
    return rag_chain

def main():

    try:

        chain = setup_rag_chain()
        print("\n✅ HealthSideKick is ready! Type 'exit' to quit.\n")

        while True:
            question = input("Your question: ")

            if question.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            print("🤖 HealthSideKick: ", end="", flush=True)
            
            # Use .stream() for a fast, modern typing effect
            for chunk in chain.stream(question):
                print(chunk, end="", flush=True)
            print("\n")

    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    main()