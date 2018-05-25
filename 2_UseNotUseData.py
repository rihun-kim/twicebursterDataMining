from twicebursterDataMining.RH_Library import *
from Bunker.Marines import *
import matplotlib.pyplot as plt

#
#
# 수업시간 스마트폰 사용유무 검출하기
outClasses = ["프로그래밍기초", "일반물리학실험", "일반화학실헝", " 역사학특강", "사회과학특강", "영문학특강", "발상과 표현", "심리철학", "AdvancedEnglish", "빛,생명,그리고색체", "문제해결기법", "EnglishPresentation&Discussion"]
studentsData = []
for studentIndex in range(0, 84):
    studentDataPath = getStudentDataPathing(studentIndex)
    print(studentDataPath)

    #
    #
    # 출석시간 뽑아내기
    attendanceTimeArray = []
    for attendanceRow in sqlite3.connect(getDatabasePathing("ATTENDANCEDATABASE.db")).execute("SELECT * FROM ATTENDANCETABLE WHERE ID==" + "'" + getStudentID(studentIndex) + "'"):
        skip = False
        for cls in outClasses:
            if cls in attendanceRow[1]:
                skip = True
                break
        if not skip:
            for row in attendanceRow[2:]:
                if row == "":
                    continue
                attendanceTimeArray.append([attendanceRow[1], row.split("~")[0], row.split("~")[1]])

    #
    #
    # 출석시간대 사용시간 뽑아내기
    classUsageArray = []
    for className, entranceTime, exitTime in attendanceTimeArray:
        for usageRow in sqlite3.connect(studentDataPath + "\\USAGEDATABASE.db").execute("SELECT * FROM USAGETABLE WHERE '" + entranceTime + "' <= STARTTIME and ENDTIME <= '" + exitTime + "'"):
            classUsageArray.append([className, entranceTime, exitTime, usageRow[0], usageRow[1], usageRow[2], usageRow[3]])
    # CLASSUSAGEDATABASEMAKING(studentDataPath + "\\CLASSUSAGEDATABASE.db", classUsageArray)

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



