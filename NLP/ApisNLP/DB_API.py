import pymysql
import sys

def DB_AUTH():
    # RDS MYSQL information
    host = ""
    port = 3306
    userName = ""
    userPasswd = ""
    database = ""

    try:
        connection = pymysql.connect(host, user=userName, passwd=userPasswd, db=database, port=port, use_unicode=True, charset='utf8')
        cursor = connection.cursor()
    except: 
        logging.error("connection fail")
        sys.exit(1)

    return connection, cursor

def select_home_temp():
    connection, cursor = DB_AUTH()
    query = "select * from temperature;"
    cursor.execute(query)
    connection.commit()
    rows = cursor.fetchall()
    
    return rows

if __name__ == "__main__":
    pass

print(select_home_temp())
