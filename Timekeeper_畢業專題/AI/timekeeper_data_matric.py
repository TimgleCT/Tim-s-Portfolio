import matplotlib as mpl
mpl.use('Agg')
import mysql.connector
import pandas as pd
import pylab as pl
import matplotlib.pyplot as plt
import numpy as np


data_matric_list = []
label_list = []

def create_data_matric():
    db = mysql.connector.connect(
            user = 'root',
            password = 'keeper',
            host = '140.127.218.207',
            database = 'TimeKeeper',
            charset = 'utf8')

    cur = db.cursor()
    get_alarmtime_query = ("SELECT * FROM `screen_record` WHERE r_ifawake IS NOT NULL")
    cur.execute(get_alarmtime_query)
    get_alarmtime = cur.fetchall()
    test = []
    for row in get_alarmtime:
        test.append(row[0])
    print(test)
    print(len(test))
    count_data = []
    for alarmtime in test:
        count_data_query = ("SELECT COUNT(sound_axis_record.Date_alarm) FROM `sound_axis_record` WHERE sound_axis_record.Date_alarm = '"+alarmtime+"'")
        cur.execute(count_data_query)
        data = cur.fetchall()
        for row in data:
            count_data.append(row[0])
    print(count_data)
    print(len(count_data))
    j = 0
    for alarmtime in test:
        if(count_data[j] != 121):
            j+=1
            pass
        else:
            get_data_query = ("SELECT user.user_id, screen_record.Date, screen_record.Period, screen_record.r_ifawake, sound_axis_record.X_axis, sound_axis_record.Y_axis, sound_axis_record.Z_axis, sound_axis_record.Sound_db, sound_axis_record.Date_time FROM user, screen_record, sound_axis_record WHERE user.user_id = screen_record.User_id AND sound_axis_record.Date_alarm = screen_record.Date AND screen_record.r_ifawake IS NOT NULL AND screen_record.Date ='"+alarmtime+"'")
            cur.execute(get_data_query)
            pic_data = cur.fetchall()
            user = []
            X_axis = []
            Y_axis = []
            Z_axis = []
            Sound_db = []
            usage = []
            ifawake = []
            time = []
            sec = 0.0
            # 形成一個矩陣，一筆資料，row[0]是u_id,row[1]是alarmtime,row[2]是usage,row[3]是ifawake,row[4]是X,5=>y,6Z,7db
            data_matric = np.zeros((11,11,5))
            line = 0
            for row in pic_data:
                X_axis.append(row[4])
                Y_axis.append(row[5])
                Z_axis.append(row[6])
                Sound_db.append(row[7]/10)
                p = row[2]
                ifawake.append(row[3])
            for i in range(p):
                usage.append(1)
            for a in range(121 - p):
                usage.append(0)

            i = 0    
            for line in range(11):
                for column in range(11):
                    data_matric[line][column][0] = X_axis[i]
                    data_matric[line][column][1] = Y_axis[i]
                    data_matric[line][column][2] = Z_axis[i]
                    data_matric[line][column][3] = Sound_db[i]
                    data_matric[line][column][4] = usage[i]
                    i+=1
            data_matric_list.append(data_matric)
            label_list.append(ifawake[0])
            j+=1
    print(data_matric_list[0])
    print(len(data_matric_list))
    print(len(label_list))

create_data_matric()