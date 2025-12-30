"""FastAPI application main file."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from app.api.endpoints import batch, health, predict
from app.config import settings
from app.core.model import get_model
from app.utils.logger import logger
from app.utils.metrics import model_loaded


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting application...")
    try:
        # Load model on startup
        logger.info("Loading sentiment model...")
        get_model()
        logger.info("Application started successfully")
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}", exc_info=True)
        model_loaded.set(0)
        raise

    yield

    # Shutdown
    logger.info("Shutting down application...")


# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    predict.router,
    prefix=f"/api/{settings.api_version}",
    tags=["predictions"],
)

app.include_router(
    batch.router,
    prefix=f"/api/{settings.api_version}",
    tags=["predictions"],
)

app.include_router(
    health.router,
    prefix=f"/api/{settings.api_version}",
    tags=["health"],
)

# Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Customer Sentiment Analysis API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": f"/api/{settings.api_version}/health",
    }


@app.get("/docs")
async def docs_redirect():
    """Redirect to docs."""
    from fastapi.responses import RedirectResponse

    return RedirectResponse(url="/docs")
