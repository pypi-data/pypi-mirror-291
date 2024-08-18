# setup.py
from setuptools import setup, find_packages

setup(
    name="sqlalchemy_snowpark",
    version="1.4",
    packages=find_packages(),
    install_requires=[
        "psycopg2-binary",
        "redshift-connector",
        "snowflake-connector-python",
        "snowflake-sqlalchemy",
        "SQLAlchemy",
        "sqlalchemy-redshift",
        "urllib3",
        "snowflake-snowpark-python",
        "sqlparse",
    ],
    author="Chandani Kumari",
    author_email="chandani@stepfunction.ai",
    description="A package for database session management using sqlalchemy and snowpark libraries",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://ChandaniStepFunction@bitbucket.org/ChandaniStepFunction/sqlalchemy-snowpark.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
