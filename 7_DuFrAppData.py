from pandas import DataFrame

from twicebursterDataMining.RH_Library import *
from Bunker.Marines import *
import matplotlib.pyplot as plt

#
#
# 학생별 앱들 간의 Duration, Frequency 의 비율 구하기
studentsClassApnoDurationDic, studentsClassApnoFrequencyDic = {}, {}
for studentIndex in range(0, 84):
    studentDataPath = getStudentDataPathing(studentIndex)
    print(studentDataPath)

    #
    #
    # 데이터 준비하기
    classApnoArray, stack = [], []
    for index, row in enumerate(sqlite3.connect(studentDataPath + "\\CLASSAPNODATABASE.db").execute("SELECT * FROM CLASSAPNOTABLE")):
        if row[2] == "RUNNING":
            stack.append(row)
        elif row[3] == "screenOff":
            startTime = 0
            endTime = row[1]
            while stack:
                startRow = stack.pop()
                startTime = startRow[1]
                classApnoArray.append([startRow[1], elapsedTimeCalculating(startTime, endTime), startRow[3]])
                endTime = startTime
    classApnoArray = sorted(classApnoArray, key=lambda low: low[0])

    #
    #
    # 사용시간, 사용횟수 추출하기
    deleteAppDic = {"com.lge.signboard":"", "com.lge.launcher2":"", "com.android.systemui":"", "com.lge.launcher3":"", "com.sec.android.app.launcher":"",
                    "com.buzzpia.aqua.launcher":"", "com.skp.launcher":"", "com.campmobile.launcher":"", "com.phone.launcher.android":"", "com.fihtdc.foxlauncher":"", "android":"",
                    "com.cashwalk.cashwalk":""}
    classApnoDurationDic, classApnoFrequencyDic = {}, {}
    for index, row in enumerate(classApnoArray):
        if ("lge.signboard" in row[2]) and (row[1] > 60):
            classApnoArray[index][2] = classApnoArray[index-1][2]

        if row[2] in deleteAppDic.keys():
            continue

        if row[2] in classApnoDurationDic.keys():
            classApnoDurationDic[row[2]] += row[1]
        else:
            classApnoDurationDic[row[2]] = row[1]

        if row[2] in classApnoFrequencyDic.keys():
            classApnoFrequencyDic[row[2]] += 1
        else:
            classApnoFrequencyDic[row[2]] = 1

    #
    #
    # 사용시간 앱별 비율 구하기
    tempSum = round(sum([row[1] for row in classApnoDurationDic.items()]), 3)
    temp = sorted([round(row[1] / tempSum, 3) for row in classApnoDurationDic.items() if round(row[1] / tempSum, 3) != 0])

    rowSum, temp2 = 0, []
    for row in temp:
        rowSum += row
        temp2.append(round(rowSum, 3))
    temp2[len(temp2) - 1] = 1

    studentsClassApnoDurationDic[studentIndex] = sorted(temp2, reverse=True)

    #
    #
    # 사용횟수 앱별 비율 구하기
    tempSum = round(sum([row[1] for row in classApnoFrequencyDic.items()]), 3)
    temp = sorted([round(row[1] / tempSum, 3) for row in classApnoFrequencyDic.items() if round(row[1] / tempSum, 3) != 0])

    rowSum, temp2 = 0, []
    for row in temp:
        rowSum += row
        temp2.append(round(rowSum, 3))
    temp2[len(temp2) - 1] = 1

    studentsClassApnoFrequencyDic[studentIndex] = sorted(temp2, reverse=True)

#
#
# 전체 사용시간, 사용횟수 그래프 그리기
# top10Color = ['#00B700', '#0BC904', '#1DDB16', '#41FF3A', '#53FF4C', '#65FF5E', '#77FF70', '#89FF82', '#9BFF94', '#ADFFA6']
# for studentIndex in range(0, 84):
#     for index, value in enumerate(studentsClassApnoDurationDic[studentIndex]):
#         if index <= 9:
#             plt.bar(studentIndex, value, color=top10Color[index])
#         else:
#             plt.bar(studentIndex, value)
#
# plt.xlabel("")
# plt.ylabel("Duration Ratio")
# plt.show()
#
# for studentIndex in range(0, 84):
#     for index, value in enumerate(studentsClassApnoFrequencyDic[studentIndex]):
#         if index <= 9:
#             plt.bar(studentIndex, value, color=top10Color[index])
#         else:
#             plt.bar(studentIndex, value)
#
# plt.xlabel("")
# plt.ylabel("Frequency Ratio")
# plt.show()
















