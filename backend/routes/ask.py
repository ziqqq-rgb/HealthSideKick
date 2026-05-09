from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from logger import logger
from modules.rag_engine import ask_database

from utilities.auth import get_current_user
from models.user import User

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/ask/")
async def ask_question(
    request: QueryRequest,
    current_user: User = Depends(get_current_user) 
):

    logger.info(f"📩 Received question from User {current_user.id}: '{request.question}'")
    
    try:

        formatted_user_id = f"user_{current_user.id}"
        
        answer = ask_database(request.question, formatted_user_id)
        
        logger.info(f"✅ Successfully generated answer.")
        return {"answer": answer}
    
    except Exception as e:
        logger.error(f"Error during RAG chain execution: {e}")
        raise HTTPException(status_code=500, detail="Error processing the question.")