from fastapi import FastAPI
from routes import router as main_router
from database.database import init_db

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    init_db()
    print("✅ Database initialized")

# Include all routers
app.include_router(main_router)
