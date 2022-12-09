from fastapi import status
from httpx import Response


def test_arithmetic_sum(test_app):
    response: Response = test_app.get(
        "/arithmetic/prog-sum/", params={"a": 0, "b": 10, "n": 1}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response: Response = test_app.get(
        "/arithmetic/prog-sum/", params={"a": 1, "b": -1, "n": 10}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response: Response = test_app.get(
        "/arithmetic/prog-sum/", params={"a": 1, "b": 100, "n": 100}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == 5050


def test_geometric_sum(test_app):
    response: Response = test_app.get(
        "/arithmetic/geom-sum/", params={"a": 1, "step": 5, "n": 5}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == 781

    response: Response = test_app.get(
        "/arithmetic/geom-sum/", params={"a": 2, "step": 0, "n": 500}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == 2
