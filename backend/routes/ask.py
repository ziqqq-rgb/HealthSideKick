from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from logger import logger
from modules.rag_engine import setup_rag_chain

router = APIRouter()

rag_chain = setup_rag_chain()

class QueryRequest(BaseModel):
    question: str

@router.post("/ask")
async def ask_question(request: QueryRequest):

    logger.info(f"📩 Received question: '{request.question}'")

    if not rag_chain:
        logger.error("RAG chain is not initialized.")
        raise HTTPException(status_code=500, detail="RAG chain is not initialized.")
    
    try:

        answer = rag_chain.invoke(request.question)
        logger.info(f"✅ Successfully generated answer for the question.")
        return {"answer": answer}
    
    except Exception as e:
        logger.error(f"Error during RAG chain execution: {e}")
        raise HTTPException(status_code=500, detail="Error processing the question.")