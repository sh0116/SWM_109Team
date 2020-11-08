# -*- coding:utf-8 -*-

import pymysql
import logging
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

#app.config['JSON_AS_ASCII']=False
# RDS MYSQL information
host = "db109.cpehjs7hbg19.ap-northeast-2.rds.amazonaws.com"
port = 3306
userName = "admin"
userPasswd = "admin109"
database = "robot2"

# connect RDS
def connectRDS(host, port, userName, userPasswd, database):
    try:
        connection = pymysql.connect(host, user=userName, passwd=userPasswd, db=database, port=port, use_unicode=True, charset='utf8mb4')
    #connection.query("set character_set_connection=utf8;")
    #connection.query("set character_set_server=utf8;")
    #connection.query("set character_set_client=utf8;")
    #connection.query("set character_set_results=utf8;")
    #connection.query("set character_set_database=utf8;")
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
        query = "insert into sensor_data (user_id,sensor_id,num,day) values ("+str(args[0])+","+str(args[1])+","+str(args[2])+",'"+str(args[3])+"');"
    #print(query)
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
    query = "insert into user_info (name, gender, birth, address, contact, prot_id) values ("+name+","+gender+","+birth+","+address+","+contact+","+prot_id+");"
    cursor.execute(query)
    #print(query)
    connection.commit()

# insert into robot_info table
def insert_robot_info(robot_name, robot_id, user_id):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    query = "insert into robot_info (robot_name, robot_serial, user_id) values ("+robot_name+","+str(robot_id)+","+str(user_id)+");"
    #print(query)
    cursor.execute(query)
    connection.commit()

def insert_medicine_data(medicine_name, user_id, *args):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    query = "";
    if(len(args) == 10): query = "insert into medicine_data (name, user_id, 월,화,수,목,금,토,일, time1,time2,time3) values ("+medicine_name+","+str(user_id)+","+str(args[0])+","+str(args[1])+","+str(args[2])+","+str(args[3])+","+str(args[4])+","+str(args[5])+","+str(args[6])+","+str(args[7])+","+str(args[8])+","+str(args[9])+");"
    elif(len(args) == 9): query = "insert into medicine_data (name, user_id, 월,화,수,목,금,토,일, time1,time2) values ("+medicine_name+","+str(user_id)+","+str(args[0])+","+str(args[1])+","+str(args[2])+","+str(args[3])+","+str(args[4])+","+str(args[5])+","+str(args[6])+","+str(args[7])+","+str(args[8])+");"
    elif(len(args) == 8): query = "insert into medicine_data (name, user_id, 월,화,수,목,금,토,일, time1) values ("+medicine_name+","+str(user_id)+","+str(args[0])+","+str(args[1])+","+str(args[2])+","+str(args[3])+","+str(args[4])+","+str(args[5])+","+str(args[6])+","+str(args[7])+");"
    #print(query)
    #connection.query("set character_set_connection=utf8;")
    #connection.query("set character_set_server=utf8;")
    #connection.query("set character_set_client=utf8;")
    #connection.query("set character_set_results=utf8;")
    #connection.query("set character_set_database=utf8;")
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
        #print(rows)
        if(rows is None): return result # empty set
        for row in rows:
            result0 = []
            for row0 in row:
                result0.append(str(row0))
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
        query += str(key) + "='" + str(value) + "'"
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
       # print(rows)
        if(rows is None): return result # empty set
        for row in rows:
            result0 = []
            for row0 in row:
                result0.append(str(row0))
        #print(str(row0))
        #print(str(row0).encode('utf-8'))
            result.append(result0)
        #print(result0)
    else: # one
        rows = cursor.fetchone()
        #print(rows)
        if(rows is None): return result # empty set
        for row in rows:
            result.append(str(row))
    #print(result)
    return result

def select_prot_info(num):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    query = "select prot_info.name, prot_info.contact from user_info, prot_info where user_info.prot_id = prot_info.id and user_info.id = "
    query += str(num)+";"
    #print(query)
    cursor.execute(query)
    connection.commit()
    rows = cursor.fetchall()

    return rows

def get_target_data2db(query):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    cursor.execute(query)
    connection.commit()
    rows = cursor.fetchall()

    return rows
    
