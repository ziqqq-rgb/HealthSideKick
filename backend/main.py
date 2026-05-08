from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from logger import logger
from middlewares.exceptions import catch_exceptions_middleware
from routes.ask import router as ask_router
from routes.uploads import router as uploads_router
from database import engine, Base
from models import user

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting HealthSideKick Server...")
    logger.info("🔧 Initializing database...")

    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database initialized successfully!")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")

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
app.include_router(uploads_router)

