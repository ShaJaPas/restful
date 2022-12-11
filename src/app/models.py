from datetime import date

from sqlmodel import SQLModel, Field


class Person(SQLModel):
    """
    Модель, описывающая человека
    """

    name: str = Field(description="Имя человека")
    sirname: str = Field(description="Фамилия человека")
    birthday: date = Field(description="Дата рождения человека")


class DbPerson(Person, table=True):
    id: int = Field(default=None, primary_key=True)
