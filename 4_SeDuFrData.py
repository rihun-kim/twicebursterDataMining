from twicebursterDataMining.RH_Library import *
from Bunker.Marines import *
from pandas import DataFrame
import matplotlib.pyplot as plt
import numpy as np

#
#
# 수업시 Session, Duration, Frequency
studentsData = []
for studentIndex in range(0, 84):
    studentDataPath = getStudentDataPathing(studentIndex)
    print(studentDataPath)

    #
    #
    # 출석시간대 사용시간 준비하기
    classUsageArray = []
    for row in sqlite3.connect(studentDataPath + "\\CLASSUSAGEDATABASE.db").execute("SELECT * FROM CLASSUSAGETABLE"):
        classUsageArray.append(row)

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

    #
    #
    # Session, Duration, Frequency 평균값 구하기
    duration, frequency = 0, 0
    for index, row in enumerate(classUsageElapsedArray):
        duration += row[0]
        frequency += row[1]

    length = len(classUsageElapsedArray)
    studentsData.append([round(duration/frequency, 3), round(duration/length, 3), round(frequency/length, 3)])

#
#
#
# 전체 학생들의 수업시 Session, Duration, Frequency 박스플롯 그리기
# sessionTotal, durationTotal, frequencyTotal = [], [], []
# for row in studentsData:
#     sessionTotal.append(row[0])
#     durationTotal.append(row[1])
#     frequencyTotal.append(row[2])
#
# plt.figure(figsize=(4, 5))
# plt.boxplot(sessionTotal, labels=("session", ))
# plt.show()
#
# plt.boxplot(durationTotal)
# plt.show()
#
# plt.figure(figsize=(4, 5))
# plt.boxplot(frequencyTotal, labels=("frequency", ))
# plt.show()
#
# plt.scatter(sessionTotal, frequencyTotal)
# plt.show()

