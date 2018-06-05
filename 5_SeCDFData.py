from twicebursterDataMining.RH_Library import *
from Bunker.Marines import *
import matplotlib.pyplot as plt
import numpy as np

#
#
# 수업이외시, 수업시 세션비교
# notClassUsageArray, classUsageArray = [], []
# for studentIndex in range(0, 84):
#     studentDataPath = getStudentDataPathing(studentIndex)
#     print(studentDataPath)
#
#     #
#     #
#     # 출석시간 뽑아내기
#     attendanceTimeArray = []
#     for attendanceRow in sqlite3.connect(getDatabasePathing("ATTENDANCEDATABASE.db")).execute("SELECT * FROM ATTENDANCETABLE WHERE ID==" + "'" + getStudentID(studentIndex) + "'"):
#         for row in attendanceRow[2:]:
#             if row == "":
#                 continue
#             attendanceTimeArray.append([attendanceRow[1], row.split("~")[0], row.split("~")[1]])
#     attendanceTimeArray = sorted(attendanceTimeArray, key=lambda row: row[1])
#
#     #
#     #
#     # 출석시간대 빼고 사용시간 뽑아내기
#     notAttendanceTimeArray = []
#     for usageRow in sqlite3.connect(studentDataPath + "\\USAGEDATABASE.db").execute("SELECT * FROM USAGETABLE;"):
#         SKIP = False
#         for attendanceRow in attendanceTimeArray:
#             if (attendanceRow[1] < usageRow[1]) and (usageRow[2] < attendanceRow[2]):
#                 SKIP = True
#                 break
#
#         if not SKIP:
#             notAttendanceTimeArray.append([getStudentID(studentIndex), usageRow[0], usageRow[1], usageRow[2], usageRow[3]])
#
#     #
#     #
#     # 수업이외시, 수업시 데이터 준비하기
#     for row in sqlite3.connect(studentDataPath + "\\CLASSUSAGEDATABASE.db").execute("SELECT ELAPSEDTIME FROM CLASSUSAGETABLE"):
#         classUsageArray.append(timeToSecFormating(row[0]))
#
#     for row in notAttendanceTimeArray:
#         notClassUsageArray.append(timeToSecFormating(row[4]))
#
# notClassUsageArray.sort()
# classUsageArray.sort()
#
#
# 수업이외시, 수업시 CDF 플롯 그리기
# counts, bin_edges = np.histogram(notClassUsageArray, bins=10000)
# cdf = np.cumsum(counts)
# plt.plot(bin_edges[1:], cdf/cdf[-1], '.b', markersize="2")
#
# counts, bin_edges = np.histogram(classUsageArray, bins=1000)
# cdf = np.cumsum(counts)
# plt.plot(bin_edges[1:], cdf/cdf[-1], '.r', markersize="2")
#
# plt.ylim(0, 1.0)
# plt.show()

#
#
# 수업이외시, 수업시 인터세션 비교
notClassUsageArray, classUsageArray = [], []
for studentIndex in range(0, 1):
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
    for row in sqlite3.connect(studentDataPath + "\\CLASSUSAGEDATABASE.db").execute("SELECT * FROM CLASSUSAGETABLE"):
        classUsageArray.append(row)

    for row in notAttendanceTimeArray:
        notClassUsageArray.append(timeToSecFormating(row[4]))

    for row in classUsageArray:
        print(row)

# notClassUsageArray.sort()
# classUsageArray.sort()


# 수업이외시, 수업시 CDF 플롯 그리기
# counts, bin_edges = np.histogram(notClassUsageArray, bins=10000)
# cdf = np.cumsum(counts)
# plt.plot(bin_edges[1:], cdf/cdf[-1], '.b', markersize="2")
#
# counts, bin_edges = np.histogram(classUsageArray, bins=1000)
# cdf = np.cumsum(counts)
# plt.plot(bin_edges[1:], cdf/cdf[-1], '.r', markersize="2")
#
# plt.ylim(0, 1.0)
# plt.show()


