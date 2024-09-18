import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_get_user_success():
    """
    Тест успешного получения данных о пользователе.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/user/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Leanne Graham",
        "email": "Sincere@april.biz"
    }

@pytest.mark.asyncio
async def test_get_user_not_found():
    """
    Тест на случай, если пользователь не найден.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/user/9999")
    assert response.status_code == 404
