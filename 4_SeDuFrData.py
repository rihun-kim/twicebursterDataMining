from pandas import DataFrame
from sklearn.decomposition import PCA

from twicebursterDataMining.RH_Library import *
from Bunker.Marines import *
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
# 전체 학생들의 수업시 Duration, Frequency 박스플롯 그리기
sessionTotal, durationTotal, frequencyTotal = [], [], []
for row in studentsData:
    sessionTotal.append(row[0])
    durationTotal.append(row[1])
    frequencyTotal.append(row[2])


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

# plt.scatter(sessionTotal, frequencyTotal)
# plt.show()

#
#
#
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# scaler = StandardScaler()
# sessionStandardTotal = scaler.fit_transform([[row] for row in sessionTotal])
# frequencyStandardTotal = scaler.fit_transform([[row] for row in frequencyTotal])
#
# sessionStandardTotal = [row[0] for row in sessionStandardTotal]
# frequencyStandardTotal = [row[0] for row in frequencyStandardTotal]
#
# plt.scatter(sessionStandardTotal, frequencyStandardTotal)
# plt.show()


# X = np.array([[row[0], row[1]] for row in zip(sessionTotal, frequencyTotal)])
# pca = PCA(n_components=2)
# pca.fit(X)
# Z = pca.transform(X)
#
# plt.scatter(Z[:,0], [0 for row in range(0, len(Z))], s=9)
# plt.show()



kmeans = KMeans(n_clusters=2).fit([[row1, row2] for row1, row2 in zip(sessionTotal, frequencyTotal)])
LABEL_COLOR_MAP = {0:'r', 1:'k', 2:'m', 3:'y', 4:'g'}
label_color = [LABEL_COLOR_MAP[l] for l in kmeans.labels_]




# fig = plt.figure()
# S = plt.scatter(sessionTotal, frequencyTotal, c=label_color)
# ax1 = fig.add_subplot(S)
# # plt.figure(figsize=(8, 8))
#
# plt.xlabel("session")
# plt.ylabel("frequency")
#
#
#
# # plt.figure(figsize=(8, 2))
# S = plt.boxplot(sessionTotal, vert=False)
# ax2 = fig.add_subplot(S)
# # plt.show()
#
# plt.figure(figsize=(2, 8))
# plt.boxplot(frequencyTotal)
# plt.show()
#
#
#
# plt.show()



