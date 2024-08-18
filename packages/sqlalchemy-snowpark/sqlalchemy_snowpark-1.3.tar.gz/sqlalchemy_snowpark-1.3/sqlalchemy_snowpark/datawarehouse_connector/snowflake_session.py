# third party imports
import os
from snowflake.snowpark import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
# custom imports
from sqlalchemy_snowpark.constants import *
from sqlalchemy_snowpark.helper import detail_error, logger
from sqlalchemy_snowpark.db_constants import *

class SnowflakeSession:
    def __init__(self):
        self.account = os.getenv(SNOWFLAKE_ACCOUNT)
        self.database = os.getenv(SNOWFLAKE_DATABASE)
        self.schema = os.getenv(SNOWFLAKE_SCHEMA)
        self.warehouse = os.getenv(SNOWFLAKE_WAREHOUSE)
        self.role = os.getenv(SNOWFLAKE_ROLE)
        self.token = self.get_login_token() if os.getenv(DB_ENGINE_KEY) == SNOWPARK_KEY else None
        self.authenticator = OAUTH_AUTHENTICATION
        self.host = os.getenv(SNOWFLAKE_HOST)
        self.user = os.getenv(SNOWFLAKE_USER)
        self.password = os.getenv(SNOWFLAKE_PASSWORD)

    def get_login_token(self):
        try:
            with open("/snowflake/session/token", "r") as f:
                return f.read()
        except Exception as e:
            print("token not found in this path : /snowflake/session/token")
            return None
    
    def get_connection_params(self):
        connection_parameters = {
            "account": self.account,
            "database": self.database,
            "schema": self.schema,
            "warehouse": self.warehouse,
            "role": self.role,
        }
        db_password = self.password
        if db_password:
            connection_parameters["password"] = db_password
            connection_parameters["user"] = self.user
        else:
            connection_parameters["token"] = self.get_login_token()
            connection_parameters["authenticator"] = self.authenticator
            connection_parameters["host"] = self.host

        return connection_parameters
    
    def get_snowpark_session(self):
        connection_parameters = self.get_connection_params()
        session = Session.builder.configs(connection_parameters).create()
        return session
    
    def get_sqlalchemy_session(self, connection_string=None):
        try:
            if not connection_string:
                connection_string = (
                    f"snowflake://{self.user}:{self.password}@{self.host}/{self.database}"
                    f"?warehouse={self.warehouse}&role={self.role}"
                )
            engine = create_engine(connection_string)
            Session = sessionmaker(bind=engine)
            session = Session()
            # if session:
            #     result = session.execute("SELECT CURRENT_VERSION()").fetchone()
            #     logger.info(f"Snowflake version: {result[0]}")
            #     return session
            return session
        except Exception as e:
            logger.error(f"Error getting SQLAlchemy session: {str(e)}")
            detail_error(e)
            return None

    def get_db_session(self, connection_string=None):
        try:
            db_engine = os.environ.get(DB_ENGINE_KEY)
            print("DB_ENGINE: ", db_engine)
            if db_engine == SNOWPARK_KEY:
                return self.get_snowpark_session()
            else:
                return self.get_sqlalchemy_session(connection_string)
        except Exception as e:
            logger.error(f"Error getting DB session: {str(e)}")
            detail_error(e)
            return None