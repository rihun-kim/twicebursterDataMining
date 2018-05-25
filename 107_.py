from twicebursterDataMining.RH_Library import *
from Bunker.Marines import *

import matplotlib.pyplot as plt
from pandas import DataFrame

studentClassApnoTimeDic, studentClassApnoCountDic = {}, {}
studentClassApnoTimeEntropyArray, studentClassApnoCountEntropyArray = [], []
for studentIndex in range(0, 1):
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
                print(startRow)
            print("--------")
    classApnoArray = sorted(classApnoArray, key=lambda low: low[0])




    # #
    # #
    # # 사용시간, 사용횟수 추출하기
    # deleteAppDic = {"com.lge.signboard":"", "com.lge.launcher2":"", "com.android.systemui":"", "com.lge.launcher3":"", "com.sec.android.app.launcher":"",
    #                 "com.buzzpia.aqua.launcher":"", "com.skp.launcher":"", "com.campmobile.launcher":"", "com.phone.launcher.android":"", "com.fihtdc.foxlauncher":"", "android":""}
    # classApnoTimeDic, classApnoCountDic = {}, {}
    # for index, row in enumerate(classApnoArray):
    #     if ("lge.signboard" in row[2]) and (row[1] > 60):
    #         classApnoArray[index][2] = classApnoArray[index-1][2]
    #
    #     if row[2] in deleteAppDic.keys():
    #         continue
    #
    #     if row[2] in classApnoTimeDic.keys():
    #         classApnoTimeDic[row[2]] += row[1]
    #     else:
    #         classApnoTimeDic[row[2]] = row[1]
    #
    #     if row[2] in classApnoCountDic.keys():
    #         classApnoCountDic[row[2]] += 1
    #     else:
    #         classApnoCountDic[row[2]] = 1
    #
    # classApnoTimeArray = sorted(classApnoTimeDic.items(), key=lambda row: row[1], reverse=True)
    # studentClassApnoTimeDic[getStudentID(studentIndex)] = [(index+1, row[0], round(row[1], 3)) for index, row in enumerate(classApnoTimeArray) if index < 10]
    # studentClassApnoTimeEntropyArray.append(entropy([valueArray[2] for valueArray in studentClassApnoTimeDic[getStudentID(studentIndex)]]))
    #
    # classApnoCountArray = sorted(classApnoCountDic.items(), key=lambda row: row[1], reverse=True)
    # studentClassApnoCountDic[getStudentID(studentIndex)] = [(index+1, row[0], row[1]) for index, row in enumerate(classApnoCountArray) if index < 10]
    # studentClassApnoCountEntropyArray.append(entropy([valueArray[2] for valueArray in studentClassApnoCountDic[getStudentID(studentIndex)]]))



#
#
# 전체 사용시간, 사용횟수 그래프 그리기
# studentClassApnoTimeDicTotal = {}
# for eachStudentClassApnoTimeArray in studentClassApnoTimeDic.values():
#     for appArray in eachStudentClassApnoTimeArray:
#         if appArray[1] in studentClassApnoTimeDicTotal.keys():
#             studentClassApnoTimeDicTotal[appArray[1]] = round(studentClassApnoTimeDicTotal[appArray[1]] + appArray[2], 3)
#         else:
#             studentClassApnoTimeDicTotal[appArray[1]] = appArray[2]
# plt.plot()
# plt.bar(studentClassApnoTimeDicTotal.keys(), studentClassApnoTimeDicTotal.values())
# plt.xticks(fontsize=5, rotation=90)
# plt.tight_layout()
# plt.show()
#
# studentClassApnoCountDicTotal = {}
# for eachStudentClassApnoCountArray in studentClassApnoCountDic.values():
#     for appArray in eachStudentClassApnoCountArray:
#         if appArray[1] in studentClassApnoCountDicTotal.keys():
#             studentClassApnoCountDicTotal[appArray[1]] = round(studentClassApnoCountDicTotal[appArray[1]] + appArray[2], 3)
#         else:
#             studentClassApnoCountDicTotal[appArray[1]] = appArray[2]
# plt.plot()
# plt.bar(studentClassApnoCountDicTotal.keys(), studentClassApnoCountDicTotal.values())
# plt.xticks(fontsize=5, rotation=90)
# plt.tight_layout()
# plt.show()

#
#
# 사용시간, 사용횟수 Top10 앱 데이터 csv 로 출력하기
# frame = DataFrame(studentClassApnoTimeDic)
# frame.to_csv("C:\\Users\\rihun\Dropbox (KAIST Dr.M)\\htdocs\\Hatchery\\EvolutionChamber\\studentClassApnoTimeDic.csv")
#
# frame = DataFrame(studentClassApnoCountDic)
# frame.to_csv("C:\\Users\\rihun\Dropbox (KAIST Dr.M)\\htdocs\\Hatchery\\EvolutionChamber\\studentClassApnoCountDic.csv")

#
#
# 엔트로피 그래프 그리기
# plt.bar(range(0, 84), studentClassApnoTimeEntropyArray)
# plt.xlabel("Student ID")
# plt.ylabel("Entropy of Duration")
# plt.show()
#
# plt.bar(range(0, 84), studentClassApnoCountEntropyArray)
# plt.xlabel("Student ID")
# plt.ylabel("Entropy of Frequency")
# plt.show()












