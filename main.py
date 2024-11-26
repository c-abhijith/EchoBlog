from fastapi import FastAPI
from blog.database import engine
from blog.models import Base

app = FastAPI()

Base.metadata.create_all(engine)
