import os
import sys
from typing import Dict, TypeVar, Generic, Union, Optional, Any

sys.path.append(os.getcwd())

from nlpbridge.persistent.mysql_dataschema import Template, Router, Node, Edge, Chat, Customer, Tag, Group, Level
from sqlmodel import select, func, desc
from sqlmodel import SQLModel
from nlpbridge.persistent.db import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType", bound=SQLModel)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: type[ModelType]) -> None:
        self.model = model

    async def _get_session(self, db_session: Optional[AsyncSession] = None) -> AsyncSession:
        return get_db_session() if db_session is None else db_session

    async def get_by_id(self, id: int, db_session: AsyncSession = None) -> Union[ModelType, None]:
        async with get_db_session() if db_session is None else db_session as session:
            response = await session.execute(select(self.model).where(self.model.id == id))
            return response.scalar_one_or_none()

    async def get_by_ids(self, list_ids: list[int], db_session: AsyncSession = None) -> Union[list[ModelType], None]:
        async with get_db_session() if db_session is None else db_session as session:
            response = await session.execute(select(self.model).where(self.model.id.in_(list_ids)))
            return response.scalars().all()

    async def get_count(self, db_session: AsyncSession = None) -> Union[int, None]:
        async with get_db_session() if db_session is None else db_session as session:
            response = await session.execute(select(func.count()).select_from(select(self.model).subquery()))
            return response.scalar_one_or_none()

    async def get_multi(self, skip: int = 0, limit: int = 100, db_session: AsyncSession = None) -> list[ModelType]:
        async with get_db_session() if db_session is None else db_session as session:
            query = select(self.model).offset(skip).limit(limit).order_by(self.model.id)
            response = await session.execute(query)
            return response.scalars().all()

    async def create(self, obj_in: Union[ModelType, Dict], db_session: AsyncSession = None) -> ModelType:
        db_obj = self.model.model_validate(obj_in)
        async with get_db_session() if db_session is None else db_session as session:
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

    async def update(self, obj_current: ModelType, obj_new: Union[ModelType, Dict[str, Any]],
                     db_session: AsyncSession = None) -> ModelType:
        async with get_db_session() if db_session is None else db_session as session:
            if isinstance(obj_new, dict):
                update_data = obj_new
            else:
                update_data = obj_new.model_dump(exclude_unset=True)
            for field in update_data:
                setattr(obj_current, field, update_data[field])

            session.add(obj_current)
            await session.commit()
            await session.refresh(obj_current)
            return obj_current

    async def delete(self, id: int, db_session: AsyncSession = None) -> ModelType:
        async with get_db_session() if db_session is None else db_session as session:
            response = await session.execute(select(self.model).where(self.model.id == id))
            obj = response.scalar_one()
            await session.delete(obj)
            await session.commit()
            return obj

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

    async def get_user_chats(self, user_id: int, db_session: AsyncSession = None, page: int = 0,
                             page_size: int = 10):
        async with get_db_session() if db_session is None else db_session as session:
            chats = await session.execute(
                select(Chat).where(Chat.uid == user_id).order_by(desc(Chat.ctime)).offset(page * page_size).limit(
                    page_size))
            return chats.scalars().all()

    async def get_user_chats_count(self, user_id: int, db_session: AsyncSession = None):
        async with get_db_session() if db_session is None else db_session as session:
            response = await session.execute(
                select(func.count()).select_from(Chat).where(Chat.uid == user_id))
            return response.scalar_one_or_none()

    async def get_router_user_chats(self, router_id: int, user_id: int, db_session: AsyncSession = None):
        async with get_db_session() if db_session is None else db_session as session:
            chats = await session.execute(
                select(Chat).where((Chat.router_id == router_id) & (Chat.uid == user_id)).order_by(desc(Chat.ctime)))
            return chats.scalars().all()


class CRUDCustomer(CRUDBase):
    def __init__(self) -> None:
        super().__init__(model=Customer)

    async def get_customer_by_router_id(self, router_ids: list[int], db_session: AsyncSession = None):
        async with get_db_session() if db_session is None else db_session as session:
            customers = await session.execute(select(Customer).where(Customer.router_id.in_(router_ids)))
            return customers.scalars().all()


class CRUDTag(CRUDBase):
    def __init__(self) -> None:
        super().__init__(model=Tag)


class CRUDGroup(CRUDBase):
    def __init__(self) -> None:
        super().__init__(model=Group)


class CRUDLevel(CRUDBase):
    def __init__(self) -> None:
        super().__init__(model=Level)
