from fastapi import FastAPI, Request
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Field, Session, SQLModel, create_engine
from datetime import datetime, timedelta

SQLITE_URL = f"sqlite:///database.db"
ips_in_use = []


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
def save_ip(ip: str, session: SessionDep) -> None:
    client = Client(ip=ip)
    session.add(client)
    session.commit()
    session.refresh()

def verify_ip(new_ip: str) -> bool:
    existing_ip = None
    for ip in ips_in_use:
        if new_ip == ip['value']:
            existing_ip = True

    if not existing_ip:
        ips_in_use.append({
            'value': new_ip,
            'counter': 1,
            'time': datetime.now()
        })
        return True

    for ip in ips_in_use:
        if new_ip == ip['value']:
            temp = ip['time'] + timedelta(minutes=1)
            if ip['counter'] == 5 and temp > datetime.now():
                return False
            else:
                ip['counter'] += 1
                return True


# ======= server =======
app  = FastAPI()

@app.get("/")
async def root(request: Request, session: SessionDep, status_code=status.HTTP_200_OK):
    ip  = request.client.host
    result = verify_ip(new_ip=ip)
    if not result:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Rate limit exceeded!")
    print('\n\n', ips_in_use, '\n\n')
    #save_ip(ip=ip, session=session)
    return {"message": f'Your IP is {ip}'}