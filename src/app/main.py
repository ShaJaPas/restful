from fastapi import Depends, FastAPI, Query, status, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import DbPerson, Person

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
) -> JSONResponse | float:
    """
    Сумма элементов арифметической прогрессии
    """

    if b <= a:
        return JSONResponse(
            content={"message": "Последний элемент в прогрессии должен быть больше первого"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return (a + b) * n / 2


@app.get("/arithmetic/geom-sum/")
def geometric_sum(
    a: int = Query(description="Первый элемент в прогрессии"),
    n: int = Query(description="Количество элементов в прогрессии", gt=1),
    step: int = Query(description="Шаг прогрессии"),
) -> float:
    """
    Сумма элементов геометрической прогрессии
    """
    return a * (step**n - 1) / (step - 1)


@app.get("/user-agent/")
def get_user_agent(user_agent: str = Header(include_in_schema=False)) -> dict[str, str]:
    return {"User-Agent": user_agent}


@app.get("/people", response_model=list[DbPerson])
async def get_person(session: AsyncSession = Depends(get_session)) -> list[DbPerson]:
    """
    Список людей в базе данных
    """
    result = await session.execute(select(DbPerson))
    people: list[DbPerson] = result.scalars().all()
    return [
        DbPerson(
            name=person.name,
            sirname=person.sirname,
            birthday=person.birthday,
            id=person.id,
        )
        for person in people
    ]


@app.post("/people", response_model=DbPerson, status_code=status.HTTP_201_ACCEPTED)
async def add_person(person: Person, session: AsyncSession = Depends(get_session)) -> DbPerson:
    """
    Добавить объект человека в БД
    """
    person = DbPerson(name=person.name, sirname=person.sirname, birthday=person.birthday)
    session.add(person)
    await session.commit()
    await session.refresh(person)
    return person
