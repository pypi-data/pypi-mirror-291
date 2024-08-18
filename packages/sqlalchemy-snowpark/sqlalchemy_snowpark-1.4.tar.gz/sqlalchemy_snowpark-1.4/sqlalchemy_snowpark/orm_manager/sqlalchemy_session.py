from sqlalchemy_snowpark.orm_manager.base_session import SFNBaseDatabaseSession, SFNBaseResultSet



class SQLAlchemyResultSet(SFNBaseResultSet):
    def __init__(self, obj):
        self.obj = obj

    def fetchone(self, get_obj=False):
        return self.obj.fetchone()

    def fetchmany(self, count, get_obj=False):
        return self.obj.fetchmany(count)

    def fetchall(self, get_obj=False):
        return self.obj.fetchall()

    def mappings_one(self):
        try:
            return self.obj.mappings().one()
        except Exception as e:
            return None

    def mappings_all(self):
        try:
            return self.obj.mappings().all()
        except Exception as e:
            return None



class SQLAlchemySession(SFNBaseDatabaseSession):
    def __init__(self, session):
        self.session = session
        self.bind = self.session.bind

    def get_session(self):
        return self.session

    def close(self):
        self.session.close()

    def execute(self, query) -> SQLAlchemyResultSet:
        obj = self.session.execute(query)
        return SQLAlchemyResultSet(obj)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def add(self, model_class, data):
        instance = model_class(**data)
        self.session.add(instance)

    def create_table(self, cls, checkfirst=True):
        cls.__table__.create(bind=self.session.bind, checkfirst=checkfirst)
        self.commit()