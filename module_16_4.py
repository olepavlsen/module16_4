from fastapi import FastAPI, status, Body, HTTPException
from typing import Annotated

from pydantic import BaseModel

app = FastAPI()

users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get("/user")
def get_users() -> list:
    return users


@app.post("/user/{username}/{age}")
def create_user(user: User):
    if len(users) == 0:
        user.id = 1
    else:
        user.id = users[-1].id + 1
    users.append(user)
    return user


@app.put("/user/{user_id}/{username}/{age}")
def update_user(user_id: int, user: User):
    try:
        user.id = user_id
        user_upd = users[user.id - 1]
        user_upd.username = user.username
        user_upd.age = user.age
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")
    return user


@app.delete("/user/{user_id}")
def delete_user(user_id: int):
    for i, u in enumerate(users):
        if u.id == user_id:
            user = users[i]
            del users[i]
            return user
    raise HTTPException(status_code=404, detail="User was not found")

# uvicorn module_16_4:app
