# app/main.py
"""
FastAPI application factory and configuration.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def create_application() -> FastAPI:
    """Create and configure FastAPI application"""
    
    # Import settings
    from app.core.config import settings
    
    # Create FastAPI app
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Configure CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Request timing middleware
    @application.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    # Global exception handler
    @application.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Global exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "error": str(exc)}
        )

    # Include API router
    try:
        from app.api.v1.api import api_router
        application.include_router(api_router, prefix=settings.API_V1_STR)
        logger.info("API router included successfully")
    except ImportError as e:
        logger.error(f"Failed to import API router: {e}")
        # Create a minimal router as fallback
        from fastapi import APIRouter
        fallback_router = APIRouter()
        
        @fallback_router.get("/health")
        async def fallback_health():
            return {"status": "API router failed to load", "error": str(e)}
        
        application.include_router(fallback_router, prefix=settings.API_V1_STR)

    return application

# Create the app instance
app = create_application()

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Report System API starting up...")

# Shutdown event  
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("👋 Report System API shutting down...")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Report System API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )