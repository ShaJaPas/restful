from datetime import date

import pytest
from fastapi import status
from httpx import AsyncClient, Response
from starlette.testclient import TestClient

from app.models import Person


@pytest.mark.parametrize(
    ("params", "status_code", "result"),
    [
        ({"a": 0, "b": 10, "n": 1}, status.HTTP_422_UNPROCESSABLE_ENTITY, 0),
        ({"a": 1, "b": -1, "n": 10}, status.HTTP_400_BAD_REQUEST, 0),
        ({"a": 1, "b": 100, "n": 100}, status.HTTP_200_OK, 5050),
    ],
)
def test_arithmetic_sum(
    test_app: TestClient, params: dict[str, int], status_code: int, result: int
) -> None:
    response: Response = test_app.get("/arithmetic/prog-sum/", params=params)
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        assert response.json() == result


@pytest.mark.parametrize(
    ("params", "status_code", "result"),
    [
        ({"a": 1, "step": 5, "n": 5}, status.HTTP_200_OK, 781),
        ({"a": 2, "step": 0, "n": 500}, status.HTTP_200_OK, 2),
    ],
)
def test_geometric_sum(
    test_app: TestClient, params: dict[str, int], status_code: int, result: int
) -> None:
    response: Response = test_app.get("/arithmetic/geom-sum/", params=params)
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        assert response.json() == result


@pytest.mark.asyncio()
async def test_get_person(test_app_async: AsyncClient) -> None:
    person = Person(name="Ivan", sirname="Ivanov", birthday=date(2022, 1, 1)).json()
    response: Response = await test_app_async.post("/people", content=person)
    assert response.status_code == status.HTTP_201_CREATED

    response = await test_app_async.get("/people")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "name": "Ivan",
            "sirname": "Ivanov",
            "birthday": str(date(2022, 1, 1)),
            "id": 1,
        }
    ]
