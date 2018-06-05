from twicebursterDataMining.RH_Library import *
from Bunker.Marines import *
import matplotlib.pyplot as plt

#
#
# 수업시간표 뽑아내기
classDic = {}
for row in sqlite3.connect(getDatabasePathing("SCHEDULEDATABASE.db")).execute("SELECT * FROM SCHEDULETABLE"):
    startTime = datetime.datetime.strptime(list(row)[4][3:8], "%H:%M")
    endTime = datetime.datetime.strptime(list(row)[4][12:], "%H:%M")
    classDic[row[0]] = str(endTime - startTime)

#
#
# 수업시간 스마트폰 사용유무 검출하기
studentsData = []
for studentIndex in range(0, 84):
    studentDataPath = getStudentDataPathing(studentIndex)
    print(studentDataPath)

    #
    #
    # 75분 수업만 뽑아내기
    attendanceTimeArray = []
    for attendanceRow in sqlite3.connect(getDatabasePathing("ATTENDANCEDATABASE.db")).execute("SELECT * FROM ATTENDANCETABLE WHERE ID==" + "'" + getStudentID(studentIndex) + "'"):
        if classDic[attendanceRow[1]] == "1:15:00":
            for row in attendanceRow[2:]:
                if row == "":
                    continue
                attendanceTimeArray.append([attendanceRow[1], row.split("~")[0], row.split("~")[1]])

    #
    #
    # 75분 수업에서 스마트폰 사용시간대 뽑아내고, 데이터베이스로 만들기
    classUsageArray = []
    for className, entranceTime, exitTime in attendanceTimeArray:
        for usageRow in sqlite3.connect(studentDataPath + "\\USAGEDATABASE.db").execute("SELECT * FROM USAGETABLE WHERE '" + entranceTime + "' <= STARTTIME and ENDTIME <= '" + exitTime + "'"):
            classUsageArray.append([className, entranceTime, exitTime, usageRow[0], usageRow[1], usageRow[2], usageRow[3]])
    CLASSUSAGEDATABASEMAKING(studentDataPath + "\\CLASSUSAGEDATABASE.db", classUsageArray)

    #
    #
    # 수업시간 스마트폰 사용유무 비율 검출하기
    tempDic = {}
    for row in classUsageArray:
        if (row[1], row[2]) not in tempDic.keys():
            tempDic[(row[1], row[2])] = 1
    studentsData.append(round(len(tempDic)/len(attendanceTimeArray), 3))

#
#
# 전체학생 수업시간 스마트폰 사용유무 박스플롯 (1이 항상 씀, 0이 항상 안씀)
plt.boxplot(studentsData)
plt.xlabel("")
plt.ylabel("")
plt.show()



