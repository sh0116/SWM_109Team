# -*- coding: utf-8 -*

import pymysql

# RDS MYSQL information
host = "db109.cpehjs7hbg19.ap-northeast-2.rds.amazonaws.com"
port = 3306
userName = "admin"
userPasswd = "admin109"
database = "robot1"

# connect RDS
def connectRDS(host, port, userName, userPasswd, database):
    try:
        connection = pymysql.connect(host, user=userName, passwd=userPasswd, db=database, port=port, use_unicode=True, charset='utf8')
        cursor = connection.cursor()
    except:
        logging.error("connection fail")
        sys.exit(1)
    return connection, cursor

# INSERT
# insert into prot_info table
def insert_prot_info(name, contact):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    query = "insert into prot_info (name, contact) values ("+name+","+contact+");"
    cursor.execute(query)
    connection.commit()

# insert into user_info table
def insert_user_info(name, gender, birth, address, contact, prot_id):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    query = "insert into user_info (name, gender, birth, address, contact, prot_id) values ("+name+","+gender+","+birth+","+address+","+contact+","+str(prot_id)+");"
    cursor.execute(query)
    #print(query)
    connection.commit()

# insert into robot_info table
def insert_robot_info(robot_name, robot_id, user_id):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    query = "insert into robot_info (robot_name, robot_id, user_id) values ("+robot_name+","+str(robot_id)+","+str(user_id)+");"
    print(query)
    cursor.execute(query)
    connection.commit()

# insert into sensor data table
def insert_data(data_name, *args):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    query = ""
   #print(args)
    if(len(args) == 1):
        query = "insert into "+data_name+" (user_id) values ("+str(args[0])+");"
    elif(len(args) == 2):
        query = "insert into "+data_name+" (num, user_id) values ("+str(args[0])+","+str(args[1])+");"
    cursor.execute(query)
    connection.commit()

# SELECT
# select from table
def select(table, num=0, *args):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    query = "select "
    #print(args)
    for arg in args:
        query += str(arg)
        if(arg != args[len(args)-1]): query += ","
    query += " from "+str(table)+";"
    #print(query)
    cursor.execute(query)
    connection.commit()
    result = []
    if (num == 0): # all
        rows = cursor.fetchall()
        if(rows is None): return result # empty set
        for row in rows:
            result0 = []
            for row0 in row:
                result0.append(row0)
            result.append(result0)
    else: # one
        rows = cursor.fetchone()
        if(rows is None): return result # empty set
        for row in rows:
            result.append(str(row))
        return result
    return result

# select from table with where condition
def select_where(table, num=0, *args, **kwargs):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    query = "select "
    for arg in args:
        query += str(arg)
        if(arg != args[len(args)-1]): query += ","
    query += " from "+str(table)+" where "
    for key, value in kwargs.items():
        query += str(key)+"="+str(value)
    query += ";"
    #print(query)
    cursor.execute(query)
    connection.commit()
    result = []
    if (num == 0): # all
        rows = cursor.fetchall()
        #print(rows)
        if(rows is None): return result # empty set
        for row in rows:
            result0 = []
            for row0 in row:
                result0.append(str(row0))
            result.append(result0)
    else: # one
        rows = cursor.fetchone()
        #print(rows)
        if(rows is None): return result # empty set
        for row in rows:
            result.append(str(row))
    return result
