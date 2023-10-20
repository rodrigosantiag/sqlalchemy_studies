from fastapi import FastAPI, status
from sqlalchemy import create_engine, text, insert
from sqlalchemy.orm import Session
from pydantic import BaseModel
import os

from entities import User

app = FastAPI()
engine = create_engine(os.getenv("DATABASE_URL"), echo=True)


class TestModel(BaseModel):
    name: str

class UserAccountModel(BaseModel):
    name: str
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


@app.put("/{id}")
async def put_data(id: int, item: TestModel):
    sql = text("UPDATE test_table SET name = :name WHERE id = :id")

    with Session(engine) as session:
        session.execute(sql, {"name": item.name, "id": id})
        session.commit()

    return {"message": f"Register #{id} successfully updated!"}


@app.post("/user_account", status_code=status.HTTP_201_CREATED)
async def add_user_account(user_account: UserAccountModel):
    statement = insert(User).values(name=user_account.name, fullname=user_account.fullname)

    with engine.connect() as conn:
        result = conn.execute(statement)
        conn.commit()

    return {"message": f"User account #{result.inserted_primary_key[0]} created!"}
