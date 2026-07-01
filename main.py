from fastapi import FastAPI
from database import engine
import model

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")

def home():
  return{
    "Message": "Blog api "
  }