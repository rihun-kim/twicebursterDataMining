from twicebursterDataMining.RH_Library import *
from Bunker.Marines import *
import numpy as np
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
# 노티정보
notiCntDic, notiInterSessionDic = {}, {}
for studentIndex in range(0, 84):
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
    #
    # Noti 걸러내기
    notiArray, tempDic = [], {}
    for row in sqlite3.connect(studentDataPath + "\\APNODATABASE.db").execute("SELECT * FROM APNOTABLE WHERE TYPE == 'POSTED'"):
        if row[2] in tempDic.keys():
            tempDic[row[2]].append(row)
            if "kakao" in row[2]:
                if "안 읽은" in row[5]:
                    None
                else:
                    notiArray.append(row)
            elif "kr.co.rinasoft.howuse" in row[2]:
                None
            elif "충전" in row[3] or "키보드" in row[3] or "걸음" in row[3] or "배터리" in row[3]:
                None
            elif elapsedTimeCalculating(tempDic[row[2]][-2][0], tempDic[row[2]][-1][0]) <= 1:
                None
            elif (tempDic[row[2]][-2][3] == tempDic[row[2]][-1][3] and tempDic[row[2]][-2][4] == tempDic[row[2]][-1][4]) or \
                (tempDic[row[2]][-2][2] == tempDic[row[2]][-1][2] and tempDic[row[2]][-2][3] == tempDic[row[2]][-1][3] and \
                 elapsedTimeCalculating(tempDic[row[2]][-2][0], tempDic[row[2]][-1][0]) <= 5):
                None
            else:
                notiArray.append(row)
        else:
            tempDic[row[2]] = [row]
            notiArray.append(row)

    #
    #
    # 수업시간 Noti 걸러내기
    attendanceTimeArray = []
    for attendanceRow in sqlite3.connect(getDatabasePathing("ATTENDANCEDATABASE.db")).execute("SELECT * FROM ATTENDANCETABLE WHERE ID==" + "'" + getStudentID(studentIndex) + "'"):
        if attendanceRow[1] in class75MDic.keys():
            for row in attendanceRow[2:]:
                if row == "":
                    continue
                attendanceTimeArray.append([attendanceRow[1], row.split("~")[0], row.split("~")[1]])

    notiArray.sort(key=lambda row: row[0])

    notiCntDic[studentIndex], notiInterSessionDic[studentIndex] = [], []
    for className, startTime, endTime in attendanceTimeArray:
        notiCnt = 0
        tempClassNotiArray = []
        deleteIndexArray = []

        for index, row in enumerate(notiArray):
            if startTime <= row[0] <= endTime:
                notiCnt += 1
                tempClassNotiArray.append(row[0])
                deleteIndexArray.append(index)

        for index in deleteIndexArray:
            del notiArray[index]

        length = len(tempClassNotiArray)
        if length <= 1:
            continue

        notiCntDic[studentIndex].append(notiCnt)

        tempArray = []
        for index in range(0, length-1):
            tempArray.append(elapsedTimeCalculating(tempClassNotiArray[index], tempClassNotiArray[index+1]))
        # tempArray.insert(0, elapsedTimeCalculating(timeFormatting(startTime), tempClassNotiArray[0]))     수업시작부터 노티사이가 필요하다면.
        notiInterSessionDic[studentIndex].append(np.mean(tempArray))

#
#
# 전체학생 수업시간 Noti 평균 갯수 박스플롯 그리기
tempArray = []
for studentIndex, studentNotiCnt in notiCntDic.items():
    tempArray.append(np.mean(studentNotiCnt))
plt.boxplot(tempArray)
plt.show()

#
#
#
# 전체학생 수업시간 평균 Noti 인터세션 박스플롯 그리기
tempArray = []
for studentIndex, studentNotiInterSession in notiInterSessionDic.items():
    tempArray.append(np.mean(studentNotiInterSession))
plt.boxplot(tempArray)
plt.show()
