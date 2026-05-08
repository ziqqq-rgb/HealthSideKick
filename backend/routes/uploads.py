from fastapi import APIRouter, UploadFile, File, Depends
from modules.ingest_data import process_and_upload_pdf

from utilities.auth import get_current_user
from models.user import User

router = APIRouter()

@router.post("/upload-pdf/")
async def upload_pdf(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):

    try:

        formatted_user_id = f"user_{current_user.id}"

        result = await process_and_upload_pdf(file, user_id=formatted_user_id)
        return {"message": "PDF processed and uploaded successfully", "details": result}
    
    except Exception as e:
        return {"error": f"An error occurred: {e}"}