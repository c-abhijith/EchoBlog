from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from blog.database import engine
from blog.models import Base
from blog.routers import auth,home

app = FastAPI(title="Blog API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(auth.router,tags=["Auth"])
app.include_router(home.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Blog API",
        "version": "1.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }