import requests
import dataCenter

global avg_act ,AVG ,hour
avg_act = [0 for i in range(24)]
AVG = 0
hour = -1

    
def avg_activity(hour_activity):
    global hour,avg_act, AVG
    if AVG > 0:
        activity_dis = abs(hour_activity - AVG)
        if  activity_dis> 200:
            print("emergency")
        else :
            print("!!!!!!!!!!!! more activity !!!!!!!!")
    hour += 1
    avg_act[hour] = hour_activity
    print(avg_act)
    if hour >= 2 and hour <= 24:
        AVG = sum(avg_act[hour-2:hour])/3
    elif hour > 60:
        hour = 0
        avg_act = [0 for i in range(24)]
    hour_activity = 0
        