# third party imports
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy import orm as sa_orm

# custom imports
from sqlalchemy_snowpark.constants import *
from sqlalchemy_snowpark.helper import detail_error, logger
from sqlalchemy_snowpark.db_constants import *


class RedshiftSession:
    def __init__(self):
        pass

    def get_db_session(self, jdbc_uri):
        try:
            connect_args = {"sslmode": "disable"}
            if not jdbc_uri:
                host = os.getenv(REDSHIFT_HOST)
                username = os.getenv(REDSHIFT_USERNAME)
                password = os.getenv(REDSHIFT_PASSWORD)
                database = os.getenv(REDSHIFT_DATABASE)

                db_connection_string = URL.create(
                    drivername=REDSHIFT_DRIVER_KEY,
                    host=host,
                    port=5439,
                    database=database,
                    username=username,
                    password=password,
                    query={"sslmode": "verify-ca"},  # Adjust sslmode as needed
                )
                engine = create_engine(db_connection_string, connect_args=connect_args)
                Session = sessionmaker(bind=engine)
                session = Session()
            else:
                engine = create_engine(jdbc_uri, connect_args=connect_args)
                Session = sa_orm.sessionmaker()
                Session.configure(bind=engine)
                session = Session()

            if session:
                result = session.execute("SELECT version()").fetchone()
                logger.info(f"Redshift version: {result[0]}")
                return session
        except Exception as e:
            logger.error(f"Error getting Redshift session: {str(e)}")
            detail_error(e)
            return None
