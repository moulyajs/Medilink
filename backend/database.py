import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load .env
load_dotenv()

# Read complete DATABASE_URL
DB_URL = os.getenv("DATABASE_URL")

print("DB_URL =", DB_URL)

if not DB_URL:
    raise RuntimeError("DATABASE_URL is not set in the environment.")

# Create SQLAlchemy engine
engine = create_engine(DB_URL)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

print("Database connected successfully!")