from fastapi import FastAPI, Path, HTTPException
from typing import Annotated, List
from pydantic import BaseModel
app = FastAPI()
users = []
class User(BaseModel):
    id: int = None
    username: str
    age: int
@app.get("/users")
async def users_list() -> List[User]:
    return users
@app.post("/user/{username}/{age}")
async def create_users(current_User: User, username: Annotated[str, Path(min_length=2, max_length=20, description='Enter username', example='UrbanUser')],
                       age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]) -> User:
    current_User.id = len(users) + 1
    current_User.username = username
    current_User.age = age
    users.append(current_User)
    return current_User
@app.put("/user/{user_id}/{username}/{age}")
async def update_users(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='35')],
                       username: Annotated[str, Path(min_length=2, max_length=20, description='Enter username', example='UrbanUser')],
                       age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]) -> User:
    try:
        edit_User = users[user_id - 1]
        edit_User.username = username
        edit_User.age = age
        return edit_User
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')
@app.delete("/user/{user_id}")
async def delete_users(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='35')]) -> User:
    delete_User = users[user_id - 1]
    if delete_User.id == user_id:
        users.pop(user_id - 1)
        return delete_User
    else:
        raise HTTPException(status_code=404, detail='User was not found')