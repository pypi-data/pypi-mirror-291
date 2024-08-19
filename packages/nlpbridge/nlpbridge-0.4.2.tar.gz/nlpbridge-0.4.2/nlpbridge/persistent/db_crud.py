import os
import sys
from typing import Dict, TypeVar, Generic, Union

sys.path.append(os.getcwd())

from nlpbridge.persistent.mysql_dataschema import Template, Router, Node, Edge, Chat
from sqlmodel import select
from sqlmodel import SQLModel
from nlpbridge.persistent.db import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType", bound=SQLModel)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: type[ModelType]) -> None:
        self.model = model

    async def get_by_id(self, id: int, session: AsyncSession = None) -> Union[ModelType, None]:
        async with get_db_session() if session is None else session as db_session:
            response = await db_session.execute(select(self.model).where(self.model.id == id))
            return response.scalar_one_or_none()

    async def get_by_ids(self, list_ids: list[int], session: AsyncSession = None) -> Union[list[ModelType], None]:
        async with get_db_session() if session is None else session as db_session:
            response = await db_session.execute(select(self.model).where(self.model.id.in_(list_ids)))
            return response.scalars().all()

    async def create(self, obj_in: Union[ModelType, Dict], session: AsyncSession = None) -> ModelType:
        db_obj = self.model.model_validate(obj_in)
        async with get_db_session() if session is None else session as db_session:
            db_session.add(db_obj)
            await db_session.commit()
            await db_session.refresh(db_obj)
            return db_obj


class CRUDTemplate(CRUDBase):
    def __init__(self) -> None:
        super().__init__(model=Template)


class CRUDRouter(CRUDBase):
    def __init__(self) -> None:
        super().__init__(model=Router)


class CRUDNode(CRUDBase):
    def __init__(self) -> None:
        super().__init__(model=Node)


class CRUDEdge(CRUDBase):
    def __init__(self) -> None:
        super().__init__(model=Edge)


class CRUDChat(CRUDBase):
    def __init__(self) -> None:
        super().__init__(model=Chat)
