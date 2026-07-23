#---------------------------------------------------------------------------------
#                                   Import Statements
#---------------------------------------------------------------------------------
import logging 
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from beanie import init_beanie
from pymongo import AsyncMongoClient
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.config import settings 
from backend.models.db_models import User, UsageStat
from backend.routers import auth
from backend.middleware.rate_limiter import limiter,rate_limit_exceeded_handler

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

#---------------------------------------------------------------------------------
#                              Life Span(starup /shutdown)
#---------------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app : FastAPI):
    logger.info("Connecting to MongoDB")
    client = AsyncMongoClient(settings.mongodb_url)
    await init_beanie(
        database=client[settings.mongodb_db_name],
        document_models=[
            User,
            UsageStat
        ],
    )
    logger.info("MongoDB Connected ✔️")

    yield 
    # Shutdown
    await client.close()
    logger.info("MongoDB Disconnected.")

#---------------------------------------------------------------------------------
#                                     App Factory
#---------------------------------------------------------------------------------

def create_app() -> FastAPI:
    app = FastAPI(
        title = "Multi-Tenant RAG SaaS API",
        description= (
            "Per-user isolated knowledge bases powered by"
            "Pinecone ~ OpenAI Embeddings ~ Groq LLaMA ~ MongoDB"
        ),
        version = "1.0.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Slowapi rate limiter state 
    app.state.limiter = limiter 
    app.add_exception_handler(RateLimitExceeded , rate_limit_exceeded_handler)

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins = settings.origins_list,
        allow_credentials = True,
        allow_methods = ["*"],
        allow_headers = ["*"]
    )

    # Routers
    app.include_router(auth.router , prefix="/api/v1")

    # Health check route 
    @app.get("/health" , tags = ['System'])
    async def health():
        return {"status" : "ok" , "version" : "1.0.0"}

    # Global exception handler 
    @app.exception_handler(Exception)
    async def global_exception_handler(request : Request , exc : Exception):
        logger.error(f"Unhandled exception : {exc}" , exc_info = True)
        return JSONResponse (
            status_code=500,
            content = {"detail" : "Internal server error. Please try again later."}
        )

    return app 


app = create_app() 
