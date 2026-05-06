from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from logger import logger
from middlewares.exceptions import catch_exceptions_middleware
from routes.ask import router as ask_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting HealthSideKick Server...")
    yield
    logger.info("🛑 Shutting down HealthSideKick Server...")

app = FastAPI( 

    title="HealthSideKick API", 
    version="1.0", 
    lifespan=lifespan
)

app.middleware("http")(catch_exceptions_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(ask_router)

