import datetime
import math
import os
import sqlite3
import plotly.plotly as py
import matplotlib.pyplot as plt


#
#
# Time
def timeFormatting(time):
    if len(time) == 19:
        return time + ".000"
    else:
        return time

def elapsedTimeCalculating(startTime, endTime):
    startTime = datetime.datetime.strptime(startTime, "%Y.%m.%d_%H.%M.%S.%f")
    endTime = datetime.datetime.strptime(endTime, "%Y.%m.%d_%H.%M.%S.%f")
    elapsedTime = endTime - startTime

    return elapsedTime.total_seconds()

def secToTimeFormatting(sec):
    if len(str(datetime.timedelta(seconds=sec))) <= 8:
        return str(datetime.timedelta(seconds=sec))+".000"
    else:
        return str(datetime.timedelta(seconds=sec))[:-3]

def timeToSecFormating(tim):
    HOUR, MIN, SEC = tim.split(":")
    SEC, MIL = SEC.split(".")

    return datetime.timedelta(hours=int(HOUR), minutes=int(MIN), seconds=int(SEC), milliseconds=int(MIL)).total_seconds()

def timeBinning(startTime, endTime):
    startTime = datetime.datetime.strptime(startTime, "%Y.%m.%d_%H.%M.%S.%f")
    endTime = datetime.datetime.strptime(endTime, "%Y.%m.%d_%H.%M.%S.%f")

    bins = []
    while startTime < endTime:
        bins.append([startTime.strftime("%Y.%m.%d_%H.%M.%S.%f")[:-3], (startTime + datetime.timedelta(minutes=5)).strftime("%Y.%m.%d_%H.%M.%S.%f")[:-3]])
        startTime += datetime.timedelta(minutes=5)

    return bins

def fileExisting(file):
    if os.path.isfile(file):
        os.remove(file)

def dayCalculating(time):
    time = datetime.datetime.strptime(time, "%Y.%m.%d_%H.%M.%S.%f")

    return time.weekday()

#
#
# DataMining
def entropy(valueArray):
    sumValues = sum(valueArray)
    probArray = [round(value/sumValues, 3) for value in valueArray]
    # print(">>", probArray)
    result = [round(-1 * prob * math.log10(prob), 3) for prob in probArray]
    # print(">>>>>", result)

    return round(sum(result), 3)

#
#
# Database
def APPDATABASEMAKING(file, appArray):
    fileExisting(file)

    connect = sqlite3.connect(file)
    cursor = connect.cursor().execute("CREATE TABLE APPTABLE(TIMESTAMP TEXT, RUNNING TEXT, PACKAGE TEXT)")

    for row in appArray:
        cursor.execute("INSERT INTO APPTABLE(TIMESTAMP, RUNNING, PACKAGE) VALUES(?, ?, ?);", (row[0], row[1], row[2]))

    connect.commit()
    connect.close()

