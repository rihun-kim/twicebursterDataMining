from twicebursterDataMining.RH_Library import *
from Bunker.Marines import *
import matplotlib.pyplot as plt

#
#
# 학생별 Top10 앱의 Duration, Frequency 엔트로피 값 구하기
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
    studentClassApnoDurationEntropyArray.append(entropy([valueArray[2] for valueArray in studentClassApnoDurationDic[getStudentID(studentIndex)]]))

    classApnoFrequencyArray = sorted(classApnoCountDic.items(), key=lambda row: row[1], reverse=True)
    studentClassApnoFrequencyDic[getStudentID(studentIndex)] = [(index + 1, row[0], row[1]) for index, row in enumerate(classApnoFrequencyArray) if index < 10]
    studentClassApnoFrequencyEntropyArray.append(entropy([valueArray[2] for valueArray in studentClassApnoFrequencyDic[getStudentID(studentIndex)]]))


#
#
# 엔트로피 박스플롯 그리기
plt.boxplot(studentClassApnoDurationEntropyArray)
plt.xlabel("")
plt.ylabel("Entropy of Duration")
plt.show()

plt.boxplot(studentClassApnoFrequencyEntropyArray)
plt.xlabel("")
plt.ylabel("Entropy of Frequency")
plt.show()












