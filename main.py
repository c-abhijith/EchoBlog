from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from blog.database import engine
from blog.models import Base
from blog.routers import auth,user,comment,like

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


@app.get("/")
async def root():
    return {
        "message": "Welcome to Blog API",
        "version": "1.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }
    
    
    
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(comment.router)
app.include_router(like.router)