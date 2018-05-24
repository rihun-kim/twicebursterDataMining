from multiprocessing import Process

from twicebursterDataMining.RH_Library import *
from Bunker.Marines import *
import matplotlib.pyplot as plt
import numpy as np

#
#
# 학생수/신청과목수 그래프 그리기
clsCreditDic = {}
for row in sqlite3.connect(getDatabasePathing("SCHEDULEDATABASE.db")).execute("SELECT ID, CREDIT FROM SCHEDULETABLE"):
    clsCreditDic[row[0]] = row[1]

studentsDic = {}
for row in sqlite3.connect(getDatabasePathing("METADATABASE.db")).execute("SELECT ID, CLASSES FROM METATABLE"):
    clses = row[1].split("~")

    creditSum = 0
    for cls in clses:
        creditSum += int(clsCreditDic.get(cls))

    if creditSum in studentsDic.keys():
        studentsDic[creditSum] += 1
    else:
        studentsDic[creditSum] = 1

plt.bar(studentsDic.keys(), studentsDic.values())
plt.xticks(range(9, 25, 1))
plt.yticks(range(0, 20, 1))
plt.xlabel("Registered credits of classes")
plt.ylabel("Number of students")
plt.show()

#
#
# 학점/신청과목수 그래프 그리기
classes = []
for row in sqlite3.connect(getDatabasePathing("METADATABASE.db")).execute("SELECT * FROM METATABLE"):
    temp = row[5].split("~")
    for clss in temp:
        classes.append(clss)

classDic = {}
for row in sqlite3.connect(getDatabasePathing("SCHEDULEDATABASE.db")).execute("SELECT * FROM SCHEDULETABLE"):
    startTime = datetime.datetime.strptime(list(row)[4][3:8], "%H:%M")
    endTime = datetime.datetime.strptime(list(row)[4][12:], "%H:%M")
    classDic[row[0]] = str(endTime - startTime)

cntDic = {}
for row in classes:
    if classDic[row] in cntDic:
        cntDic[classDic[row]] += 1
    else:
        cntDic[classDic[row]] = 1

x_num = ["1;15:00", "1:45:00", "2:45:00", "3:00:00", "3:15:00"]
y_cnt = [353, 30, 59, 1, 2]
plt.bar(x_num, y_cnt)
plt.yticks(range(0, 360, 20))
plt.xlabel("Registered Classes' Time")
plt.ylabel("Number of students' class")
plt.show()

#############################

