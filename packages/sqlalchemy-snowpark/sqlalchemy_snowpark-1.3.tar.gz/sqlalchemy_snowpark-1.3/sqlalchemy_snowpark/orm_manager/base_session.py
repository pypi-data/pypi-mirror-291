from abc import ABC, abstractmethod
from datetime import datetime
import sqlparse


class SFNBaseResultSet(ABC):
    def __init__(self, obj):
        self.obj = obj

    @abstractmethod
    def fetchone(self, get_obj=False):
        pass

    @abstractmethod
    def fetchmany(self, count, get_obj=False):
        pass

    @abstractmethod
    def fetchall(self, get_obj=False):
        pass

    @abstractmethod
    def mappings_one(self):
        pass

    @abstractmethod
    def mappings_all(self):
        pass


class SFNBaseDatabaseSession(ABC):

    def __init__(self, session):
        self.session = session

    @abstractmethod
    def get_session(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def execute(self, query) -> SFNBaseResultSet:
        """Executes a SQL query using the SQLAlchemy session and returns a SQLAlchemyResultSet.

        Parameters:
        query (str): The SQL query to be executed.

        Returns:
        SFNBaseResultSet: An object that wraps the result of the SQL query execution.
        """
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @abstractmethod
    def add(self):
        """Inserts a new record into the given table."""
        pass

    def _format_query(self, query, reindent=True):
        return sqlparse.format(query, reindent=reindent)

    def _print(self, *args, **kwargs):
        kwargs.setdefault("flush", True)
        print(*args, **kwargs)

    def _get_where_clause(self, filter, filter_by):
        where_clause = ""
        if filter and filter_by:
            raise Exception(
                "Both filter and filter_by cannot be defined together. Define either of them."
            )

        if filter:
            where_clause_conditions = []

            for key, value in filter.items():
                if isinstance(value, list) or isinstance(value, dict):
                    raise Exception("unsupported filter format, review and update it")

                # handle None values coming up in where clause as client_column_name = 'None' or client_column_name != 'None'
                if "'None'" in value:
                    value = value.replace(" ", "")
                    if "='None'" in value:
                        value = value.replace("='None'", " is NULL")
                    if "!='None'" in value:
                        value = value.replace("!='None'", " is NOT NULL")

                where_clause_conditions.append(f"{key}{value}")

            where_clause = " AND ".join(where_clause_conditions)

        elif filter_by:
            keys = list(filter_by.keys())
            if len(keys) != 1:
                raise Exception("only one filter is allowed")
            key = keys[0]
            operator = key.upper()

            if isinstance(filter_by[key], dict):
                where_clause = f" {operator} ".join(
                    f"{k}{v}" for k, v in filter_by[key].items()
                )
            elif isinstance(filter_by[key], list):
                global_operator = operator
                conditions_list = filter_by[key]
                if len(conditions_list) == 0 or (not conditions_list[0]):
                    raise Exception(
                        "conditions cannot be empty, provide valid statements"
                    )
                conditions = conditions_list[0]
                print("conditions: {}".format(conditions))
                if isinstance(conditions, dict):
                    if len(conditions) <= 1:
                        raise Exception(
                            "internal operator conditions must be more than one, please review"
                        )

                    clauses = []
                    for internal_operator in conditions:
                        internal_clause = list()
                        for k, v in conditions[internal_operator].items():
                            if isinstance(v, list):
                                filter_list_value = list()
                                for val in v:
                                    filter_list_value.append(f" {k} {val} ")
                                filter_list_value = " AND ".join(filter_list_value)
                                internal_clause.append(filter_list_value)
                            else:
                                internal_clause.append(f" {k} {v} ")
                            # internal_clause = f" {internal_operator.upper()} ".join(
                            #     f"{k} {v}" for k, v in conditions[internal_operator].items() if isinstance(v, str)
                            # )
                        internal_clause = f" {internal_operator.upper()} ".join(
                            internal_clause
                        )
                        internal_clause = "( " + internal_clause + " )"
                        clauses.append(internal_clause)
                        print("clauses : ", clauses)

                    where_clause = f" {global_operator} ".join(clauses)

            else:
                raise Exception("unsupported filter_by format, review and update it")
        print("where_clause :", where_clause)
        return where_clause

    def query(
        self,
        model_class,
        # schema: str,
        # table: str,
        filter: dict = dict(),
        filter_by: dict = dict(),
        order_by: list = [],
        fields: list = [],
        limit: int = None,
    ) -> SFNBaseResultSet:
        """
        Executes a SQL query on the Snowflake database using the provided parameters.

        Parameters:
        - schema (str): The name of the database schema.
        - table (str): The name of the table to query.
        - filter (dict): A dictionary containing a single filter condition.
            - Ex: {"column_1": "='value1'"}
            - Note: Both filter and filter_by cannot be defined together.
        - filter_by (dict): A dictionary containing the filter conditions. The dictionary should have only one key-value pair.
            The key should be the logical operator and the value should be one of following;
            - i) when only one logical operator is defined, value should be a dictionary
                - Ex:
                    {
                        "and": {
                            "column_1": "='value1'",
                            "column_1": "!='value1'",
                            "column_1": " in ('value', 'value')",
                        }
                    }

            - ii) when multiple operators are defined, value should be a list of a single dictionary, where each key denotes another logical operator.
                - Ex:
                    {
                        "and": [
                            {
                                "and": {
                                    "column_1": "='value1'",
                                    "column_1": "!='value1'",
                                    "column_1": " in ('value', 'value')",
                                },
                                "or": {
                                    "column_1": "='value1'",
                                    "column_1": "!='value1'",
                                    "column_1": " in ('value', 'value')",
                                },
                            }
                        ]
                    }
        - fields (list, optional): A list of column names to select. If not provided, all columns will be selected.
        - limit (int, optional): The maximum number of rows to return. If not provided, all rows will be returned.

        Returns:
        - SFNBaseResultSet: An object that represents the result set of the query.
        """
        table = model_class.__tablename__
        schema = model_class.__table_args__["schema"]

        if not table and not schema:
            raise Exception(
                "either table name or schema is not provided. please review the model_class."
            )

        limit_clause = ""
        fields_clause = ""
        order_by_clause = ""
        where_clause = self._get_where_clause(filter, filter_by)

        if limit:
            limit_clause = f" LIMIT {limit}"

        if fields:
            fields_clause = ", ".join(fields)
        else:
            fields_clause = "*"

        if order_by:
            order_by_clause += ", ".join(f"{col} {order}" for col, order in order_by)

        query = f"SELECT {fields_clause} FROM {schema}.{table} "

        if where_clause:
            query += " WHERE " + where_clause

        if order_by_clause:
            query += " ORDER BY " + order_by_clause

        if limit_clause:
            query += " " + limit_clause

        self._print("\nquery: \n")
        self._print(self._format_query(query))
        self._print("\n")
        return self.execute(query)

    def _is_numeric(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def update(self, model_class, data: dict, filter=None, filter_by=None):
        """Updates records in the database table based on the provided filter conditions."""
        try:
            if not data:
                raise Exception("data cannot be empty")

            table = model_class.__tablename__
            schema = model_class.__table_args__["schema"]

            where_clause = self._get_where_clause(filter, filter_by)

            def format_set_values(data):
                set_values_list = []
                for k, v in data.items():
                    if isinstance(v, datetime):
                        set_values_list.append(f"{k} = '{str(v)}'")
                    elif self._is_numeric(str(v)) or isinstance(v, bool):
                        set_values_list.append(f"{k} = {v}")
                    elif v is None:
                        set_values_list.append(f"{k} = NULL")

                    else:
                        set_values_list.append(f"""{k} = '{v.replace("'", "''")}'""")

                set_values = ", ".join(set_values_list)
                return set_values

            # set_values = ', '.join([f"{k} = {v}" if str(v).isnumeric() else (f"""{k} = '{v.replace("'", "''")}'""" if v is not None else f'{k} = NULL') for k, v in data.items()])
            set_values = format_set_values(data)
            print("set values :", set_values)
            update_query = f"""
                UPDATE {schema}.{table}
                SET {set_values}
                WHERE {where_clause}
                """
            self._print("\n")
            # self._print("update query: \n")
            self._print(self._format_query(update_query))
            self._print("\n")
            self.execute(update_query)
        except Exception as e:
            print(str(e))

    def delete(self, model_class, filter=None, filter_by=None):
        """Deletes records from the database table based on the provided filter conditions."""
        if not filter and not filter_by:
            print("warning: no filters provided, this might erase complete data.")
        table = model_class.__tablename__
        schema = model_class.__table_args__["schema"]
        where_clause = self._get_where_clause(filter, filter_by)
        delete_query = f"DELETE FROM {schema}.{table}"
        if where_clause:
            delete_query += " WHERE " + where_clause
        self._print("\n")
        self._print("delete query: \n")
        self._print(self._format_query(delete_query))
        self._print("\n")
        self.execute(delete_query)

    def _generate_create_table_sql(self, cls):
        columns = []
        for column in cls.__table__.columns:
            column_name = column.name
            column_type = column.type.compile(dialect=None)
            column_constraints = " ".join(str(c) for c in column.constraints)
            column_definition = (
                f"{column_name} {column_type} {column_constraints}".strip()
            )
            columns.append(column_definition)
        columns_sql = ", ".join(columns)
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {cls.__table_args__['schema']}.{cls.__tablename__} ({columns_sql})"
        return create_table_sql

    @abstractmethod
    def create_table(self, cls, checkfirst=True):
        pass
