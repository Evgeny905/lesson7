from fastapi import FastAPI, Path
app = FastAPI()
users = {'1': 'Имя: Example, возраст: 18'}
@app.get("/users")
async def users_dict() -> dict:
    return users
@app.post("/user/{username}/{age}")
async def create_users(username: str, age: int) -> str:
    current_index = int(max(users, key=int)) + 1
    users[current_index] = f'Имя: {username}, возраст: {age}'
    return f'User {current_index} is registered'
@app.put("/user/{user_id}/{username}/{age}")
async def update_users(user_id: int, username: str, age: int) -> str:
    users[user_id] = f'Имя: {username}, возраст: {age}'
    return f'The user {user_id} is updated'
@app.delete("/user/{user_id}")
async def delete_users(user_id: int) -> str:
    users.pop(user_id)
    return f'The user {user_id} is delete'