def select_fall_down(**kwargs):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    query = "select id,timestamp,num from sensor_data where sensor_id=5 and "
    for key, value in kwargs.items():
        query += str(key) + "=" + str(value)
    query += " ORDER BY id DESC LIMIT 5;"
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

def select_touch(**kwargs):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    query ="select sum(num) from sensor_data where sensor_id=7 and "
    for key, value in kwargs.items():
        query += str(key) + "=" + str(value)
    query += ";"
    cursor.execute(query)
    connection.commit()
    rows = cursor.fetchone()
    #print(rows)

    return rows[0]

def select_today_realtime(**kwargs):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)

    today_query ="select day(now());"
    #print("today query", today_query)
    cursor.execute(today_query)
    connection.commit()
    today = cursor.fetchone()

    query = "select SUM(num) from sensor_data where sensor_id=6 and day(timestamp)="+str(today[0])+" and "
    for key, value in kwargs.items ():
        query += str(key) + "=" + str(value)
    query += ";"
    #"select count(*) as num from fall_down ;"
    #print(query)
    cursor.execute(query)
    connection.commit()
    rows = cursor.fetchone()

    return rows[0]
    
def select_realtime(**kwargs):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    query ="select num from sensor_data where sensor_id=6 and "
    for key, value in kwargs.items():
        query += str(key) + "=" + str(value)
    query += " order by id desc;"
    cursor.execute(query)
    connection.commit()
    rows = cursor.fetchone()
    print(rows[0])

    return rows[0]

def select_avg_realtime(**kwargs):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    query ="select AVG(num) from sensor_data where sensor_id=8 and "
    for key, value in kwargs.items():
        query += str(key) + "=" + str(value)
    query += ";"
    cursor.execute(query)
    connection.commit()
    rows = cursor.fetchone()
    
    return rows[0]

def select_latest_realtime(**kwargs):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    query = "select SUM(num) from sensor_data where sensor_id=8 and "
    for key, value in kwargs.items ():
        query += str(key) + "=" + str(value)
    query += " ORDER BY id DESC LIMIT 5;"
    #"select count(*) as num from fall_down ;"
    print(query)
    cursor.execute(query)
    connection.commit()
    rows = cursor.fetchone()

    return rows[0]

def select_sub_activity(**kwargs):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    today_query ="select day(now());"
    #print("today query", today_query)
    cursor.execute(today_query)
    connection.commit()
    today = cursor.fetchone()
    print("day :" ,today[0] )
    #select sum(num) from sensor_data where sensor_id=6 day(timestamp)=today
    today_activity_query ="select SUM(num) from sensor_data where day(timestamp)=" + str(today[0])+" and "
    cnt = 0
    length = len(kwargs)
    for key, value in kwargs.items():
        today_activity_query += str(key) + "=" + str(value)
        cnt+=1
        if (cnt < length):
            today_activity_query += " and "
    today_activity_query += ";"
    cursor.execute(today_activity_query)
    #print("today activity query", today_activity_query)
    connection.commit()
    today_activity = cursor.fetchone()
    
    before_day = int(today[0] - 1) #어제 날짜
    before_day_query ="select SUM(num) from sensor_data where day(timestamp)=" + str(before_day)+" and "
    cnt = 0
    length = len(kwargs)
    for key, value in kwargs.items():
        before_day_query += str(key) + "=" + str(value)
        cnt+=1
        if (cnt < length):
            before_day_query += " and "
    before_day_query += ";"
    cursor.execute(before_day_query)
    connection.commit()
    before_day_activity = cursor.fetchone()
    print(before_day_activity[0])
    sub_activity = int(today_activity[0]) - int(before_day_activity[0])
    if sub_activity > 0 :
        sub_activity = "+ " +str(sub_activity)
    else:
        sub_activity = "- " + str(abs(sub_activity))
    return str(sub_activity)


