# SQLAlchemy Toolkit

This project is a library that simplifies the use of SQLAlchemy in Python applications. It also provides a implementation of the repository pattern for SQLAlchemy.

It has a FastAPI integration through a middleware that manages the session and transaction for each request.

![PyPI](https://img.shields.io/pypi/v/sqlalchemy-toolkit.svg)
![Supported Python versions](https://img.shields.io/pypi/pyversions/sqlalchemy-toolkit.svg)

## Features

Here's what sqlalchemy-repository can do for you. 🚀

- **DatabaseManager**: It provides a class that manages the session and transaction for each request.
- **Repository pattern**: It provides a implementation of the repository pattern for SQLAlchemy.
- **FastAPI integration**: It provides a middleware that manages the session and transaction for each request in FastAPI.
- **Async support**: It provides a async version of the DatabaseManager, the Repository pattern and the FastAPI middleware.

## Installation

```console
$ pip install sqlalchemy-toolkit
---> 100%
Successfully installed sqlalchemy-toolkit
```

## Usage

Here's a quick example. ✨

### A SQL Table

Imagine you have a SQL table called `hero` with:

- `id`
- `name`
- `secret_name`
- `age`

### Create a SQLAlchemy model

```python
from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_toolkit import Entity


class Hero(Entity):
    __tablename__ = "heroes"

    id: Mapped[Optional[int]] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(255))
    secret_name: Mapped[str] = mapped_column(String(255))
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=None)
```

The class `Hero` is a **SQLAlchemy** model. It is a subclass of `Entity` from **sqlalchemy-repository**, which is a subclass of `SQLAlchemy`'s `DeclarativeBase` class.

And each of those class attributes is a **SQLAlchemy** column.

### Create a SQLAlchemy session

```python
from sqlalchemy_toolkit import DatabaseManager

db = DatabaseManager("sqlite:///heroes.db")
```

The `DatabaseManager` class is a class that manages the session through the `session_ctx` method.

### Create a repository

```python
from sqlalchemy_toolkit import SQLAlchemyRepository

class HeroRepository(SQLAlchemyRepository[Hero, int]):
    entity_class = Hero

hero_repository = HeroRepository()
```

### Use the repository

```python
with db.session_ctx():
    hero = Hero(name="Deadpond", secret_name="Dive Wilson")

    hero_repository.save(hero)

    heroes = hero_repository.find_all()
```

## FastAPI integration

Here's a quick example using the previous hero model. ✨

### Without using the repository

```python
from typing import Any, List, Optional

from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy_toolkit import DatabaseManager
from sqlalchemy_toolkit.ext.fastapi import SQLAlchemyMiddleware

from .models import Hero


class HeroDto(BaseModel):
    id: Optional[int]
    name: str
    secret_name: str
    age: int


app = FastAPI()

db = DatabaseManager("sqlite:///heroes.db")

app.add_middleware(SQLAlchemyMiddleware, db=db)


@app.get("/heroes", response_model=List[HeroDto])
def find_all_heroes() -> Any:
    stm = select(Hero)
    return db.session.scalars(stm).all()
```

### Using the repository

```python
from typing import Any, List, Optional

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy_toolkit import DatabaseManager
from sqlalchemy_toolkit.ext.fastapi import SQLAlchemyMiddleware
from typing_extensions import Annotated

from .repository.hero_repository import HeroRepository


class HeroDto(BaseModel):
    id: Optional[int]
    name: str
    secret_name: str
    age: int


app = FastAPI()

db = DatabaseManager("sqlite:///heroes.db")

app.add_middleware(SQLAlchemyMiddleware, db=db)


@app.get("/heroes", response_model=List[HeroDto])
def find_all_heroes(hero_repository: Annotated[HeroRepository, Depends()]) -> Any:
    return hero_repository.find_all()
```

## License

This project is licensed under the terms of the [MIT license](https://github.com/javalce/sqlalchemy-toolkit/blob/master/LICENSE).
