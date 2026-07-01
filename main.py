from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#db dependency
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

#home
@app.get("/")
def home():
  return{
    "Message": "Blog api "
  }

# Create Blog
@app.post("/blogs", response_model=schemas.BlogResponse)
def create_blog(blog:schemas.BlogCreate, db:Session = Depends(get_db)):
  new_blog = models.Blog(
    title = blog.title,
    content = blog.content
  )
  db.add(new_blog)
  db.commit()
  db.refresh(new_blog)

  return new_blog


# Fetch Blogs
@app.get("/blogs",response_model=list[schemas.BlogResponse])
def get_blogs(db: Session = Depends(get_db)):
  return db.query(models.Blog).all()


# Fetch by Id
@app.get("/blogs/{id}", response_model=schemas.BlogResponse)
def get_blog(id:int, db: Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id).first()
  if not blog:
    raise HTTPException(status_code=404, detail="Blog not found")
  return blog


# Update blog
@app.put("/blogs/{id}", response_model=schemas.BlogResponse)
def update_blog(id:int, blog: schemas.BlogCreate, db: Session = Depends(get_db)):
  existing_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
  if not existing_blog:
    raise HTTPException(status_code=404, detail="Blog not found")

  existing_blog.title = blog.title
  existing_blog.content = blog.content

  db.commit()
  db.refresh(existing_blog)

  return existing_blog

# Delete Blog
@app.delete("/blogs/{id}")
def delete_blog(id:int, db: Session = Depends(get_db)):
  blog = db.query(models.Blog).filter(models.Blog.id == id).first()
  if not blog:
     raise HTTPException(status_code=404, detail="Blog not found")

  db.delete(blog)
  db.commit()

  return {"Message": "Blog deleted"}

