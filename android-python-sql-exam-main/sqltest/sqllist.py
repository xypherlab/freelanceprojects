import pymysql

conn = pymysql.connect(
    host='localhost',
    user='xypher',
    password='1234',
    db='exam',
)
cur = conn.cursor()
examname="exam3"
sqlQuery            = "CREATE TABLE "+examname+"(id int, question text, choice1 text, choice2 text, choice3 text, choice4 text, answer text)"
cur.execute(sqlQuery)  



cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'exam'")


for table in [tables[0] for tables in cur.fetchall()]:
    print(table)
	