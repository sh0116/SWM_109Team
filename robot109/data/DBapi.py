import requests
import json
import time

url = "http://www.109center.com:5000/set_rasinfo"


def booting_user_info():
    f = open("/home/pi/robot109/data/user_info.txt", 'r')
    user_id = f.readline()
    f.close()

    data = request("select * from user_info where id = {};".format(user_id),"user_info")


    
    w = open("/home/pi/robot109/data/user_info.txt", 'w', encoding='UTF8')
    w.write("{\n")
    w.write("\'id\':\"{}\",\n".format(data["id"].strip(" ")))
    w.write("\'name\':\"{}\",\n".format(data["name"].strip(" ").replace("\\/", "/").encode().decode('unicode_escape')))
    w.write("\'sex\':\"{}\",\n".format(data["sex"].strip(" ")))
    w.write("\'birth\':\"{}.{}.{}\",\n".format(data["birth"][0],data["birth"][1].strip(" "),data["birth"][2].strip(" ")))
    w.write("\'address\':\"{}\",\n".format(data["address"].strip(" ").replace("\\/", "/").encode().decode('unicode_escape')))
    w.write("\'phone\':\"{}\",\n".format(data["phone"].strip(" ")))
    w.write("\'prot_id\':\"{}\"\n".format(data["prot_id"].strip(" ")))
    w.write("}\n")
    w.close()

    #with open('/home/pi/robot109/data/user_info.txt','r') as inf:
    #print(eval(inf.read())["address"])

def str2dict_user_info(res):
    result  = dict()
    res     = list(res.split(','))
    result["id"]        = res[0][2:]
    result["name"]      = res[1]
    result["sex"]       = res[2]
    result["birth"]     = res[3].split('(')[1],res[4],res[5].split(")")[0]
    result["address"]   = res[6]
    result["phone"]     = res[7]
    result["prot_id"]    = res[8][:-1]

    return result

def str2dict_prot_info(res):
    result  = dict()
    res     = list(res.split(','))

    result["id"]        = res[0][1:]
    result["name"]      = res[1]
    result["phone"]     = res[2]

    return result

def str2diict_robot_info(res):
    result  = dict()
    res     = list(res.split(','))

    result["id"]        = res[0][1:]
    result["serial"]      = res[1]
    result["ip"]       = res[2]
    result["user_id"]   = res[3]

    return result

def str2dict_count(res):
    result  = dict()

    result["cnt"]   = res[1]

    return result

def str2dict_medicine_data(res):
    result = list()
    res = ","+res
    res = res.replace('datetime.timedelta(0)',"datetime.timedelta(-1,-1)")
    res = res.replace('None',"datetime.timedelta(-1,-1)")
    res_lists = res.split("))")
    print(res)
    for res_list in res_lists[:-1]:
        res_list2 = res_list.split(",")
        res_temp = dict()
        #medic_id
        res_temp["id"] = res_list2[1][2:]
        #name
        res_temp["name"] = res_list2[2].replace("\\/", "/").encode().decode('unicode_escape')
        #user_id
        res_temp["user_id"] = res_list2[3][1:]
        #day
        res_temp["days"] = res_list2[4][1:]+res_list2[5][1:]+res_list2[6][1:]+res_list2[7][1:]+res_list2[8][1:]+res_list2[9][1:]+res_list2[10][1:]
        res_temp_temp = list()
        for i in range(0,4,2):
            time = int(res_list2[12+i][:-1])
            if time//3600 > 0:
                hour = time//3600
                minute = time%3600//60
            else:
                hour = 0
                minute = time//60
            res_temp_temp.append([hour,minute])
        time = int(res_list2[16])
        print(time)
        if time//3600 > 0:
            hour = time//3600
            minute = time%3600//60
        else:
            hour = 0
            minute = time//60
        print(hour,minute)
        res_temp_temp.append([hour,minute])

        res_temp["time"] = res_temp_temp
        
        result.append(res_temp)
    
    w = open("/home/pi/robot109/data/medicine_info.txt", 'w', encoding='UTF8')
    w.write(str(result))
    w.close()
    return result