def NOTIDATABASEMAKING(file, logArray):
    fileExisting(file)

    connect = sqlite3.connect(file)
    cursor = connect.cursor().execute("CREATE TABLE NOTIFICATIONTABLE(TIMESTAMP TEXT, POSTREMOVALRINGER TEXT, PACKAGE TEXT, TITLE TEXT, TEXT TEXT, SUBTEXT TEXT, SOUND TEXT, VIBRATE TEXT, DEFAULTS INT, LEDON INT, LEDOFF INT, LEDRGB INT)")

    for row in logArray:
        cursor.execute("INSERT INTO NOTIFICATIONTABLE(TIMESTAMP, POSTREMOVALRINGER, PACKAGE, TITLE, TEXT, SUBTEXT, SOUND, VIBRATE, DEFAULTS, LEDON, LEDOFF, LEDRGB) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]))

    connect.commit()
    connect.close()

def APNODATABASEMAKING(file, appArray):
    fileExisting(file)

    connect = sqlite3.connect(file)
    cursor = connect.cursor().execute("CREATE TABLE APNOTABLE(TIMESTAMP TEXT, TYPE TEXT, PACKAGE TEXT, TITLE TEXT, TEXT TEXT, SUBTEXT TEXT, SOUND TEXT, VIBRATE TEXT, DEFAULTS INT, LEDON INT, LEDOFF INT, LEDRGB INT)")

    for row in appArray:
        cursor.execute("INSERT INTO APNOTABLE(TIMESTAMP, TYPE, PACKAGE, TITLE, TEXT, SUBTEXT, SOUND, VIBRATE, DEFAULTS, LEDON, LEDOFF, LEDRGB) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]))

    connect.commit()
    connect.close()

def USAGEDATABASEMAKING(file, usageArray):
    fileExisting(file)

    connect = sqlite3.connect(file)
    cursor = connect.cursor().execute("CREATE TABLE USAGETABLE(TYPE TEXT, STARTTIME TEXT, ENDTIME TEXT, ELAPSEDTIME TEXT)")

    for row in usageArray:
        cursor.execute("INSERT INTO USAGETABLE(TYPE, STARTTIME, ENDTIME, ELAPSEDTIME) VALUES(?, ?, ?, ?);", (row[0], row[1], row[2], row[3]))

    connect.commit()
    connect.close()

def CLASSUSAGEDATABASEMAKING(file, usageArray):
    fileExisting(file)

    connect = sqlite3.connect(file)
    cursor = connect.cursor().execute("CREATE TABLE CLASSUSAGETABLE(CLASSNAME TEXT, ENTRANCETIME TEXT, EXITTIME TEXT, TYPE TEXT, STARTTIME TEXT, ENDTIME TEXT, ELAPSEDTIME TEXT)")

    for row in usageArray:
        cursor.execute("INSERT INTO CLASSUSAGETABLE(CLASSNAME, ENTRANCETIME, EXITTIME, TYPE, STARTTIME, ENDTIME, ELAPSEDTIME) VALUES(?, ?, ?, ?, ?, ?, ?)", (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    connect.commit()
    connect.close()

def CLASSAPNODATABASEMAKING(file, classApnoArray):
    fileExisting(file)

    connect = sqlite3.connect(file)
    cursor = connect.cursor().execute("CREATE TABLE CLASSAPNOTABLE(Z TEXT, TIMESTAMP TEXT, TYPE TEXT, PACKAGE TEXT)")

    for row in classApnoArray:
        cursor.execute("INSERT INTO CLASSAPNOTABLE(Z, TIMESTAMP, TYPE, PACKAGE) VALUES(?, ?, ?, ?)", (row[0], row[1], row[2], row[3]))

    connect.commit()
    connect.close()


#
#
# ploting

def PLOTING3D(X, Y, Z):
    scatter = dict(
        mode="markers", name="y", type="scatter3d",
        x=X, y=Y, z=Z,
        marker=dict(size=2, color="rgb(23, 190, 207)")
    )
    clusters = dict(
        alphahull=7, name="y", opacity=0.1, type="mesh3d",
        x=X, y=Y, z=Z
    )
    layout = dict(
        title='3d point clustering',
        scene=dict(
            xaxis=dict(zeroline=False),
            yaxis=dict(zeroline=False),
            zaxis=dict(zeroline=False),
        )
    )
    fig = dict(data=[scatter, clusters], layout=layout)
    py.plotly.tools.set_credentials_file(username='dhgkjdasf', api_key='cURhfnaDsgSDmOc0OHQw')
    py.plot(fig, filename='3d point clustering')
    plt.show()















# def elapsedTimeArrayCalculating(startTimeArray, endTimeArray):
#     elapsedTimeArray = []
#     for index in range(0, len(startTimeArray)):
#         startTIme = datetime.datetime.strptime(startTimeArray[index][0][0:], "%Y.%m.%d_%H.%M.%S")
#         endTime = datetime.datetime.strptime(endTimeArray[index][0][0:], "%Y.%m.%d_%H.%M.%S")
#         elapsedTimeArray.append(str(endTime - startTIme))
#
#     return elapsedTimeArray

#
# def sumUpTimeCalculating(startTime, endTime):
#     startHour, startMin, startSec = startTime.split(":")
#     startSec, startMil = startSec.split(".")
#
#     endHour, endMin, endSec = endTime.split(":")
#     endSec, endMil = endSec.split(".")
#
#     return str(int(startHour) + int(endHour)) + ":" + str(int(startMin) + int(endMin)) + ":" + str(int(startSec) + int(endSec)) + "." + str(int(startMil) + int(endMil))




# # APPSESSUIBDATABASE
# def APPSESSIONDATABASEMAKING(file, appSessionArray):
#     fileExisting(file)
#
#     connect = sqlite3.connect(file)
#     cursor = connect.cursor().execute("CREATE TABLE APPSESSIONTABLE(ID TEXT, CLASSNAME TEXT, STARTTIME TEXT, ENDTIME TEXT, SESSIONTIME TEXT, SESSIONTYPE TEXT, SESSIONPACKAGE TEXT)")
#
#     for row in appSessionArray:
#         cursor.execute("""INSERT INTO APPSESSIONTABLE(ID, CLASSNAME, STARTTIME, ENDTIME, SESSIONTIME, SESSIONTYPE, SESSIONPACKAGE) VALUES(?, ?, ?, ?, ?, ?, ?);""",
#                        (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
#
#     connect.commit()
#     connect.close()
#
# def APPSESSIONDATABASEMERGING(file, appSessionArray):
#     fileExisting(file)
#
#     connect = sqlite3.connect(file)
#     cursor = connect.cursor().execute("CREATE TABLE APPSESSIONTABLE(ID TEXT, CLASSNAME TEXT, STARTTIME TEXT, ENDTIME TEXT, SESSIONTIME TEXT, SESSIONTYPE TEXT, SESSIONPACKAGE TEXT)")
#
#     for row in appSessionArray:
#         cursor.execute("""INSERT INTO APPSESSIONTABLE(ID, CLASSNAME, STARTTIME, ENDTIME, SESSIONTIME, SESSIONTYPE, SESSIONPACKAGE) VALUES(?, ?, ?, ?, ?, ?, ?);""",
#                        (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
#
#     connect.commit()
#     connect.close()
#
# def APPSESSIONCNTDATABASEMERGING(file ,appSessionArray):
#     fileExisting(file)
#
#     connect = sqlite3.connect(file)
#     cursor = connect.cursor().execute(
#         "CREATE TABLE APPSESSIONTABLE(ID TEXT, CLASSNAME TEXT, USAGESTARTTIME TEXT, USAGEENDTIME TEXT, SESSIONPACKAGE TEXT, SESSIONSTARTTIME TEXT, SESSIONENDTIME TEXT, SHORTCOUNT, LONGCOUNT, SCROLLCOUNT, KEYCOUNT)")
#
#     for row in appSessionArray:
#         cursor.execute(
#             """INSERT INTO APPSESSIONTABLE(ID, CLASSNAME, USAGESTARTTIME, USAGEENDTIME, SESSIONPACKAGE, SESSIONSTARTTIME, SESSIONENDTIME, SHORTCOUNT, LONGCOUNT, SCROLLCOUNT, KEYCOUNT) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ? ,? ,?);""",
#             (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]))
#
#     connect.commit()
#     connect.close()
#
#
# def AGGREGATIONDATABASEMAKING(file, aggregationArray):
#     fileExisting(file)
#
#     connect = sqlite3.connect(file)
#     cursor = connect.cursor().execute(
#         "CREATE TABLE AGGREGATIONTABLE(ID TEXT, " +
#         "CLASS_NAME TEXT, CLASS_ENTRANCE TEXT, CLASS_EXIT TEXT, " +
#         "USAGE_START TEXT, USAGE_EXIT TEXT, USAGE_ELAPSED TEXT, " +
#         "SESSION_NAME TEXT, SESSION_START, SESSION_EXIT, SESSION_ELAPSED, SHORT, LONG, SCROLL, KEY)")
#
#     for row in aggregationArray:
#         cursor.execute(
#             """INSERT INTO AGGREGATIONTABLE(ID, CLASS_NAME, CLASS_ENTRANCE, CLASS_EXIT, USAGE_START, USAGE_EXIT, USAGE_ELAPSED,
#             SESSION_NAME, SESSION_START, SESSION_EXIT, SESSION_ELAPSED, SHORT, LONG, SCROLL, KEY) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
#             (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14]))
#
#     connect.commit()
#     connect.close()






# def activityTableMerging(path, activityArray):
#     fileExisting(path, "ACTIVITYDATABASE.db")
#
#     connect = sqlite3.connect(path + "\\ACTIVITYDATABASE.db")
#     cursor = connect.cursor().execute("CREATE TABLE ACTIVITYTABLE(TIMESTAMP TEXT, VEHICLE INTEGER, BICYCLE INTEGER, FOOT INTEGER, RUNNING INTEGER, STILL INTEGER, WALKING INTEGER, UNKNOWN INTEGER)")
#     for row in activityArray:
#         cursor.execute("""INSERT INTO ACTIVITYTABLE(TIMESTAMP, VEHICLE, BICYCLE, FOOT, RUNNING, STILL, WALKING, UNKNOWN) VALUES(?, ?, ?, ?, ?, ?, ?, ?);""", (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
#     connect.commit()
#     connect.close()
#
# def specificActivityTableMerging(path, name, timeArray, activityArray):
#     fileExisting(path, name + ".db")
#
#     connect = sqlite3.connect(path + "\\" + name + ".db")
#     cursor = connect.cursor().execute("CREATE TABLE ACTIVITYTABLE(TIME TEXT, ACTIVITY TEXT)")
#     for index in range(0, len(activityArray)):
#         cursor.execute("""INSERT INTO ACTIVITYTABLE(TIME, ACTIVITY) VALUES(?, ?);""", (timeArray[index], activityArray[index]))
#     connect.commit()
#     connect.close()
#

# def specificAppTableMerging(path, name, startTimeArray, endTimeArray, elapsedTimeArray):
#     fileExisting(path, name + ".db")
#
#     connect = sqlite3.connect(path + "\\" + name + ".db")
#     cursor = connect.cursor().execute("CREATE TABLE APPTABLE(STARTTIME TEXT, ENDTIME TEXT, ELAPSEDTIME TEXT)")
#     for index in range(0, len(startTimeArray)):
#         cursor.execute("""INSERT INTO APPTABLE(STARTTIME, ENDTIME, ELAPSEDTIME) VALUES(?, ?, ?);""", (startTimeArray[index][0], endTimeArray[index][0], str(elapsedTimeArray[index])))
#     connect.commit()
#     connect.close()

# def LOGDATABASEMAKING(file, logArray):
#     fileExisting(file)
#
#     connect = sqlite3.connect(file)
#     cursor = connect.cursor().execute("CREATE TABLE LOGTABLE(TIMESTAMP TEXT, CALLSMS TEXT, NUMBER TEXT, TYPE TEXT, DURATIONBODY TEXT, READ TEXT)")
#
#     for row in logArray:
#         cursor.execute("""INSERT INTO LOGTABLE(TIMESTAMP, CALLSMS, NUMBER, TYPE, DURATIONBODY, READ) VALUES(?, ?, ?, ?, ?, ?);""", (row[0], row[1], row[2], row[3], row[4], row[5]))
#
#     connect.commit()
#     connect.close()

# def specificLogTableMerging(path, name, logArray):
#     fileExisting(path, name + ".db")
#
#     connect = sqlite3.connect(path + "\\" + name + ".db")
#     cursor = connect.cursor().execute("CREATE TABLE LOGTABLE(TIMESTAMP TEXT, CALLSMS TEXT, NUMBER TEXT, TYPE TEXT, DURATIONBODY TEXT, READ TEXT)")
#     for row in logArray:
#         cursor.execute("""INSERT INTO LOGTABLE(TIMESTAMP, CALLSMS, NUMBER, TYPE, DURATIONBODY, READ) VALUES(?, ?, ?, ?, ?, ?);""", (row[0], row[1], row[2], row[3], row[4], row[5]))
#     connect.commit()
#     connect.close()