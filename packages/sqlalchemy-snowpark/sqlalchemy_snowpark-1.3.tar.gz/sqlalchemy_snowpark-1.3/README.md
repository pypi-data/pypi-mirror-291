# SQLAlchemy-Snowpark Session Management Module

This pip module simplifies the management of database sessions using SQLAlchemy and Snowpark. It allows users to create a session with Snowflake, PostgreSQL, and other supported databases using a connection string or environment variables.


# Overview

This `README.md` file provides comprehensive instructions for installing, setting up, and using the `Sqlalchemy-Snowpark` module, ensuring users can easily establish connections to their data warehouses and use inbuilt methods to query the datawarehouse and manage results.

---

## Installation

You can install the module using pip:

```bash
pip install sqlalchemy-snowpark
```

# Sqlalchemy - Snowpark

## Snowflake
This Python module helps establish a database session to Snowflake using SQLAlchemy or using Snowpark python connector. It supports creating connections via a provided connection string or by using environment variables for credentials.

Requires `DB_SOURCE`, `USERNAME`, `HOST`, `PASSWORD`, `ROLE`, `WAREHOUSE`, and `DATABASE`.

If you want to create a session using SQLAlchemy then set the following environment variables
```bash
export DB_ENGINE=sqlalchemy
```

and if you want to create a Snowpark session the set the following environment variables
```bash
export DB_ENGINE=snowpark
```

### 1. Create DB Session Using a Connection String
If you have a connection string, you can create a session like this:

```python
from sqlalchemy_snowpark.connection import get_db_session

connection_string = "snowflake://user:password@account/database/schema?warehouse=warehouse&role=role"
session = get_db_session(snowflake_creds)
session.close()
```

### 2. Create DB Session Using environment variables
Environment Variables
The following environment variables are required if no connection string is provided:

Note : In case of snowpark session ( DB_ENGINE=snowpark ), only this option will work.

```bash
export SNOWFLAKE_USER={snowflake_username}
export SNOWFLAKE_PASSWORD={snowflake_password}
export SNOWFLAKE_ACCOUNT={snowflake_account}
export SNOWFLAKE_DATABASE={snowflake_database}
export SNOWFLAKE_SCHEMA={snowflake_schema}
export SNOWFLAKE_WAREHOUSE={snowflake_warehouse}
export SNOWFLAKE_ROLE={snowflake_role}
export SNOWFLAKE_HOST={snowflake_host}
```

```python
from sqlalchemy_snowpark.connection import get_db_session

session = get_db_session()
```

### Whitelisting
If network policy is activated in the snowflake account and incoming ips are not allowed or restricted then need to whitelist our StepFunction IP : 

Please follow the below steps for the same :
1. Navigate to the Admin->Security section by clicking on "Admin" in the left navigation panel
2. Switch to Network Rules. Create a new rule by clicking on + Network Rule button
   a. Name: SFN_RULE
   b. Choose Type: IPv4 and Mode: Ingress
   c. Under Identifiers -> Add IP 18.210.244.167
3. Switch to Network Policy. Create a new policy by clicking on + Network Policy button
   a. Name: SFN_POLICY
   b. Under Allowed Section & Under Select Rule Dropdown select SFN_RULE then click on Create button to create the policy.
   c. Click on the dotted icon(...) at the end of the policy name and click Activate to start the policy. 
4.   Navigate back to the worksheet and replace placeholder <IP> with the StepFunctions public IP address.
	
     ALTER NETWORK POLICY SFN_POLICY SET ALLOWED_IP_LIST=('18.210.244.167')

## Redshift

Requires `USERNAME`, `HOST`, `PASSWORD`, and `DATABASE`.

### 1. Create DB Session Using a Connection String

```python
### Direct Connection (Redshift in Public Subnet)
from sqlalchemy_snowpark.connector import get_db_session
from sqlalchemy.engine.url import URL

# Define the connection parameters
redshift_connection_string = URL.create(
    drivername="redshift+redshift_connector",  # The driver to use
    username="your_username",  # Your Redshift username
    password="your_password",  # Your Redshift password
    host="your_redshift_cluster_host",  # Redshift cluster endpoint
    port=5439,  # Default port for Redshift
    database="your_database_name",  # The name of your Redshift database
    query={"sslmode": "verify-ca"}  # Optional: to ensure the connection is encrypted
)

session = get_db_session(redshift_connection_string)
session.close()
```
### 2. Create DB Session Using Environment Variables
Environment Variables
The following environment variables are required if no connection string is provided:

```bash
export REDSHIFT_USERNAME={redshift_username}
export REDSHIFT_PASSWORD={redshift_password}
export REDSHIFT_HOST={redshift_host}
export REDSHIFT_DATABASE={redshift_database}
```


```python
from sqlalchemy_snowpark.connection import get_db_session

session = get_db_session()
```


## PostgreSQL

Requires `USERNAME`, `HOST`, `PASSWORD`, and `DATABASE`.

