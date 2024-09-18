from fastapi import FastAPI, HTTPException
import aiohttp

app = FastAPI()

# URL внешнего API для получения данных о пользователе
EXTERNAL_API_URL = "https://jsonplaceholder.typicode.com/users"


async def fetch_user_from_external_api(user_id: int):
    """
    Асинхронная функция для получения данных о пользователе из внешнего API.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{EXTERNAL_API_URL}/{user_id}") as response:
            if response.status == 200:
                return await response.json()
            else:
                raise HTTPException(status_code=response.status, detail="Ошибка получения данных о пользователе")

@app.get("/user/{user_id}")
async def get_user(user_id: int):
    """
    Эндпоинт для получения информации о пользователе по ID.
    """
    try:
        user_data = await fetch_user_from_external_api(user_id)
        return {
            "id": user_data.get("id"),
            "name": user_data.get("name"),
            "email": user_data.get("email"),
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
