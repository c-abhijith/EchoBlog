from fastapi import FastAPI
from blog.database import Base,engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get('/')
def index():
    return {"message":"ok"}