from twicebursterDataMining.RH_Library import *
from Bunker.Marines import *
import matplotlib.pyplot as plt

#
#
# 75분 수업만 뽑아내기
class75MDic = {}
for row in sqlite3.connect(getDatabasePathing("SCHEDULEDATABASE.db")).execute("SELECT * FROM SCHEDULETABLE"):
    startTime = datetime.datetime.strptime(list(row)[4][3:8], "%H:%M")
    endTime = datetime.datetime.strptime(list(row)[4][12:], "%H:%M")
    if str(endTime - startTime) == "1:15:00":
        class75MDic[row[0]] = [row[4], row[5]]

#
#
# 전체학생 Bin 평균의 Duration, Frequency 박스플롯
studentsDataDurationDic = {}
for studentIndex in range(0, 2):
    studentDataPath = getStudentDataPathing(studentIndex)
    print(studentDataPath)

    #
    #
    # 출석시간 뽑아내기
    attendanceTimeArray = []
    for attendanceRow in sqlite3.connect(getDatabasePathing("ATTENDANCEDATABASE.db")).execute("SELECT * FROM ATTENDANCETABLE WHERE ID==" + "'" + getStudentID(studentIndex) + "'"):
        if attendanceRow[1] in class75MDic.keys():
            for row in attendanceRow[2:]:
                if row == "":
                    continue
                attendanceTimeArray.append([attendanceRow[1], row.split("~")[0], row.split("~")[1]])

    #
    # 수업 시작시간 뽑아내기
    # 미시경제학, 회계원리만 퍼스트클래스와 세컨드클래스가 시간이 다르므로 따로 처리해야함
    classStartTimeDic = {}
    for attendanceRow in attendanceTimeArray:
        firstClassTime = class75MDic[attendanceRow[0]][0]
        # secondClassTime = classDic[attendanceRow[0]][1]

        startTime = attendanceRow[1][0:11] + firstClassTime[3:5] + "." + firstClassTime[6:8] + ".00.000"

        if attendanceRow[0] in classStartTimeDic.keys():
            classStartTimeDic[attendanceRow[0]].append(startTime)
        else:
            classStartTimeDic[attendanceRow[0]] = [startTime]

    #
    #
    #
    binArray = []
    for className, usingStartTime, usingEndTime in sqlite3.connect(studentDataPath + "\\CLASSUSAGEDATABASE.db").execute("SELECT CLASSNAME, STARTTIME, ENDTIME FROM CLASSUSAGETABLE"):
        for classStartTime in classStartTimeDic[className]:
            if usingStartTime[:10] == classStartTime[:10]:
                binArray.append([elapsedTimeCalculating(classStartTime, usingStartTime), elapsedTimeCalculating(classStartTime, usingEndTime)])

    #
    #
    #
    cnt = 0
    dicDic = {}
    for bin in binArray:
        tempDic = {}
        for sec in range(int(bin[0]), int(bin[1])+1):
            for i in range(0, 15):
                if i * 300 <= sec <= (i+1) * 300:
                    if i in tempDic.keys():
                        tempDic[i] = tempDic[i] + 1
                    else:
                        tempDic[i] = 1

        for row in tempDic.items():
            if row[0] in dicDic.keys():
                dicDic[row[0]].append(row[1])
            else:
                dicDic[row[0]] = [row[1]]

    for row in sorted(dicDic.items(), key=lambda row: row[0]):
        if row[0] in studentsDataDurationDic.keys():
            studentsDataDurationDic[row[0]].append(round(sum(row[1]) / len(row[1]), 3))
        else:
            studentsDataDurationDic[row[0]] = [round(sum(row[1]) / len(row[1]), 3)]

#
#
#
for row in studentsDataDurationDic.items():
    plt.boxplot(row[1], row[0])

plt.show()

