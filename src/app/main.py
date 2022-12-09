from fastapi import FastAPI, Query, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


class BasicResponse(BaseModel):
    message: str


@app.get(
    "/arithmetic/prog-sum/",
    responses={status.HTTP_400_BAD_REQUEST: {"model": BasicResponse}},
)
def arithmetic_sum(
    a: int = Query(description="Первый элемент в прогрессии"),
    b: int = Query(description="Последний элемент в прогрессии"),
    n: int = Query(description="Количество элементов в прогрессии", gt=1),
):
    """
    Сумма элементов арифметической прогрессии
    """
    if b <= a:
        return JSONResponse(
            content={
                "message": "Последний элемент в прогрессии должен быть больше первого"
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return (a + b) * n / 2


@app.get("/arithmetic/geom-sum/")
def geometric_sum(
    a: int = Query(description="Первый элемент в прогрессии"),
    n: int = Query(description="Количество элементов в прогрессии", gt=1),
    step: int = Query(description="Шаг прогрессии"),
):
    """
    Сумма элементов геометрической прогрессии
    """
    return a * (step**n - 1) / (step - 1)
