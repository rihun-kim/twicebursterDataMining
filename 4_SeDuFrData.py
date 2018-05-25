from twicebursterDataMining.RH_Library import *
from Bunker.Marines import *
import matplotlib.pyplot as plt

#
#
# 수업시 Duration, Frequency
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
    # Duration, Frequency 구하기
    classUsageDic = {}
    for row in classUsageArray:
        if (row[0], row[1], row[2]) in classUsageDic.keys():
            classUsageDic[(row[0], row[1], row[2])].append(row[6])
        else:
            classUsageDic[(row[0], row[1], row[2])] = [row[6]]

    classUsageElapsedArray = []
    for elapsedArray in classUsageDic.values():
        elapsedSum = 0
        for elapsedRow in elapsedArray:
            elapsedSum += timeToSecFormating(elapsedRow)
        classUsageElapsedArray.append([round(elapsedSum, 3), len(elapsedArray)])

    duration, frequency = 0, 0
    for index, row in enumerate(classUsageElapsedArray):
        duration += row[0]
        frequency += row[1]

    studentsData.append([round(duration/len(classUsageElapsedArray), 3), round(frequency/len(classUsageElapsedArray), 3)])

#
#
#
# 전체 학생들의 수업시 Duration, Frequency 박스플롯 그리기
durationTotal, frequencyTotal = [], []
for row in studentsData:
    durationTotal.append(row[0])
    frequencyTotal.append(row[1])

plt.boxplot(durationTotal)
plt.show()

plt.boxplot(frequencyTotal)
plt.show()