#
#
# 수업이외시 Duration, Frequency
studentsData = []
for studentIndex in range(0, 84):
    studentDataPath = getStudentDataPathing(studentIndex)
    print(studentDataPath)

    #
    #
    # 출석시간 뽑아내기
    attendanceTimeArray = []
    for attendanceRow in sqlite3.connect(getDatabasePathing("ATTENDANCEDATABASE.db")).execute("SELECT * FROM ATTENDANCETABLE WHERE ID==" + "'" + getStudentID(studentIndex) + "'"):
        for row in attendanceRow[2:]:
            if row == "":
                continue
            attendanceTimeArray.append([attendanceRow[1], row.split("~")[0], row.split("~")[1]])
    attendanceTimeArray = sorted(attendanceTimeArray, key=lambda row: row[1])

    #
    #
    # 출석시간대 빼고 사용시간 뽑아내기
    notAttendanceTimeArray = []
    for usageRow in sqlite3.connect(studentDataPath + "\\USAGEDATABASE.db").execute("SELECT * FROM USAGETABLE;"):
        SKIP = False
        for attendanceRow in attendanceTimeArray:
            if (attendanceRow[1] < usageRow[1]) and (usageRow[2] < attendanceRow[2]):
                SKIP = True
                break

        if not SKIP:
            notAttendanceTimeArray.append([getStudentID(studentIndex), usageRow[0], usageRow[1], usageRow[2], usageRow[3]])

    #
    #
    # notAttendanceTimeArray 데이터에서 요일별로 자르기
    day7UsageArray = [[], [], [], [], [], [], []]
    for row in notAttendanceTimeArray:
        if row[2][0:10] == row[3][0:10]:
            day7UsageArray[dayCalculating(row[2])].append([row[0], row[1], row[2], row[3], timeToSecFormating(row[4])])
        else:
            #1
            day7UsageArray[dayCalculating(row[2])].append([row[0], row[1], row[2], row[2][0:11]+"23.59.59.999", elapsedTimeCalculating(row[2], row[2][0:11]+"23.59.59.999")])
            #2
            day7UsageArray[dayCalculating(row[3])].append([row[0], row[1], row[3][0:11]+"00.00.00.000", row[3], elapsedTimeCalculating(row[3][0:11]+"00.00.00.000", row[3])])

    #
    #
    # Duration, Frequency 요일별로 평균값 계산하기
    duration, frequency = [], []
    for day1UsageArray in day7UsageArray:
        durationDic, frequencyDic = {}, {}
        for row in day1UsageArray:
            if row[2][:10] in durationDic.keys():
                durationDic[row[2][:10]] += row[4]
                frequencyDic[row[2][:10]] += 1
            else:
                durationDic[row[2][:10]] = row[4]
                frequencyDic[row[2][:10]] = 1

        durationSum = 0
        for row in durationDic.values():
            durationSum += row
        duration.append(round(durationSum/len(durationDic), 3))

        frequencySum = 0
        for row in frequencyDic.values():
            frequencySum += row
        frequency.append(round(frequencySum/len(frequencyDic), 3))

    #
    #
    # Duration, Frequency 주중, 주말, 전체 평균값 계산하기
    durationTotal, frequencyTotal, durationWeekend, frequencyWeekend = 0, 0, 0, 0
    for index in range(0, 7):
        durationTotal += duration[index]
        frequencyTotal += frequency[index]
        if index == 4:
            studentsData.append([getStudentID(studentIndex), 0, round(durationTotal / 5, 3), round(frequencyTotal / 5, 3)])
        elif index >= 5:
            durationWeekend += duration[index]
            frequencyWeekend += frequency[index]
    studentsData.append([getStudentID(studentIndex), 1, round(durationWeekend / 2, 3), round(frequencyWeekend / 2, 3)])
    studentsData.append([getStudentID(studentIndex), 2, round(durationTotal / 7, 3), round(frequencyTotal / 7, 3)])

#
#
#
# 전체 학생들의 수업이외시 Duration, Frequency 박스플롯 그리기
durationWeekdays, durationWeekend, durationTotal = [], [], []
frequencyWeekdays, frequencyWeekend, frequencyTotal = [], [], []
for row in studentsData:
    if row[1] == 0:
        durationWeekdays.append(row[2])
        frequencyWeekdays.append(row[3])
    elif row[1] == 1:
        durationWeekend.append(row[2])
        frequencyWeekend.append(row[3])
    else:
        durationTotal.append(row[2])
        frequencyTotal.append(row[3])

plt.boxplot((durationWeekdays, durationWeekend, durationTotal))
plt.show()

plt.boxplot((frequencyWeekdays, frequencyWeekend, frequencyTotal))
plt.show()

#############################

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

#############################

#
#
# 수업이외시, 수업시 세션비교
notClassUsageArray, classUsageArray = [], []
for studentIndex in range(0, 84):
    studentDataPath = getStudentDataPathing(studentIndex)
    print(studentDataPath)

    #
    #
    # 출석시간 뽑아내기
    attendanceTimeArray = []
    for attendanceRow in sqlite3.connect(getDatabasePathing("ATTENDANCEDATABASE.db")).execute("SELECT * FROM ATTENDANCETABLE WHERE ID==" + "'" + getStudentID(studentIndex) + "'"):
        for row in attendanceRow[2:]:
            if row == "":
                continue
            attendanceTimeArray.append([attendanceRow[1], row.split("~")[0], row.split("~")[1]])
    attendanceTimeArray = sorted(attendanceTimeArray, key=lambda row: row[1])

    #
    #
    # 출석시간대 빼고 사용시간 뽑아내기
    notAttendanceTimeArray = []
    for usageRow in sqlite3.connect(studentDataPath + "\\USAGEDATABASE.db").execute("SELECT * FROM USAGETABLE;"):
        SKIP = False
        for attendanceRow in attendanceTimeArray:
            if (attendanceRow[1] < usageRow[1]) and (usageRow[2] < attendanceRow[2]):
                SKIP = True
                break

        if not SKIP:
            notAttendanceTimeArray.append([getStudentID(studentIndex), usageRow[0], usageRow[1], usageRow[2], usageRow[3]])

    #
    #
    # 수업이외시, 수업시 데이터 준비하기
    for row in sqlite3.connect(studentDataPath + "\\CLASSUSAGEDATABASE.db").execute("SELECT ELAPSEDTIME FROM CLASSUSAGETABLE"):
        classUsageArray.append(timeToSecFormating(row[0]))

    for row in notAttendanceTimeArray:
        notClassUsageArray.append(timeToSecFormating(row[4]))

