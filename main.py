from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.routers.outlook_router import router as outlook_router
from app.routers.teams_router import router as teams_router
from app.routers.analytics_router import router as analytics_router

# Initialize FastAPI app
app = FastAPI(
    title="Microsoft Graph SDK API",
    description="Email and Teams Chat extraction API for MuznyM@Muzny986.onmicrosoft.com",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(outlook_router)
app.include_router(teams_router)
app.include_router(analytics_router)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "service": "Microsoft Graph SDK API",
        "version": "0.1.0",
        "endpoints": {
            "health": "/health",
            "outlook_emails": "/outlook/emails",
            "teams_chats": "/teams/chats",
            "outlook_analytics": "/analytics/outlook/analyze",
            "teams_analytics": "/analytics/teams/analyze",
        }
    }


@app.get("/health")
async def health_check():
    """Simple health check endpoint to verify server is working"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "Microsoft Graph SDK API",
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
