from typing import Any

# custom imports
from sqlalchemy_snowpark.orm_manager.base_session import (
    SFNBaseDatabaseSession,
    SFNBaseResultSet,
)
from snowflake.snowpark import Row


class DotNotationRow:
    def __init__(self, row):
        # Convert row to a dictionary for easy attribute access
        self.row_dict = row.as_dict()

    def __getattr__(self, name):
        # Convert attribute name to lowercase to match dictionary keys
        if name.upper() in self.row_dict:
            return self.row_dict[name.upper()]
        raise AttributeError(f"'DotNotationRow' object has no attribute '{name}'")

    def __getitem__(self, index):
        # Allow indexing to access values like in a list or tuple
        return list(self.row_dict.values())[index]

    def __repr__(self):
        # Provide a string representation of the object for debugging
        return f"DotNotationRow({self.row_dict})"

    def __str__(self):
        # Provide a structured representation of the row values
        items = (f"{key}: {value!r}" for key, value in self.row_dict.items())
        return f"{{ {', '.join(items)} }}"


class SnowparkResultSet(SFNBaseResultSet):
    def __init__(self, obj, session=None):
        # super().__init__(obj)
        self.obj = obj

    def _process_results(self, results, get_obj=False):
        # Wrap each Row object in a DotNotationRow object
        if get_obj:
            if isinstance(results, Row):
                return DotNotationRow(results)
            return [DotNotationRow(row) for row in results]
        return results

    def fetchone(self, get_obj=False):
        result = self.obj.collect()
        if result:
            result = result[0]
            return self._process_results(result, get_obj=get_obj)
        return None

    def fetchmany(self, count, get_obj=False):
        result = self.obj.collect()
        if result:
            result = result[:count]
            return self._process_results(result, get_obj=get_obj)
        return None

    def fetchall(self, get_obj=False):
        result = self.obj.collect()
        if result:
            return self._process_results(result, get_obj=get_obj)
        return []

    def mappings_one(self):
        df = self.obj.collect()
        if not df:
            return None
        return {
            column_name.lower(): column_value
            for column_name, column_value in df[0].as_dict().items()
        }

    def mappings_all(self):
        rows = [row.as_dict() for row in self.obj.collect()]
        updated_rows = []

        for row in rows:
            updated_row = {
                column_name.lower(): column_value
                for column_name, column_value in row.items()
            }
            updated_rows.append(updated_row)

        return updated_rows


class SnowparkSession(SFNBaseDatabaseSession):
    def __init__(self, session):
        self.session = session
        self.bind = self.session.connection
        # self.begin_transaction()

    def get_session(self):
        return self.session

    def close(self):
        self.session.close()

    def execute(self, query) -> SnowparkResultSet:
        if not query.strip().lower().startswith("select"):
            obj = self.session.sql(query).collect()
        else:
            obj = self.session.sql(query)
        # print("obj:", obj)
        # print("obj type:", type(obj))
        # print("obj cols:", obj.columns)
        return SnowparkResultSet(obj, self.session)

    def begin_transaction(self):
        self.session.sql("BEGIN").collect()

    def commit(self):
        self.session.sql("COMMIT").collect()

    def rollback(self):
        self.session.sql("ROLLBACK").collect()

    def add(self, model_class, data):
        table = model_class.__tablename__
        schema = model_class.__table_args__["schema"]
        columns = data.keys()
        values = data.values()

        def get_tuple_value(values):
            list_value = []
            for value in values:
                if isinstance(value, str):
                    value.replace("'", "''")
                # elif value is None:
                #     value = "NULL"
                list_value.append(value)
            return tuple(list_value)

        values = get_tuple_value(values=values)
        insert_query = f"""
        INSERT INTO {schema}.{table} ({', '.join(columns)})
        VALUES ({', '.join('?' * len(values))})
        """
        # print("insert_query:")
        # print(self._format_query(insert_query, reindent=True))
        # # df = self.session.sql(insert_query, values)
        # print(df.queries)
        self.session.sql(insert_query, values).collect()

    def create_table(self, cls, checkfirst=True):
        create_table_sql = self._generate_create_table_sql(cls)
        self._print("\ncreate query:")
        self._print(create_table_sql)
        self._print("\n")
        self.execute(create_table_sql)
        self.commit()
