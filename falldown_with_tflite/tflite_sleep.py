from datetime import datetime

global day, cal_day, pre_time
day = ['monday','tuesday','wednesday', 'thursday', 'friday', 'saturday', 'sunday']
cal_day = datetime.today().weekday()
pre_time = datetime.now()
#nowTuple = pre_time.timetuple()

def day_sleep_time():
    global day, cal_day, pre_time
    sleep_hour = int(nowTuple.tm_hour)
    sleep_min = int(nowTuple.tm_min)
    seconds = (pre_time.hour * 60 + pre_time.minute) * 60 + pre_time.second
    sleep_time = seconds/3600
    data = {'user_id' : '1', 'graph' : sleep_time,'day':day[cal_day]}
    #print("sleep time : {}-{}-{} {}:{}:{}".format(pre_time.year, pre_time.month, pre_time.day,pre_time.hour,pre_time.minute,pre_time.second))
    #print("sleep %d",sleep_time,day[cal_day])

def day_wake_time():
    global day, cal_day, pre_time
    wake_up_hour = int(nowTuple.tm_hour)
    wake_up_min = int(nowTuple.tm_min)
    seconds = (pre_time.hour * 60 + pre_time.minute) * 60 + pre_time.second
    wake_up_time = seconds/3600
    if seconds >= 14400 and seconds <= 27000:
        data = {'user_id' : '3', 'graph' : wake_up_time,'day':day[cal_day]}
        #print("wake up time : {}-{}-{} {}:{}:{}".format(pre_time.year, pre_time.month, pre_time.day,pre_time.hour,pre_time.minute,pre_time.second))
        #print("wake up %d",wake_up_time,day[cal_day])
