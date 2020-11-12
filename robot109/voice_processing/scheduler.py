import datetime
import schedule
import time
from data import DBapi
from voice_processing import scenario
days = ["월","화","수","목","금","토","일"]

global tag_cnt
global user_id

def sche(name,j):
    print("tts",name,j[0],j[1])
    scenario.call_Ask_medicine(name,j[0],j[1])

def cre_job():
    global tag_cnt
    tag_cnt = -1
    global user_id
    today = datetime.datetime.today().weekday()
    print("select * from medicine_data where user_id = {} and {} = 1;".format(user_id,days[today]))
    #DBapi.request("select * from medicine_data where user_id = {} and {} = 1;".format(user_id,days[today]),"medicine_data")

    medicine_time_list = list()
    
    r = open("/home/pi/robot109/data/medicine_info.txt", 'r', encoding='UTF8')
    list_temp = eval(r.readline())
    for i in list_temp:
        medicine_time_list.append([i["name"],i["time"]])
    r.close()

    for i in medicine_time_list:
        name = i[0]
        for j in i[1]:
            if j[1] != -1:
                tag_cnt += 1
                print("set {} = {}:{}".format(i[0],str(j[0]).zfill(2),str(j[1]).zfill(2)))
                schedule.every().day.at("{}:{}".format(str(j[0]).zfill(2),str(j[1]).zfill(2))).do(sche,name,j).tag(tag_cnt)  
        
def del_job():
    global tag_cnt
    if tag_cnt:
        return
    for i in range(0,tag_cnt+1):
        print("clear:",i)
        schedule.clear(i)


def ask_job():
    global user_id
    ans = scenario.call_Ask_dq()
    DBapi.request("insert into user_qa(user_id,a1,a2,a3,a4) values ({},{},{},{},{})".format(user_id,ans[0],ans[1],ans[2],ans[3]),1)
    


def main():
    global user_id
    with open('/home/pi/robot109/data/user_info.txt','r') as inf:
        user_id = eval(inf.read())["id"]
    ask_job()
    """
    schedule.every().day.at("00:01").do(cre_job)
    schedule.every().day.at("23:59").do(del_job)

    schedule.every().day.at("14:00").do(ask_job)

    while True:
        schedule.run_pending()
        time.sleep(1)"""
 
if __name__=="__main__":
    main()