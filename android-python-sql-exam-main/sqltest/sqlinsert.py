import pymysql
connection = pymysql.connect(
    host='localhost',
    user='xypher',
    password='1234',
    db='exam',
)
qenter = input("Enter Question: ")
c1 = input("c1: ")
c2 = input("c2: ")
c3 = input("c3: ")
c4 = input("c4: ")
answer = input("answer: ")

try:
    with connection.cursor() as cursor:
        sql = "INSERT INTO questionbank (`question`, `choice1`, `choice2`, `choice3`, `choice4`, `answer`) VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            cursor.execute(sql, (qenter, c1, c2,c3,c4,answer))
            print("Task added successfully")
        except:
            print("Oops! Something wrong")
 
    connection.commit()
finally:
    connection.close()
