from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from typing import Annotated, List
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
app = FastAPI()
templates = Jinja2Templates(directory='templates')
users = []
class User(BaseModel):
    id: int = None
    username: str
    age: int
@app.get("/")
async def Get_Main_Page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request':request, 'users':users})
@app.get("/user/{user_id}")
async def Get_Users(request: Request, user_id: int) -> HTMLResponse:
    Error = True
    for get_user in users:
        if get_user.id == user_id:
            Error = False
            return templates.TemplateResponse('users.html', {'request': request, 'user': get_user})
        else:
            continue
    if Error:
        raise HTTPException(status_code=404, detail='User was not found')
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