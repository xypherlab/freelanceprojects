import pymysql
connection = pymysql.connect(
    host='localhost',
    user='x',
    password='mapuatech',
    db='exam',
)
try:
    with connection.cursor() as cursor:
        sql = "UPDATE todos SET `title`=%s, `desc`=%s WHERE `id` = %s"
        try:
            cursor.execute(sql, ('your new title', 'your new description', 1))
            print("Successfully Updated...")
        except:
            print("Oops! Something wrong")
 
    connection.commit()
finally:
    connection.close()