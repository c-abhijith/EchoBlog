from fastapi import FastAPI
from blog.database import init_db
from blog.routers import auth

app = FastAPI()

# Initialize database
init_db()

# Include routers
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Blog API"} 