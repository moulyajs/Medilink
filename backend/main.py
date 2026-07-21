from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.patient import Patient
from models.profile import Profile
from models.otp import EmailOTP
from database import Base, engine
from routers.profile import router as profile_router
from routers.auth import router as auth_router
from routers.chat import router as chat_router
from routers.upload import router as upload_router
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
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(chat_router)
app.include_router(upload_router)