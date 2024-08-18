# third party imports
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# custom imports
from sqlalchemy_snowpark.constants import *
from sqlalchemy_snowpark.helper import detail_error, logger
from sqlalchemy_snowpark.db_constants import *


class PostgreSqlSession:
    def __init__(self):
        pass

    def get_db_session(self, connection_string=None):
        try:
            if not connection_string:
                username = self.data.get(POSTGRESQL_USERNAME)
                host = self.data.get(POSTGRESQL_HOST)
                password = self.data.get(POSTGRESQL_PASSWORD)
                database = self.data.get(POSTGRESQL_DATABASE)
                connection_string = f"postgresql+{PSYCOPG2_KEY}://{username}:{password}@{host}:5432/{database}"
            engine = create_engine(connection_string)
            Session = sessionmaker(bind=engine)
            session = Session()
            if session:
                result = session.execute("SELECT version()").fetchone()
                logger.info(f"PostgreSQL version: {result[0]}")
                return session
            return session
        except Exception as e:
            logger.error(f"Error getting PostgreSQL session: {str(e)}")
            detail_error(e)
            return None
