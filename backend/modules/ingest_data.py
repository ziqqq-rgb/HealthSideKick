import os
from time import time
from uuid import uuid4
from datetime import datetime, timezone
from fastapi import UploadFile
from dotenv import load_dotenv
from llama_parse import LlamaParse
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
import shutil

from logger import logger

load_dotenv()
LLAMA_API_KEY = os.getenv("LLAMAPARSE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
UPLOAD_DIR = "./uploaded_files"

def save_uploaded_file(files: UploadFile) -> str:

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, files.filename)

    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(files.file, f)
        return file_path
    
    except Exception as e:
        logger.error(f"Error saving uploaded file: {e}")
        raise e
        

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

def chunk_and_store(parsed_docs, file_name: str, user_id: str, file_id: str, upload_date: str):
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

        for chunk in final_chunks:
            chunk.metadata.update({
                "file_name": file_name,
                "user_id": user_id,
                "file_id": file_id,
                "upload_date": upload_date
            })
        
        
        embedding = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

        vector_store = PineconeVectorStore.from_documents(
            documents=final_chunks,
            index_name=PINECONE_INDEX_NAME,
            embedding=embedding
        )

        batch_size = 50
        logger.info(f"⏳ Uploading to Pinecone in batches of {batch_size}...")
        
        for i in range(0, len(final_chunks), batch_size):
            batch = final_chunks[i : i + batch_size]
            vector_store.add_documents(batch)
            logger.info(f"   -> Uploaded chunks {i} to {i + len(batch)}")
            
            if i + batch_size < len(final_chunks):
                logger.info("   💤 Sleeping 10s to respect Google API limits...")
                time.sleep(10)

        logger.info("✅ SUCCESS! Phase 2 Complete. Check your Pinecone Dashboard now!")

        
    except Exception as e:
        logger.error(f"Error in chunking and storing: {e}")
        raise e

async def process_and_upload_pdf(file: UploadFile, user_id: str) -> dict:

    file_path = None

    try:
        
        file_id = f"doc_{uuid4().hex[:8]}"
        upload_date = datetime.now(timezone.utc).isoformat()

        logger.info("Starting PDF processing and upload...")

        file_path = save_uploaded_file(file)
        parsed_content = parse_document(file_path)

        if parsed_content:
            chunk_and_store(
                parsed_docs=parsed_content, 
                file_name=file.filename, 
                user_id=user_id, 
                file_id=file_id, 
                upload_date=upload_date
            )

        return {
            "status": "success",
            "message": file.filename,
            "file_id": file_id
        }
    except Exception as e:
        logger.error(f"Error processing and uploading PDF: {e}")
        return {
            "status": "error",
            "message": str(e)
        }
    
    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Cleaned up uploaded file: {file_path}")

