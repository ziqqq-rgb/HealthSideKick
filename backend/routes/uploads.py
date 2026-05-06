from fastapi import APIRouter, UploadFile, File
from modules.ingest_data import process_and_upload_pdf

router = APIRouter()

@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):

    try:
        result = await process_and_upload_pdf(file)
        return {"message": "PDF processed and uploaded successfully", "details": result}
    
    except Exception as e:
        return {"error": f"An error occurred: {e}"}