def select_avg_sleep(**kwargs):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    #select sum(num) from sensor_data where sensor_id=6 day(timestamp)=today
    today_activity_query ="select avg(hour(timestamp)) from sensor_data where "
    cnt = 0
    length = len(kwargs)
    for key, value in kwargs.items():
        today_activity_query += str(key) + "=" + str(value)
        cnt+=1
        if (cnt < length):
            today_activity_query += " and "
    today_activity_query += ";"
    #print("today activity query", today_activity_query)
    cursor.execute(today_activity_query)
    hour = cursor.fetchone()

    activity_query ="select avg(minute(timestamp)) from sensor_data where "
    cnt = 0
    length = len(kwargs)
    for key, value in kwargs.items():
        activity_query += str(key) + "=" + str(value)
        cnt+=1
        if (cnt < length):
            activity_query += " and "
    activity_query += ";"
    cursor.execute(activity_query)
    minute= cursor.fetchone()
    
    return int(hour[0]),int(minute[0])


def select_min_max(**kwargs):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    today_query ="select day(now());"
    #print("today query", today_query)
    cursor.execute(today_query)
    connection.commit()
    today = cursor.fetchone()
    #print("day :" ,today[0] )
    #select sum(num) from sensor_data where sensor_id=6 day(timestamp)=today
    query ="select min(num),max(num) from sensor_data where day(timestamp)=" + str(today[0])+" and "
    cnt = 0
    length = len(kwargs)
    for key, value in kwargs.items():
        query += str(key) + "=" + str(value)
        cnt+=1
        if (cnt < length):
            query += " and "
    query += ";"
    cursor.execute(query)
    connection.commit()
    #row = cursor.fetchone()
    rows = cursor.fetchall()
    
    return rows

def user_avg_activity():
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    query ="select avg(num) from sensor_data where sensor_id=6 and hour(timestamp)>=6 and hour(timestamp)<=21 group by hour(timestamp) order by hour(timestamp); "
    cursor.execute(query)
    connection.commit()
    rows = cursor.fetchall()
    #print(rows)
    
    return rows

def ONEuser_avg_activity(**kwargs):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    query ="select avg(num) from sensor_data where sensor_id=6 and hour(timestamp)>=6 and hour(timestamp)<=21 and "
    for key, value in kwargs.items ():
        query += str(key) + "=" + str(value)
    query += " group by hour(timestamp) order by hour(timestamp); "
    cursor.execute(query)
    connection.commit()
    rows = cursor.fetchall()
    #print(rows)
    
    return rows

def select_question(**kwargs):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    today_query ="select day(now());"
    cursor.execute(today_query)
    connection.commit()
    today = cursor.fetchone()

    query ="select a1,a2,a3,a4 from user_qa where day(timestamp)=" + str(today[0])+" and "
    cnt = 0
    length = len(kwargs)
    for key, value in kwargs.items():
        query += str(key) + "=" + str(value)
        cnt+=1
        if (cnt < length):
            query += " and "
    query += ";"
    cursor.execute(query)
    connection.commit()
    rows = cursor.fetchall()
    A = []
    for n in rows:
        for f in n:
            if f == 0:
                A.append('X')
            else:
                A.append('O')
    return A


def select_wake_up(**kwargs):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    query = "select id,hour(timestamp),minute(timestamp) from sensor_data where sensor_id = 3 and "
    for key, value in kwargs.items():
        query += str(key) + "=" + str(value)
    query += " order by id desc limit 1;"
    cursor.execute(query)
    connection.commit()
    #print(query)
    rows = cursor.fetchall()
    #print(rows)
    return rows

def select_sleep(**kwargs):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    query = "select id,hour(timestamp),minute(timestamp) from sensor_data where sensor_id = 4 and "
    for key, value in kwargs.items():
        query += str(key) + "=" + str(value)
    query += " order by id desc limit 1;"
    cursor.execute(query)
    connection.commit()
    rows = cursor.fetchall()
    return rows

def compare_sleep_time(**kwargs):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    query = "select id,hour(timestamp),minute(timestamp) from sensor_data where sensor_id = 4 and "
    for key, value in kwargs.items():
        query += str(key) + "=" + str(value)
    query += " order by id desc limit 1;"
    cursor.execute(query)
    connection.commit()
    rows = cursor.fetchall()
    return rows


def ffff_data(data_name, *args):
    connection, cursor = connectRDS(host, port, userName, userPasswd, database)
    query = "update ffff set fall = " +str(args[1])+ " where id = 1"
    cursor.execute(query)
    connection.commit()

