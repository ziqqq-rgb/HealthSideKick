from fastapi import Request
from fastapi.responses import JSONResponse

from logger import logger

async def catch_exceptions_middleware(request: Request, call_next):

    try:

        reponse = await call_next(request)
        return reponse

    except Exception as e:
        logger.exception(f"Critical error occured at {request.url.path}: {str(e)}")

        return JSONResponse(
            status_code=500,
            content={"detail": "An unexpected error occurred. Please try again later."}
        )