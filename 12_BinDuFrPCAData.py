from pandas import DataFrame

from twicebursterDataMining.RH_Library import *
from Bunker.Marines import *

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
# 전체학생 Bin 평균의 Duration, Frequency 박스플롯
studentsDataAppBinDic = {}
studentsDataDurationDic, studentsFrequencyDic = {}, {}
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
    # 수업 시작시간 뽑아내기
    classStartTimeDic = {}
    for attendanceRow in attendanceTimeArray:
        firstClassTime = class75MDic[attendanceRow[0]][0]
        startTime = attendanceRow[1][0:11] + firstClassTime[3:5] + "." + firstClassTime[6:8] + ".00.000"

        if attendanceRow[0] in classStartTimeDic.keys():
            classStartTimeDic[attendanceRow[0]].append(startTime)
        else:
            classStartTimeDic[attendanceRow[0]] = [startTime]

    #
    #
    # 앱 Bin 데이터 추출하기
    apnoArray, appBinArray = [], []
    deleteAppDic = {"com.lge.signboard": "", "com.lge.launcher2": "", "com.android.systemui": "", "com.lge.launcher3": "", "com.sec.android.app.launcher": "",
                    "com.buzzpia.aqua.launcher": "", "com.skp.launcher": "", "com.campmobile.launcher": "", "com.phone.launcher.android": "", "com.fihtdc.foxlauncher": "", "android": "",
                    "com.cashwalk.cashwalk": ""}
    for timeStamp, type, package in sqlite3.connect(studentDataPath + "\\CLASSAPNODATABASE.db").execute("SELECT TIMESTAMP, TYPE, PACKAGE FROM CLASSAPNOTABLE WHERE TYPE=='RUNNING'"):
        if package not in deleteAppDic:
            apnoArray.append([timeStamp, type, package])

    for className, exitTime in sqlite3.connect(studentDataPath + "\\CLASSUSAGEDATABASE.db").execute("SELECT CLASSNAME, EXITTIME FROM CLASSUSAGETABLE"):
        for classStartTime in classStartTimeDic[className]:
            for index, apnoRow in enumerate(apnoArray):
                if classStartTime[:10] == apnoRow[0][:10] == exitTime[:10] and classStartTime[12:] < apnoRow[0][12:] <= exitTime[12:]:
                    appBinArray.append([elapsedTimeCalculating(classStartTime, apnoRow[0]), apnoRow[2]])
                    del(apnoArray[index])
                    break

    binDic = {}
    for binTimeStamp, binName in appBinArray:
        for binIndex in range(0, 15):
            if binIndex * 300 <= binTimeStamp <= (binIndex + 1) * 300:
                if binIndex in binDic.keys():
                    if binName in binDic[binIndex].keys():
                        binDic[binIndex][binName] += 1
                        break
                    else:
                        binDic[binIndex][binName] = 1
                else:
                    binDic[binIndex] = {binName : 1}
                    break

    tempArray = []
    for key, values in binDic.items():
        cnt = 0
        for index, row in enumerate(sorted(values.items(), key=lambda row : row[1], reverse=True)):
            if index == 3:
                break
            tempArray.append([key, row])
            cnt += 1
        for i in range(cnt, 4):
            tempArray.append([key, ("", "")])
    studentsDataAppBinDic[studentIndex] = sorted(tempArray, key=lambda row : row[0])

    #
    #
    # Duration, Frequency Bin 데이터 추출하기
    # binArray, classNum = [], []
    # for className, usingStartTime, usingEndTime in sqlite3.connect(studentDataPath + "\\CLASSUSAGEDATABASE.db").execute("SELECT CLASSNAME, STARTTIME, ENDTIME FROM CLASSUSAGETABLE"):
    #     for classStartTime in classStartTimeDic[className]:
    #         if usingStartTime[:10] == classStartTime[:10]:
    #             binArray.append([elapsedTimeCalculating(classStartTime, usingStartTime), elapsedTimeCalculating(classStartTime, usingEndTime)])
    #             classNum.append(classStartTime)
    # classNum = len(set(classNum))

    # binDic = {}
    # for binStartTime, binEndTime in binArray:
    #     tempDic = {}
    #     for sec in range(int(binStartTime), int(binEndTime) + 1):
    #         for binIndex in range(0, 15):
    #             if binIndex * 300 <= sec <= (binIndex + 1) * 300:
    #                 if binIndex in tempDic.keys():
    #                     tempDic[binIndex] = tempDic[binIndex] + 1
    #                 else:
    #                     tempDic[binIndex] = 1
    #     for row in tempDic.items():
    #         if row[0] in binDic.keys():
    #             binDic[row[0]].append(row[1])
    #         else:
    #             binDic[row[0]] = [row[1]]
    #
    # for binIndex, binArray in sorted(binDic.items(), key=lambda row: row[0]):
    #     if binIndex in studentsDataDurationDic.keys():
    #         studentsDataDurationDic[binIndex].append(round(sum(binArray) / len(binArray), 3))
    #         studentsFrequencyDic[binIndex].append(len(binArray) / classNum)
    #     else:
    #         studentsDataDurationDic[binIndex] = [round(sum(binArray) / len(binArray), 3)]
    #         studentsFrequencyDic[binIndex] = [len(binArray) / classNum]


#
#
#
frame = DataFrame(studentsDataAppBinDic)
frame.to_csv("C:\\Users\\rihun\Dropbox (KAIST Dr.M)\\htdocs\\Hatchery\\EvolutionChamber\\AppBin.csv")


#
#
# 전체학생 Duration 박스플롯 그리기
# plt.boxplot([bin for bin in studentsDataDurationDic.values()])
# plt.show()

#
#
# 전체학생 Frequency 박스플롯, 꺾은선 그리기
# plt.boxplot([bin for bin in studentsFrequencyDic.values()])
# plt.show()
#
# plt.plot([bin for bin in studentsFrequencyDic.values()], linewidth=0.5)
# plt.xticks(range(0, 15, 1))
# plt.show()

#
#
# 사용시간, 사용횟수 bin 데이터 csv 로 출력하기
# frame = DataFrame(studentsDataDurationDic)
# frame.to_csv("C:\\Users\\rihun\Dropbox (KAIST Dr.M)\\htdocs\\Hatchery\\EvolutionChamber\\studentBinDurationDic.csv")
#
# frame = DataFrame(studentsFrequencyDic)
# frame.to_csv("C:\\Users\\rihun\Dropbox (KAIST Dr.M)\\htdocs\\Hatchery\\EvolutionChamber\\studentBinFrequencyDic.csv")






































