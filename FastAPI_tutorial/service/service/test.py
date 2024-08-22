import sys

print(sys.executable)

connection_url = URL.create(
    "mssql+pyodbc",
    username="",
    password="",
    host="localhost",
    port=1433,
    database="priority",
    query={
        "driver": "ODBC Driver 17 for SQL Server",
        "authentication": "ActiveDirectoryIntegrated",
    },
)