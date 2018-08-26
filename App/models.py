import psycopg2

conn = psycopg2.connect("dbname='stack' user = 'postgres' password = 'fifi' host = 'localhost' port = '5432'")
cur = conn.cursor()

def create_tables():
	conn = psycopg2.connect("dbname='stack' user='postgres' password='fifi' host='localhost' port = '5432'")
	with conn.cursor() as cur:
		cur.execute("CREATE TABLE IF NOT EXISTS users (userid serial PRIMARY KEY,name VARCHAR(150) NOT NULL,username VARCHAR(150) NOT NULL,password VARCHAR(100) NOT NULL, email VARCHAR(150) NOT NULL, time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)")
		cur.execute("CREATE TABLE IF NOT EXISTS questions (questid serial PRIMARY KEY,question VARCHAR(350) NOT NULL,username VARCHAR(150) NOT NULL, time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)")
		cur.execute("CREATE TABLE IF NOT EXISTS answers (answerid serial PRIMARY KEY,questid INTEGER NOT NULL,username VARCHAR(150) NOT NULL,answer TEXT NOT NULL, time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)")
	conn.commit()