# #
# #
# # 수업이외시 Session, Duration, Frequency 해당 데이터가 필요할 때 쓸 것
# studentsData = []
# for studentIndex in range(0, 84):
#     studentDataPath = getStudentDataPathing(studentIndex)
#     print(studentDataPath)
#
#     #
#     #
#     # 출석시간 뽑아내기
#     attendanceTimeArray = []
#     for attendanceRow in sqlite3.connect(getDatabasePathing("ATTENDANCEDATABASE.db")).execute("SELECT * FROM ATTENDANCETABLE WHERE ID==" + "'" + getStudentID(studentIndex) + "'"):
#         for row in attendanceRow[2:]:
#             if row == "":
#                 continue
#             attendanceTimeArray.append([attendanceRow[1], row.split("~")[0], row.split("~")[1]])
#     attendanceTimeArray = sorted(attendanceTimeArray, key=lambda row: row[1])
#
#     #
#     #
#     # 출석시간대 빼고 사용시간 뽑아내기
#     notAttendanceTimeArray = []
#     for usageRow in sqlite3.connect(studentDataPath + "\\USAGEDATABASE.db").execute("SELECT * FROM USAGETABLE;"):
#         SKIP = False
#         for attendanceRow in attendanceTimeArray:
#             if (attendanceRow[1] < usageRow[1]) and (usageRow[2] < attendanceRow[2]):
#                 SKIP = True
#                 break
#
#         if not SKIP:
#             notAttendanceTimeArray.append([getStudentID(studentIndex), usageRow[0], usageRow[1], usageRow[2], usageRow[3]])
#
#     #
#     #
#     # notAttendanceTimeArray 데이터에서 요일별로 자르기
#     day7UsageArray = [[], [], [], [], [], [], []]
#     for row in notAttendanceTimeArray:
#         if row[2][0:10] == row[3][0:10]:
#             day7UsageArray[dayCalculating(row[2])].append([row[0], row[1], row[2], row[3], timeToSecFormating(row[4])])
#         else:
#             #1
#             day7UsageArray[dayCalculating(row[2])].append([row[0], row[1], row[2], row[2][0:11]+"23.59.59.999", elapsedTimeCalculating(row[2], row[2][0:11]+"23.59.59.999")])
#             #2
#             day7UsageArray[dayCalculating(row[3])].append([row[0], row[1], row[3][0:11]+"00.00.00.000", row[3], elapsedTimeCalculating(row[3][0:11]+"00.00.00.000", row[3])])
#
#     #
#     #
#     # Session, Duration, Frequency 요일별로 평균값 계산하기
#     session, duration, frequency = [], [], []
#     for day1UsageArray in day7UsageArray:
#         session.append(np.mean([row[4] for row in day1UsageArray]))
#         durationDic, frequencyDic = {}, {}
#         for row in day1UsageArray:
#             if row[2][:10] in durationDic.keys():
#                 durationDic[row[2][:10]] += row[4]
#                 frequencyDic[row[2][:10]] += 1
#             else:
#                 durationDic[row[2][:10]] = row[4]
#                 frequencyDic[row[2][:10]] = 1
#
#         durationSum = 0
#         for row in durationDic.values():
#             durationSum += row
#         duration.append(round(durationSum/len(durationDic), 3))
#
#         frequencySum = 0
#         for row in frequencyDic.values():
#             frequencySum += row
#         frequency.append(round(frequencySum/len(frequencyDic), 3))
#
#     #
#     #
#     # Session, Duration, Frequency 주중, 주말, 전체 평균값 계산하기
#     sessionTotal, durationTotal, frequencyTotal, sessionWeekend, durationWeekend, frequencyWeekend = 0, 0, 0, 0, 0, 0
#     for index in range(0, 7):
#         sessionTotal += session[index]
#         durationTotal += duration[index]
#         frequencyTotal += frequency[index]
#         if index == 4:
#             studentsData.append([getStudentID(studentIndex), 0, round(sessionTotal / 5, 3), round(durationTotal / 5, 3), round(frequencyTotal / 5, 3)])
#         elif index >= 5:
#             sessionWeekend += session[index]
#             durationWeekend += duration[index]
#             frequencyWeekend += frequency[index]
#     studentsData.append([getStudentID(studentIndex), 1, round(sessionWeekend / 2, 3), round(durationWeekend / 2, 3), round(frequencyWeekend / 2, 3)])
#     studentsData.append([getStudentID(studentIndex), 2, round(sessionTotal / 7, 3), round(durationTotal / 7, 3), round(frequencyTotal / 7, 3)])
#
# #
# #
# #
# # 전체 학생들의 수업이외시 Session, Duration, Frequency 박스플롯 그리기
# sessionWeekdays, sessionWeekend, sessionTotal = [], [], []
# durationWeekdays, durationWeekend, durationTotal = [], [], []
# frequencyWeekdays, frequencyWeekend, frequencyTotal = [], [], []
# for row in studentsData:
#     if row[1] == 0:
#         sessionWeekdays.append(row[2])
#         durationWeekdays.append(row[3])
#         frequencyWeekdays.append(row[4])
#     elif row[1] == 1:
#         sessionWeekend.append(row[2])
#         durationWeekend.append(row[3])
#         frequencyWeekend.append(row[4])
#     else:
#         sessionTotal.append(row[2])
#         durationTotal.append(row[3])
#         frequencyTotal.append(row[4])
#
# plt.boxplot((sessionWeekdays, sessionWeekend, sessionTotal))
# plt.xlabel(("Session", "Weekdays", "Weekend", "Week"))
# plt.yticks(np.arange(0, np.max(sessionWeekend), 50))
# plt.show()
#
# plt.boxplot((durationWeekdays, durationWeekend, durationTotal))
# plt.xlabel(("Weekdays", "Weekend", "Week"))
# plt.show()
#
# plt.boxplot((frequencyWeekdays, frequencyWeekend, frequencyTotal))
# plt.xlabel(("Weekdays", "Weekend", "Week"))
# plt.show()

