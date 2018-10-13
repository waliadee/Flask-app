import sqlite3
conn = sqlite3.connect('dbAPI.db')
c = conn.cursor()
c.execute('''CREATE TABLE storeAPIData (CompanyName,DateTime,OpenValue, MaxValue, MinValue,CloseValue)''')
conn.commit()
conn.close()
