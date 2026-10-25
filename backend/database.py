
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DB_URL = DATABASE_URL

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in the environment.")

DB_SCHEMA = os.getenv("DB_SCHEMA")

# Keep the existing SSL configuration.
connect_args = {"sslmode": "require"}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)

# Preserve schema translation for ORM-generated SQL.
if DB_SCHEMA:
    engine = engine.execution_options(
        schema_translate_map={None: DB_SCHEMA}
    )

# Route raw SQL to the isolated test schema.
# This runs for every newly established DBAPI connection.
if DB_SCHEMA == "integration_test":
    @event.listens_for(engine, "connect")
    def set_integration_test_search_path(
        dbapi_connection, connection_record
    ):
        cursor = dbapi_connection.cursor()
        try:
            cursor.execute("SET search_path TO integration_test")
        finally:
            cursor.close()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
