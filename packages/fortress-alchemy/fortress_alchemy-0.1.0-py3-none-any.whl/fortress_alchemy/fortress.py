from typing import Any
from fortress_sdk_python import Fortress
from sqlalchemy import Engine
from sqlalchemy import create_engine
from urllib.parse import quote_plus


class FortressAlchemy:
    def __init__(self, org_id: str, api_key: str):
        """
        Initialize the FortressAlchemy instance.

        :param org_id: Your organization ID.
        :param api_key: Your API key
        """
        self.__fortress = Fortress(org_id, api_key)._Fortress__fortress
        self.__database_cache = {}
        self.__tenant_to_database = {}

    def create_engine(self, tenant_id: str, **kwargs: Any) -> Engine:
        """
        Create a SQLAlchemy engine for the given tenant.

        :param tenant_id: The tenant ID.
        :param kwargs: Additional keyword arguments to pass to create_engine.
        :return: A SQLAlchemy engine.
        """
        if tenant_id in self.__database_cache:
            return self.__database_cache[tenant_id]
        database_connection = self.__fortress.get_uri(tenant_id, "tenant")
        uri = f"postgresql://{quote_plus(database_connection.username)}:{quote_plus(database_connection.password)}@{database_connection.url}:{database_connection.port}/{database_connection.database}"

        engine = create_engine(uri, **kwargs)
        self.__database_cache[tenant_id] = engine
        self.__tenant_to_database[tenant_id] = database_connection.database_id
        return engine
