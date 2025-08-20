# app/main.py

from fastapi import FastAPI, Depends

import os
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as simulation_router



app = FastAPI(title="SimImpact API", version="0.1")

# Enable CORS for frontend requests
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
app.add_middleware(
	CORSMiddleware,
	allow_origins=allowed_origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# Register routes
app.include_router(simulation_router, prefix="/api")
