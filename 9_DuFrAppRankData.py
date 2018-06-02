from pandas import DataFrame

from twicebursterDataMining.RH_Library import *
from Bunker.Marines import *

#
#
# 수업시간 스마트폰 앱 Duration, Frequency 앱 순위표
studentClassApnoDurationDic, studentClassApnoFrequencyDic = {}, {}
studentClassApnoDurationEntropyArray, studentClassApnoFrequencyEntropyArray = [], []
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
    classApnoTimeDic, classApnoCountDic = {}, {}
    for index, row in enumerate(classApnoArray):
        if ("lge.signboard" in row[2]) and (row[1] > 60):
            classApnoArray[index][2] = classApnoArray[index-1][2]

        if row[2] in deleteAppDic.keys():
            continue

        if row[2] in classApnoTimeDic.keys():
            classApnoTimeDic[row[2]] += row[1]
        else:
            classApnoTimeDic[row[2]] = row[1]

        if row[2] in classApnoCountDic.keys():
            classApnoCountDic[row[2]] += 1
        else:
            classApnoCountDic[row[2]] = 1

    classApnoDurationArray = sorted(classApnoTimeDic.items(), key=lambda row: row[1], reverse=True)
    studentClassApnoDurationDic[getStudentID(studentIndex)] = [(index + 1, row[0], round(row[1], 3)) for index, row in enumerate(classApnoDurationArray) if index < 10]

    classApnoFrequencyArray = sorted(classApnoCountDic.items(), key=lambda row: row[1], reverse=True)
    studentClassApnoFrequencyDic[getStudentID(studentIndex)] = [(index + 1, row[0], row[1]) for index, row in enumerate(classApnoFrequencyArray) if index < 10]

#
#
# Duration 순위표 그리기
rankDic = {}
for eachStudentClassApnoDurationDicArray in studentClassApnoDurationDic.values():
    for appRow in eachStudentClassApnoDurationDicArray:
        if appRow[1] not in rankDic.keys():
            rankDic[appRow[1]] = 1
        else:
            rankDic[appRow[1]] += 1

top10Cnt = 1
for name, count in sorted(rankDic.items(), key=lambda row:row[1], reverse=True):
    if top10Cnt == 11:
        break
    print(count, name)
    top10Cnt += 1

#
#
# Frequency 순위표 그리기
rankDic = {}
for eachStudentClassApnoFrequencyArray in studentClassApnoFrequencyDic.values():
    for appRow in eachStudentClassApnoFrequencyArray:
        if appRow[1] not in rankDic.keys():
            rankDic[appRow[1]] = 1
        else:
            rankDic[appRow[1]] += 1

top10Cnt = 1
for name, count in sorted(rankDic.items(), key=lambda row:row[1], reverse=True):
    if top10Cnt == 11:
        break
    print(count, name)
    top10Cnt += 1

#
#
# 사용시간, 사용횟수 Top10 앱 데이터 csv 로 출력하기
frame = DataFrame(studentClassApnoDurationDic)
frame.to_csv("C:\\Users\\rihun\Dropbox (KAIST Dr.M)\\htdocs\\Hatchery\\EvolutionChamber\\studentClassApnoTimeDic.csv")

frame = DataFrame(studentClassApnoFrequencyDic)
frame.to_csv("C:\\Users\\rihun\Dropbox (KAIST Dr.M)\\htdocs\\Hatchery\\EvolutionChamber\\studentClassApnoCountDic.csv")









