# app/main.py

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as simulation_router


app = FastAPI(title="SimImpact API", version="0.1")

# Enable CORS for frontend requests
app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:3000"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# Register routes
app.include_router(simulation_router, prefix="/api")
