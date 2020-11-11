import pymysql
import sys
import boto3
import os
"""    
# RDS MYSQL information
host = "db109.cpehjs7hbg19.ap-northeast-2.rds.amazonaws.com"
port = 3306
userName = "admin"
userPasswd = "admin109"
database = "robot1"
region="ap-northeast-2
"""
def main():
    ENDPOINT="db109.cpehjs7hbg19.ap-northeast-2.rds.amazonaws.com"
    PORT="3306"
    USR="admin"
    REGION="ap-northeast-2"
    DBNAME="mysql"
    os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

    #gets the credentials from .aws/credentials
    session = boto3.Session(profile_name='default')
    client = boto3.client('rds')

    token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USR, Region=REGION)
    try:
        connection = pymysql.connect(host=ENDPOINT, user=USR, passwd=token, db=DBNAME, port=PORT, use_unicode=True, charset='utf8')
        cur = connection.cursor()
        cur.execute("""SELECT now()""")
        query_results = cur.fetchall()
        print(query_results)
    except Exception as e:
        print("Database connection failed due to {}".format(e))  



def select_home_temp():
    connection, cursor = DB_AUTH()
    query = "select * from temperature;"
    cursor.execute(query)
    connection.commit()
    rows = cursor.fetchall()
    
    return rows

if __name__ == "__main__":
    main()


