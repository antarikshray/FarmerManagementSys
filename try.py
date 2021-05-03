import sqlite3;

con = sqlite3.connect('FarmerDB.db')
cur = con.cursor()

#cur.execute("INSERT INTO FarmerDetails VALUES (7,'Shefali Ray','1998-02-03',7746463546)")
cur.execute('insert into FarmerDetails values(?, ?, ?, ?)',(7,'Alagrit Ram', '1997-02-03', 7746463541))


con.commit()
con.close()