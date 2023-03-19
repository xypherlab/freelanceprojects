import pymysql
connection = pymysql.connect(
    host='localhost',
    user='xypher',
    password='1234',
    db='exam',
)
try:
    with connection.cursor() as cursor:
        #sql = "SELECT `id`, `title`, `desc` FROM todos WHERE `date` = CURDATE()"
        sql = "SELECT `name`, `email`, `date` FROM todos"
        #try:
        if True:
            cursor.execute(sql)
            result = cursor.fetchall()
            print(str(result))
            print("Id\t\t Title\t\t\t\t\tDescription")
            print("---------------------------------------------------------------------------")
            print(len(result))
            for row in result:
                print(str(row[0]) + "\t\t" + row[1] + "\t\t\t" + row[2])
 
        #except:
            #print("Oops! Something wrong")
 
    connection.commit()
finally:
    connection.close()