### 1. Create DB Session Using a Connection String

```python
from sqlalchemy_snowpark.connection import get_db_session

postgresql_connection_string = f"postgresql+psycopg2://{username}:{password}@{host}:5432/{database}"
session = get_session(postgresql_connection_string)
session.close()
```

### 2. Create DB Session Using Environment Variables
Environment Variables
The following environment variables are required if no connection string is provided:

```bash
export POSTGRESQL_USERNAME={postgresql_username}
export POSTGRESQL_PASSWORD={postgresql_password}
export POSTGRESQL_HOST={postgresql_host}
export POSTGRESQL_DATABASE={postgresql_database}
```
```python
from sqlalchemy_snowpark.connection import get_db_session

session = get_db_session()
```

---

# Handling Connection

Once the session is established, you can interact with your data warehouse using most of the SQLAlchemy's ORM capabilities.

---

# ORM Capabilities 

## Methods Overview
1. fetchone(get_obj=False) 
This method is used to fetch one record. If get_obj=True, it will return response in dictionary_format otherwise plain result will be returned.

Usage 
```python
result = db_session.execute(query).fetchone() 
# OR
result db_session.execute(query).fetchone(get_obj=True)
```

2. fetchmany(count, get_obj=False) 
This method is used to fetch multiple records at a time . If get_obj=True, it will return response in dictionary_format otherwise plain result will be returned.

Usage 
```python
result = db_session.execute(query).fetchmany(count=10, get_obj=False) 
# OR
result db_session.execute(query).fetchone(count=10, get_obj=True)
```

3. fetchall(get_obj=False) 
This method is used to fetch all records at a time . If get_obj=True, it will return response in dictionary_format otherwise plain result will be returned.

Usage 
```python
result = db_session.execute(query).fetchall() 
# OR
result db_session.execute(query).fetchall(get_obj=True)
```

4. mappings_one()
This method is used to fetch one record in dictionary format.

Usage 
```python
result = db_session.execute(query).mappings_one() 
``` 

5. mappings_all()
This method is used to fetch all records in dictionary format.

Usage 
```python
result = db_session.execute(query).mappings_all() 
``` 

6. close()
This method is used to close the db session.
Usage 
```python
db_session.close()
``` 

7. execute(query)
This method is used to execute db  query.

Usage 
```python
db_session.execute({query}).fetchone()
``` 

8.commit()
Commits the transaction

Usage 
```python
db_session.commit()
```

9. rollback()
Rolls back the transaction.

Usage 
```python
db_session.rollback()
```

10. add(model_class, data)
Adds a new record to the database.

Note: Model class represents the sqlachemy model class
Usage 
```python
db_session.add(model_class={model_class}, data={data_in_dict_format})
```

11. create_table(cls, checkfirst=True)
Creates a table based on the model class.

Usage 
```python
db_session.create_table(cls=model_class, checkfirst=True)
```

12. query(model_class, filter: dict = dict(), filter_by: dict = dict(), order_by: list = [], fields: list = [], limit: int = None)
This method is used to run query using a model class just like we do in sqlachemy 
`
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
`

Usage 
```python
filter = {
    "filter_1": f"='{filter_1_value}'",
    "filter_2": f"='{filter_2_value}'",
    "filter_3": f"!='{filter_3_value}'",
    "filter_4": f"in ({filter_4_value}, {filter_5_value})",
}
result = db_session.query(
    model_class=ModelClassName,
    fields=["field_name"],
    filter=filter,
    limit=10,
    offset=10

).fetchone()
```

13. update(model_class, data: dict, filter=None, filter_by=None)
This method is used to update the data in table using model class
"""Updates records in the database table based on the provided filter conditions."""

Usage
```python
update_filter = {
    "filter_1": f"='{filter_1_value}'",
    "filter_2": f"='{filter_2_value}'",
}
update_record = dict()
update_record["column_1"] = "value_1"
self.db_session.update(
    model_class=ModelClassName,
    data=update_record,
    filter=update_filter,
)
```

14. delete(model_class, filter=None, filter_by=None)
"""Deletes records from the database table based on the provided filter conditions."""

Usage
```python
db_session.delete(
    model_class=ModelClassName,
    filter={"column_1": f"='{value_1}'"},
)
```

---


# Troubleshooting

## Common Issues

- Invalid Credentials: Ensure that the USERNAME and PASSWORD are correct.
- Host Unreachable: Verify the HOST address and network connectivity.
- Unsupported Data Source: Check if the DB_SOURCE is among the supported ones (snowflake, redshift, postgresql).

## Error Handling

The `get_db_session` method prints exceptions to help identify issues during the connection process. Ensure that the provided connection details are accurate and the data warehouse is accessible.

---

# Conclusion

This module simplifies the process of connecting to various data warehouses. Follow the setup instructions carefully, and refer to the examples for guidance on using the `get_session` function. For further assistance, check the documentation or raise an issue on the project's GitHub repository.
```