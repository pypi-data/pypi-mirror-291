# third party import
import os

# custom import
from sqlalchemy_snowpark.orm_manager.snowpark_session import SnowparkSession
from sqlalchemy_snowpark.orm_manager.sqlalchemy_session import SQLAlchemySession
from sqlalchemy_snowpark.datawarehouse_connector.snowflake_session import (
    SnowflakeSession,
)
from sqlalchemy_snowpark.datawarehouse_connector.postgresql_session import (
    PostgreSqlSession,
)
from sqlalchemy_snowpark.datawarehouse_connector.redshift_session import RedshiftSession
from sqlalchemy_snowpark.logger import logger
from sqlalchemy_snowpark.constants import *

from sqlalchemy_snowpark.constants import (
    DB_ENGINE_KEY,
    POSTGRESQL,
    SNOWPARK_KEY,
    DB_SOURCE,
    SNOWFLAKE,
    REDSHIFT,
)
from sqlalchemy_snowpark.helper import detail_error


def create_session(connection_string):
    try:
        db_source = os.getenv(DB_SOURCE)
        session = None
        if db_source == SNOWFLAKE or "snowflake" in connection_string:
            snowflake_session_obj = SnowflakeSession()
            session = snowflake_session_obj.get_db_session(connection_string)

        elif (
            db_source == REDSHIFT or "redshift+redshift_connector" in connection_string
        ):
            redshift_session_obj = RedshiftSession()
            session = redshift_session_obj.get_db_session(connection_string)

        elif db_source == POSTGRESQL or "postgresql" in connection_string:
            postgresql_session_obj = PostgreSqlSession()
            session = postgresql_session_obj.get_db_session(connection_string)

        # by default connection will be to snowflake data warehouse
        else:
            logger.error(
                RED
                + " DataSource "
                + {db_source}
                + " not supported at the moment... "
                + ENDC
            )
            return None
        return session
    except Exception as e:
        detail_error(e)
        return None


def get_db_session(connection_string=None):
    try:
        db_engine = os.environ.get(DB_ENGINE_KEY)
        session = create_session(connection_string)
        db_session = (
            SnowparkSession(session)
            if db_engine == SNOWPARK_KEY
            else SQLAlchemySession(session)
        )
        return db_session
    except Exception as e:
        detail_error(e)
        return None
