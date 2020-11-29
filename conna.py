import psycopg2 as psql

conn=psql.connect(
    host='localhost',
    database='test',
    user='postgres',
    password='%%%%%',
)

cur=conn.cursor()
cur.execute('''INSERT INTO person(name,country) VALUES ('joker','DC')''')
cur.execute('SELECT * FROM person')

cur.close()
conn.commit()
conn.close()