notClassUsageArray.sort()
classUsageArray.sort()

#
#
# 수업이외시, 수업시 CDF 플롯 그리기
counts, bin_edges = np.histogram(notClassUsageArray, bins=10000)
cdf = np.cumsum(counts)
plt.plot(bin_edges[1:], cdf/cdf[-1], '.b', markersize="2")

counts, bin_edges = np.histogram(classUsageArray, bins=1000)
cdf = np.cumsum(counts)
plt.plot(bin_edges[1:], cdf/cdf[-1], '.r', markersize="2")

plt.ylim(0, 1.0)
plt.show()

#############################

#
#
# 수업시 사용한 앱 사용내역 데이터베이스 만들기
def multiClassAPNO(startIndex, endIndex):
    for studentIndex in range(startIndex, endIndex):
        studentDataPath = getStudentDataPathing(studentIndex)
        print(studentDataPath)

        try:
            #
            #
            # 데이터 준비하기
            apnoUsageArray = []
            for row in sqlite3.connect(studentDataPath + "\\APNODATABASE.db").execute("SELECT TIMESTAMP, TYPE, PACKAGE FROM APNOTABLE"):
                apnoUsageArray.append(row)

            classUsageArray = []
            for row in sqlite3.connect(studentDataPath + "\\CLASSUSAGEDATABASE.db").execute("SELECT CLASSNAME, TYPE, STARTTIME, ENDTIME FROM CLASSUSAGETABLE"):
                classUsageArray.append(row)

            #
            #
            # 데이터 뽑아내기
            classApnoArray = []
            for index, classUsageRow in enumerate(classUsageArray):
                classUsageType, classUsageOnTime, classUsageOffTime = classUsageRow[1], classUsageRow[2], classUsageRow[3]

                if classUsageType == "screen":
                    runApnoIndex, runApnoArray = 0, []
                    touchAction, previousAppNeedy, usageOnTimeIndex = False, False, 0
                    for apnoUsageRowIndex, apnoUsageRow in enumerate(apnoUsageArray):
                        if classUsageOnTime <= apnoUsageRow[0] <= classUsageOffTime:
                            if apnoUsageRow[0] == classUsageOnTime and apnoUsageRow[2] == "screenOn":
                                runApnoArray.append([-1, apnoUsageRow[0], apnoUsageRow[1], apnoUsageRow[2]])
                                usageOnTimeIndex = apnoUsageRowIndex
                            elif apnoUsageRow[0] == classUsageOffTime and apnoUsageRow[2] == "screenOff":
                                runApnoArray.append([-1, apnoUsageRow[0], apnoUsageRow[1], apnoUsageRow[2]])
                                runApnoArray.insert(0, [classUsageType, touchAction, previousAppNeedy, usageOnTimeIndex])
                                break
                            elif apnoUsageRow[1] == "POSTED" or apnoUsageRow[1] == "REMOVED":
                                runApnoArray.append([-999, apnoUsageRow[0], apnoUsageRow[1], apnoUsageRow[2]])
                            elif apnoUsageRow[1] == "RUNNING":
                                runApnoIndex += 1
                                runApnoArray.append([runApnoIndex, apnoUsageRow[0], apnoUsageRow[1], apnoUsageRow[2]])
                            elif len(runApnoArray) != 0:
                                runApnoArray.append([runApnoIndex, apnoUsageRow[0], apnoUsageRow[1], apnoUsageRow[2]])
                                if not touchAction and ("TOUCH" in apnoUsageRow[1] or "KEY" in apnoUsageRow[1]):
                                    touchAction = True
                                if not previousAppNeedy and runApnoIndex == 0:
                                    previousAppNeedy = True

                    #
                    #
                    # 깡통버리기 및 이전에 사용하다가 화면만 끈 앱 찾기
                    if touchAction:
                        if previousAppNeedy:
                            for index in range(runApnoArray[0][3], 0, -1):
                                if apnoUsageArray[index][1] == "RUNNING":
                                    runApnoArray.insert(2, [0, runApnoArray[1][1], apnoUsageArray[index][1], apnoUsageArray[index][2]])
                                    break
                        if previousAppNeedy:
                            for row in runApnoArray:
                                if (row[0] != "screen") and (int(row[0]) >= 0):
                                    row[0] = int(row[0]) + 1
                                classApnoArray.append(row)
                        else:
                            for row in runApnoArray:
                                classApnoArray.append(row)

                elif classUsageType == "noti":
                    runApnoIndex, runApnoArray = 0, []
                    touchAction, previousAppNeedy, usageOnTimeIndex = False, False, 0
                    for apnoUsageRowIndex, apnoUsageRow in enumerate(apnoUsageArray):
                        if classUsageOnTime <= apnoUsageRow[0] <= classUsageOffTime:
                            if apnoUsageRow[0] == classUsageOnTime:
                                usageOnTimeIndex = apnoUsageRowIndex

                            if apnoUsageRow[0] == classUsageOffTime and apnoUsageRow[2] == "screenOff":
                                runApnoArray.append([-1, apnoUsageRow[0], apnoUsageRow[1], apnoUsageRow[2]])
                                runApnoArray.insert(0, [classUsageType, touchAction, previousAppNeedy, usageOnTimeIndex])
                                break
                            elif apnoUsageRow[1] == "POSTED" or apnoUsageRow[1] == "REMOVED":
                                runApnoArray.append([-999, apnoUsageRow[0], apnoUsageRow[1], apnoUsageRow[2]])
                            elif apnoUsageRow[1] == "RUNNING":
                                runApnoIndex += 1
                                runApnoArray.append([runApnoIndex, apnoUsageRow[0], apnoUsageRow[1], apnoUsageRow[2]])
                            else:
                                runApnoArray.append([runApnoIndex, apnoUsageRow[0], apnoUsageRow[1], apnoUsageRow[2]])
                                if not touchAction and ("TOUCH" in apnoUsageRow[1] or "KEY" in apnoUsageRow[1]):
                                    touchAction = True
                                if not previousAppNeedy and runApnoIndex == 0:
                                    previousAppNeedy = True

                    #
                    #
                    # 깡통버리기 및 노티로 시작한 앱 찾기
                    if touchAction:
                        if previousAppNeedy:
                            for index in range(runApnoArray[0][3], 0, -1):
                                if apnoUsageArray[index][1] == "RUNNING":
                                    runApnoArray.insert(1, [0, runApnoArray[1][1], apnoUsageArray[index][1], apnoUsageArray[index][2]])
                                    break
                        if previousAppNeedy:
                            for row in runApnoArray:
                                if (row[0] != "noti") and (int(row[0]) >= 0):
                                    row[0] = int(row[0]) + 1
                                classApnoArray.append(row)
                        else:
                            for row in runApnoArray:
                                classApnoArray.append(row)

            CLASSAPNODATABASEMAKING(studentDataPath + "\\CLASSAPNODATABASE.db", classApnoArray)
        except Exception as e:
            print("[ EXCEPTION ]" + studentDataPath)
            print(e.with_traceback(e))


if __name__ == '__main__':
    procs = []
    for index in range(0, 9):
        startIndex = 0 if index == 0 else index * 10
        endIndex = startIndex + 10 if index != 8 else startIndex + 4

        proc = Process(target=multiClassAPNO, args=(startIndex, endIndex))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()