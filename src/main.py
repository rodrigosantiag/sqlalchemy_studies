from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, text, insert, select, update, delete
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os

import logging
from entities import User, Address

app = FastAPI()
engine = create_engine(os.getenv("DATABASE_URL"), echo=True)

logger = logging.getLogger(__name__)

class TestModel(BaseModel):
    name: str


class UserAccountModel(BaseModel):
    name: str
    fullname: str

class UserAccountFullnameModel(BaseModel):
    fullname: str


@app.get("/")
async def get_data():
    result = []

    with engine.connect() as conn:
        rows = conn.execute(text("SELECT id, name FROM test_table"))

        for id, name in rows:
            result.append({
                "id": id,
                "name": name
            })

    return result


@app.post("/", status_code=status.HTTP_201_CREATED)
async def add_data(model: TestModel):
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO test_table (name) VALUES (:name)"),
            {"name": model.name}
        )

        # conn.execute(
        #     text("INSERT INTO not_public.test_table_2 (name) VALUES (:name)"),
        #     {"name": model.name}
        # )

    return {"message": f"{model.name} inserted"}


@app.put("/{id_}")
async def put_data(id_: int, item: TestModel):
    sql = text("UPDATE test_table SET name = :name WHERE id = :id_")

    with Session(engine) as session:
        session.execute(sql, {"name": item.name, "id": id_})
        session.commit()

    return {"message": f"Register #{id_} successfully updated!"}


@app.post("/user_account", status_code=status.HTTP_201_CREATED)
async def add_user_account(user_account: UserAccountModel):
    statement = insert(User).values(name=user_account.name, fullname=user_account.fullname)

    with engine.connect() as conn:
        result = conn.execute(statement)
        conn.commit()

    return {"message": f"User account #{result.inserted_primary_key[0]} created!"}


@app.get("/user_account")
async def get_user_account(name: str):
    sql = select(User.id, User.name, User.fullname, User.addresses).where(User.name == name)

    with Session(engine) as session:
        user = session.execute(sql).first()

    if not user:
        return {}

    with Session(engine) as session:
        user_addresses = session.execute(select(Address.email_address).where(Address.user_id == user.id))

    addresses = []

    for address in user_addresses:
        addresses.append(address.email_address)

    return {
        "name": user.name,
        "fullname": user.fullname,
        "addresses": addresses
    }


@app.patch("/user_account/{id_}")
async def update_user_account(id_: int, user_account: UserAccountFullnameModel):
    get_user_sql = select(User).where(User.id == id_)

    with Session(engine) as session:
        user = session.execute(get_user_sql).first()

    if not user:
        return JSONResponse(status_code=400, content={"message": "Invalid data"})

    update_sql = update(User).where(User.id == id_).values(fullname=user_account.fullname)

    with Session(engine) as session:
        session.execute(update_sql)
        session.commit()

    return {"message": "User updated"}

@app.delete("/user_account/{id_}")
async def delete_user_account(id_: int):
    delete_sql = delete(User).where(User.id == id_)

    with Session(engine) as session:
        session.execute(delete_sql)
        session.commit()

    return {"message": "User deleted"}
