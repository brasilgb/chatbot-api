import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

dsn = os.getenv("DBMAKER_DSN")
user = os.getenv("DBMAKER_USER")
password = os.getenv("DBMAKER_PASSWORD", "")

conn_str = f"DSN={dsn};UID={user};PWD={password};"

print(conn_str.replace(password, "***") if password else conn_str)

conn = pyodbc.connect("DSN=GRUPOSOLARDB;")

cursor = conn.cursor()
cursor.execute("""
SELECT 
    "1051datem",
    "1051depto",
    "1051orige",
    "1051numnf",
    "1051total"
FROM a_mnf105
WHERE "1052anoem" = 2026
""")

for row in cursor.fetchmany(5):
    print(row)

cursor.close()
conn.close()