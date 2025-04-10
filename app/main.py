"""
Main application module for the Common Assessment Tool.
This module initializes the FastAPI application and includes all routers.
Handles database initialization and CORS middleware configuration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models
from app.database import engine
from app.clients.router import router as clients_router
from app.auth.router import router as auth_router
import subprocess
import os

# Initialize database tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title="Case Management API",
    description="API for managing client cases",
    version="1.0.0",
)

# Include routers
app.include_router(auth_router)
app.include_router(clients_router)


@app.get("/health")
async def health():
    return {"status": "ok"}

@app.on_event("startup")
async def run_script_once():
    marker_file = "/code/.data_init"

    if not os.path.exists(marker_file):
        subprocess.Popen(["python", "initialize_data.py"])
        with open(marker_file, "w") as f:
            f.write("done")

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
    allow_credentials=True,
)
