# -*- coding: utf-8 -*

import pymysql

# RDS MYSQL information
host = "db109.cpehjs7hbg19.ap-northeast-2.rds.amazonaws.com"
port = 3306
userName = "admin"
userPasswd = "admin109"
database = "robot2"

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
# insert to user_info table
# insert into sensor data table
def insert_data(data_name, *args):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    query = ""
   #print(args)
    if(len(args) == 2):#fall_down
        query = "insert into "+data_name+" (user_id, sensor_id) values ("+str(args[0])+","+str(args[1])+");"
    elif(len(args) == 3):#temp,humi,activity
        query = "insert into sensor_data (user_id,sensor_id,num) values ("+str(args[0])+","+str(args[1])+","+str(args[2])+");"
    elif(len(args) == 4):#wake,sleep
        query = "insert into sensor_data (user_id,sensor_id,num,day) values ("+str(args[0])+","+str(args[1])+","+str(args[2])+","+str(args[3])+");"
    cursor.execute(query)
    connection.commit()

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
    query = "insert into robot_info (robot_name, robot_serial, user_id) values ("+robot_name+","+str(robot_id)+","+str(user_id)+");"
    print(query)
    cursor.execute(query)
    connection.commit()

#-------------------------------------------------------------------#

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
    cnt = 0
    length = len(kwargs)
    for key, value in kwargs.items():
        query += str(key) + "=" + str(value)
        cnt+=1
        if (cnt < length): 
            query += " and "
    query += " order by id desc;"
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

def get_target_data2db(table_name,target_user):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    query = "select * from " + table_name + " where name = \""+ target_user +"\";"
    cursor.execute(query)
    connection.commit()
    rows = cursor.fetchall()
    print(table_name)
    return rows

    
def select_fall_down(**kwargs):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    query = "select id,timestamp from sensor_data where sensor_id=5 and "
    for key, value in kwargs.items():
        query += str(key) + "=" + str(value)
    query += " order by id desc;"
    #"select count(*) as num from fall_down ;"
    cursor.execute(query)
    connection.commit()
    rows = cursor.fetchall()

    return rows

def select_fall_down_count(**kwargs):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    query ="select count(*) as num from sensor_data where sensor_id=5 and "
    for key, value in kwargs.items():
        query += str(key) + "=" + str(value)
    query += ";"
    cursor.execute(query)
    connection.commit()
    rows = cursor.fetchone()

    return rows

def select_wake_up(**kwargs):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    query = "SELECT * FROM ( SELECT id,num,day,timestamp FROM sensor_data where sensor_id=3 and "
    for key, value in kwargs.items():
        query += str(key) + "=" + str(value)
    query += " ORDER BY id DESC LIMIT 7) A ORDER BY id ASC;"
    cursor.execute(query)
    connection.commit()
    rows = cursor.fetchall()
    return rows

def select_sleep(**kwargs):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    query = "SELECT * FROM ( SELECT id,num,day,timestamp FROM sensor_data where sensor_id=4 and "
    for key, value in kwargs.items():
        query += str(key) + "=" + str(value)
    query += " ORDER BY id DESC LIMIT 7) A ORDER BY id ASC;"
    cursor.execute(query)
    connection.commit()
    rows = cursor.fetchall()
    return rows



def ffff_data(data_name, *args):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    query = "update ffff set fall = " +str(args[1])+ " where id = 1"
    cursor.execute(query)
    connection.commit()