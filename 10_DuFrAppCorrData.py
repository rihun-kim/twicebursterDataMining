from twicebursterDataMining.RH_Library import *
from Bunker.Marines import *
import matplotlib.pyplot as plt
from scipy import stats

#
#
# 수업시간 스마트폰 앱 Duration, Frequency 상관관계
studentsCorrArray = []
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

    classApnoDurationArray1 = sorted(classApnoDurationDic.items(), key=lambda row: row[1], reverse=True)
    classApnoDurationArray2 = [(index + 1, row[0], round(row[1], 3)) for index, row in enumerate(classApnoDurationArray1) if index < 10]

    classApnoFrequencyArray1 = sorted(classApnoFrequencyDic.items(), key=lambda row: row[1], reverse=True)
    classApnoFrequencyArray2 = [(index + 1, row[0], round(row[1], 3)) for index, row in enumerate(classApnoFrequencyArray1) if index < 10]

    corrDic = {}
    for row in classApnoDurationArray2:
        corrDic[row[1]] = []
    for row in classApnoFrequencyArray2:
        corrDic[row[1]] = []
    for key in corrDic.keys():
        corrDic[key] = [round(classApnoDurationDic[key], 3), classApnoFrequencyDic[key]]
        studentsCorrArray.append([round(classApnoDurationDic[key], 3), classApnoFrequencyDic[key]])

#
#
# 상관관계 그래프 그리기
duration = [row[0] for row in studentsCorrArray]
frequency = [row[1] for row in studentsCorrArray]

slope, intercept, r_value, p_value, stderr = stats.linregress(frequency, duration)

print(slope)

plt.scatter(frequency, duration, s=3)
plt.show()








