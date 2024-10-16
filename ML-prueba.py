import sqlite3
import pandas as pd

db = sqlite3.connect("Proyecto-Escuela")

query = """
    SELECT * FROM Registros
"""



print(pd.read_sql_query(query, db))