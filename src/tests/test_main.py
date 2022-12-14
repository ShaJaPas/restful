import pytest
from fastapi import status
from httpx import Response
from starlette.testclient import TestClient


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
