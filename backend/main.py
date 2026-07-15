from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routers.profile import router as profile_router
# Create database tables
Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Medilink API",
    description="Backend API for Medilink",
    version="1.0.0"
)

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Later replace with frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Welcome to Medilink API 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
app.include_router(profile_router)