def request(job,table):
    push_data = {
        'query'       : job,
    }
    response = requests.post(url,data=push_data)
    print(response.text)
    try:
        fun_name = "str2dict_" + table
        return globals()[fun_name]( response.text )
    except:
        return "can't transfer"

if __name__ =="__main__":
    #booting_user_info()
    #insert into sensor_data (user_id ,sensor_id,num) values (3,6,26);

    print(request("insert into user_qa(user_id,a1,a2,a3,a4) values (1,{},{},{},{})".format(1,1,1,1),1))



    """print(request("insert into sensor_data (user_id ,sensor_id,num) values (3,6,23);","sensor_data"))
    time.sleep(1)
    print(request("insert into sensor_data (user_id ,sensor_id,num) values (3,6,70);","sensor_data"))
    time.sleep(1)
    print(request("insert into sensor_data (user_id ,sensor_id,num) values (3,6,90);","sensor_data"))
    time.sleep(1)
    print(request("insert into sensor_data (user_id ,sensor_id,num) values (3,6,60);","sensor_data"))
    time.sleep(1)
    print(request("insert into sensor_data (user_id ,sensor_id,num) values (3,6,35);","sensor_data"))
    time.sleep(1)
    print(request("insert into sensor_data (user_id ,sensor_id,num) values (3,6,20);","sensor_data"))
    time.sleep(1)
    print(request("insert into sensor_data (user_id ,sensor_id,num) values (3,6,80);","sensor_data"))
    time.sleep(1)
    print(request("insert into sensor_data (user_id ,sensor_id,num) values (3,6,70);","sensor_data"))
    time.sleep(1)
    print(request("insert into sensor_data (user_id ,sensor_id,num) values (3,6,10);","sensor_data"))
    time.sleep(1)
    print(request("insert into sensor_data (user_id ,sensor_id,num) values (3,6,90);","sensor_data"))
    time.sleep(1)
    print(request("insert into sensor_data (user_id ,sensor_id,num) values (3,6,50);","sensor_data"))
    time.sleep(1)
    print(request("insert into sensor_data (user_id ,sensor_id,num) values (3,6,23);","sensor_data"))
    time.sleep(1)
    print(request("insert into sensor_data (user_id ,sensor_id,num) values (3,6,70);","sensor_data"))
    time.sleep(1)
    print(request("insert into sensor_data (user_id ,sensor_id,num) values (3,6,90);","sensor_data"))
    time.sleep(1)
    print(request("insert into sensor_data (user_id ,sensor_id,num) values (3,6,60);","sensor_data"))
    time.sleep(1)
    print(request("insert into sensor_data (user_id ,sensor_id,num) values (3,6,35);","sensor_data"))
    time.sleep(1)
    print(request("insert into sensor_data (user_id ,sensor_id,num) values (3,6,20);","sensor_data"))
    time.sleep(1)
    print(request("insert into sensor_data (user_id ,sensor_id,num) values (3,6,80);","sensor_data"))
    time.sleep(1)
    print(request("insert into sensor_data (user_id ,sensor_id,num) values (3,6,70);","sensor_data"))
    time.sleep(1)
    print(request("insert into sensor_data (user_id ,sensor_id,num) values (3,6,10);","sensor_data"))
    time.sleep(1)
    print(request("insert into sensor_data (user_id ,sensor_id,num) values (3,6,90);","sensor_data"))
    time.sleep(1)
    print(request("insert into sensor_data (user_id ,sensor_id,num) values (3,6,50);","sensor_data"))"""


    #print(request("select * from medicine_data where user_id = {};".format(1),"medicine_data"))
    #print(request("select * from medicine_data where user_id = {} and \"{}\" = 1;".format(1,"월"),"medicine_data"))
    #print(request("Insert into user_information(name,gender,birth,address,contact,prot_id) values(\"박수현\", \"m\", \"1980-02-20\", \"강남구 테헤란로 311\", \"010-7867-9796\",4);","medicine_data"))
    #print(request("Insert into prot_information(name,contact) values(\"박필준\",\"010-9284-9796\");","medicine_data"))
    #print(request("update user_info set address = \"강남구 테헤란로 322\" where id = 4;",1))