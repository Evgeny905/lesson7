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
    if len(users) == 0:
        current_User.id = 1
        current_User.username = username
        current_User.age = age
        users.append(current_User)
        return current_User
    else:
        current_User.id = users[-1].id + 1
        current_User.username = username
        current_User.age = age
        users.append(current_User)
        return current_User
@app.put("/user/{user_id}/{username}/{age}")
async def update_users(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='35')],
                       username: Annotated[str, Path(min_length=2, max_length=20, description='Enter username', example='UrbanUser')],
                       age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]) -> User:
    Error = True
    for edit_user in users:
        if edit_user.id == user_id:
            Error = False
            edit_user.username = username
            edit_user.age = age
            return edit_user
        else:
            continue
    if Error:
        raise HTTPException(status_code=404, detail='User was not found')
@app.delete("/user/{user_id}")
async def delete_users(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='35')]) -> User:
    Error = True
    i = -1
    for delete_User in users:
        i += 1
        if delete_User.id == user_id:
            Error = False
            users.pop(i)
            return delete_User
        else:
            continue
    if Error:
        raise HTTPException(status_code=404, detail='User was not found')