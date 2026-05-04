import os
from dotenv import load_dotenv
from llama_parse import LlamaParse
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()
LLAMA_API_KEY = os.getenv("LLAMAPARSE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

def parse_document(file_path: str) -> str:

    try:

        parser = LlamaParse(
            api_key = LLAMA_API_KEY,
            result_type="markdown",
            verbose=True
        )

        documents = parser.load_data(file_path)

        return documents
    
    except Exception as e:
        print(f"Error initializing LlamaParse: {e}")
        return None

def chunk_and_store(parsed_docs):
    try:
        
        full_markdown_text = "\n\n".join([page.text for page in parsed_docs])

        headers_to_split_on = [

            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        
        markdown_splitter = MarkdownHeaderTextSplitter(

            headers_to_split_on=headers_to_split_on, 
            strip_headers=False
        )

        structured_chunks = markdown_splitter.split_text(full_markdown_text)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500, 
            chunk_overlap=200
        )

        final_chunks = text_splitter.split_documents(structured_chunks)
        
        
        embedding = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

        vector_store = PineconeVectorStore.from_documents(
            documents=final_chunks,
            index_name=PINECONE_INDEX_NAME,
            embedding=embedding
        )
        print("SUCCESS! Phase 2 Complete. Check your Pinecone Dashboard now!")
        
    except Exception as e:
        print(f"Error in chunking and storing: {e}")


# test the function
if __name__ == "__main__":

    file_path = "./data/sample2.pdf" 

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")

    else:
        parsed_content = parse_document(file_path)
        if parsed_content:
            chunk_and_store(parsed_content)