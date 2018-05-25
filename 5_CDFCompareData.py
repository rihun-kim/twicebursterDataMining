from twicebursterDataMining.RH_Library import *
from Bunker.Marines import *
import matplotlib.pyplot as plt

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