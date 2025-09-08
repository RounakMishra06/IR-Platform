from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.routes import detection, containment, eradication, recovery, post_incident
from app.core.config import settings
from app.core.database import engine, Base
import uvicorn

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Incident Response Platform API",
    description="Centralized platform for incident response management",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(detection.router, prefix="/api/detection", tags=["Detection"])
app.include_router(containment.router, prefix="/api/containment", tags=["Containment"])
app.include_router(eradication.router, prefix="/api/eradication", tags=["Eradication"])
app.include_router(recovery.router, prefix="/api/recovery", tags=["Recovery"])
app.include_router(post_incident.router, prefix="/api/post-incident", tags=["Post-Incident"])

@app.get("/")
async def root():
    return {"message": "Incident Response Platform API", "status": "online"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
