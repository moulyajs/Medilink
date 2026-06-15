from database import SessionLocal
from sqlalchemy import text

try:
    db = SessionLocal()

    result = db.execute(text("SELECT current_user"))
    print(result.fetchone())

    print("CONNECTED SUCCESSFULLY")

except Exception as e:
    print("ERROR:")
    print(e)