import pymysql

 

# Create a connection object

dbServerName    = "127.0.0.1"

dbUser          = "x"

dbPassword      = "mapuatech"

dbName          = "exam"

charSet         = "utf8mb4"

cusrorType      = pymysql.cursors.DictCursor

 

connectionObject   = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword,

                                     db=dbName, charset=charSet,cursorclass=cusrorType)

try:

    cursorObject        = connectionObject.cursor()                                     
    sqlQuery            = "CREATE TABLE Employee(id int, LastName varchar(32), FirstName varchar(32), DepartmentCode int)"   
    cursorObject.execute(sqlQuery)

    sqlQuery            = "show tables"   

    cursorObject.execute(sqlQuery)

    rows                = cursorObject.fetchall()

 

    for row in rows:

        print(row)

except Exception as e:

    print("Exeception occured:{}".format(e))

finally:

    connectionObject.close()