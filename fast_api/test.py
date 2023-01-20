from fastapi import FastAPI,Request,HTTPException,Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URl = "sqlite:///.Users.db"
engine = create_engine(DB_URl, connect_args={"check_same_thread":False})
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()    

class Voters(BaseModel):
    # id:Optional[int]=None
    username:str
    password:str

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def show_users(db:Session=Depends(get_db)):
    return db.query(User).all()

@app.post("/api/login/")
def login(username: str, password: str, db: Session = Depends(get_db)):
    # Query the database for a user with the provided username and password
    user = db.query(User).filter(User.username == username, User.password == password).first()
    if user:
        return {"message": "Success"}
    else:
        return {"message": "Invalid username or password"}
