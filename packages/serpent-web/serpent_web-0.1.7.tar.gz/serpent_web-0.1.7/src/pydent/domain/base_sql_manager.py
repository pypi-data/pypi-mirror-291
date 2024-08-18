from abc import ABC
from typing import TypeVar

from pydent.data.sql.base_sql_model import BaseSqlModel
from pydent.domain.base_manager import BaseManager

TModel = TypeVar('TModel', bound=BaseSqlModel)


class BaseSqlManager(BaseManager[TModel], ABC):
    pass
