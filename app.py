from fastapi import FastAPI, Request
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

SQLITE_URL = f"sqlite:///database.db"


# ======= models =======
class Client(SQLModel, table=True):
    __tablename__ = 'ip'

    id: int | None = Field(default=None, primary_key=True)
    ip: str = Field(index=True)


# ======= db settings =======
engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


# ======= functions =======
def save_ip(ip: str, session: SessionDep):
    client = Client(ip=ip)
    session.add(client)
    session.commit()
    session.refresh()

def verify_ip(ip: str):
    pass


# ======= server =======
app  = FastAPI()

@app.get("/")
async def root(request: Request, session: SessionDep):
    ip  = request.client.host
    verify_ip(ip=ip)
    save_ip(ip=ip, session=session)
    return {"message": f'Your IP is {ip}'}