import pandas as pd
import matplotlib.pyplot as plot
from scipy import stats, polyval
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from twicebursterDataMining.RH_Library import *

surveyData = pd.read_csv("C:\\Users\\rihun\\Dropbox (KAIST Dr.M)\\htdocs\\Hatchery\\EvolutionChamber\\POST SURVEY1.csv",
                         names=["FrequencyForClass", "SessionForClass","DICT","SEARCH","CLASSINFORM","CLASSMATERIAL","PHOTO","MEMO",
                                "FrequencyForNot","SessionForNot","MMS","SNS","EMAIL","WEB","TIME","GAME","WEBTOON"])

rawData = pd.read_csv("C:\\Users\\rihun\\Dropbox (KAIST Dr.M)\\htdocs\\Hatchery\\EvolutionChamber\\Data1.csv",
                      names=["Frequency", "Session", "Duration", "SessionAppNum", "Sex", "HighSchool", "UsageRatio",
                             "TOP10DurationEntropy", "TOP10FrequencyEntropy", "SAS", "SCORE","SCROLL","KEY","SHORT"])
LABEL_COLOR_MAP = {0: '#0054FF', 1: '#00D8FF', 2: '#1DDB16', 3: '#FFBB00', 4: '#000000'}



plt.scatter(rawData["SCROLL"], rawData["SAS"])
plt.show()



# X = np.array([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]] for row in
#               zip( rawData["SessionAppNum"], rawData["SAS"], rawData["SCORE"], rawData["SCROLL"], rawData["KEY"], rawData["SHORT"],
#                   rawData["TOP10DurationEntropy"], rawData["TOP10FrequencyEntropy"])])
# pca = PCA(n_components=8)
# pca.fit(X)
# Z = pca.transform(X)
# kmeans = KMeans(n_clusters=4).fit([[row1, row2] for row1, row2 in zip(Z[:, 0], Z[:, 1])])
# label_color = [LABEL_COLOR_MAP[l] for l in kmeans.labels_]
# plt.scatter(Z[:, 0], Z[:, 1], c=label_color)
# # PLOTING3D(Z[:, 0], Z[:, 1], Z[:, 2])
# # plt.scatter(Z[:, 0], [0 for row in range(0, len(Z))], s=9)
# plt.show()


















# label_color = [LABEL_COLOR_MAP[l] for l in rawData["HighSchool"]]

# label_color = []
# for row in rawData["SCORE"]:
#     if 0 <= row < 1:
#         label_color.append(LABEL_COLOR_MAP[0])
#     elif 1 <= row < 2:
#         label_color.append(LABEL_COLOR_MAP[1])
#     elif 2 <= row < 3:
#         label_color.append(LABEL_COLOR_MAP[2])
#     elif 3 <= row < 4:
#         label_color.append(LABEL_COLOR_MAP[3])
#     elif 4 <= row:
#         label_color.append(LABEL_COLOR_MAP[4])

# label_color = []
# for row in rawData["SAS"]:
#     if 10 <= row < 15:
#         label_color.append(LABEL_COLOR_MAP[0])
#     elif 15 <= row < 20:
#         label_color.append(LABEL_COLOR_MAP[1])
#     elif 25 <= row < 30:
#         label_color.append(LABEL_COLOR_MAP[2])
#     elif 30 <= row < 35:
#         label_color.append(LABEL_COLOR_MAP[3])
#     elif 4 <= row:
#         label_color.append(LABEL_COLOR_MAP[4])

# plot.scatter(rawData["SCROLL"], rawData["KEY"], color=label_color)
# plt.show()

# PLOTING3D(rawData["SCROLL"], rawData["KEY"], rawData["SHORT"])













# 인터렉션 상관관계
# plot.scatter(rawData["SCROLL"], rawData["SHORT"])
# slope, intercept, r, p, std = stats.linregress(rawData["SCROLL"], rawData["SHORT"])
# ry = polyval([slope, intercept], rawData["SCROLL"])
#
# print(slope, intercept, r, p, std)
# plt.plot(rawData["SCROLL"], rawData["SHORT"], 'k.')
# plt.plot(rawData["SCROLL"], ry, 'r.-')
# plot.show()










# PCA 분석
# rawData["Session"] = scaler.fit_transform([[row] for row in rawData["Session"]])
# rawData["Frequency"] = scaler.fit_transform([[row] for row in rawData["Frequency"]])
# rawData["SessionAppNum"] = scaler.fit_transform([[row] for row in rawData["SessionAppNum"]])
#
# X = np.array([[row[0], row[1], row[2], row[3]] for row in
#               zip(rawData["Frequency"], rawData["Session"],
#                   rawData["TOP10DurationEntropy"], rawData["TOP10FrequencyEntropy"])])
# pca = PCA(n_components=4)
# pca.fit(X)
# Z = pca.transform(X)
# plt.scatter(Z[:, 0], Z[:, 1], s=9)
# PLOTING3D(Z[:, 0], Z[:, 1], Z[:, 2])
# plt.scatter(Z[:, 0], [0 for row in range(0, len(Z))], s=9)
# plt.show()



# 설문데이터 뽑기
# dictlen = len([row for row in surveyData["DICT"] if row == 1.0])
# searchlen = len([row for row in surveyData["SEARCH"] if row == 1.0])
# classInformlen = len([row for row in surveyData["CLASSINFORM"] if row == 1.0])
# classmateriallen = len([row for row in surveyData["CLASSMATERIAL"] if row == 1.0])
# photolen = len([row for row in surveyData["PHOTO"] if row == 1.0])
# memolen = len([row for row in surveyData["MEMO"] if row == 1.0])
#
# mmslen = len([row for row in surveyData["MMS"] if row == 1.0])
# snslen = len([row for row in surveyData["SNS"] if row == 1.0])
# emaillen = len([row for row in surveyData["EMAIL"] if row == 1.0])
# weblen = len([row for row in surveyData["WEB"] if row == 1.0])
# timelen = len([row for row in surveyData["TIME"] if row == 1.0])
# gamelen = len([row for row in surveyData["GAME"] if row == 1.0])
# webtoonlen = len([row for row in surveyData["WEBTOON"] if row == 1.0])
#
# plt.bar(("dict", "search", "classMaterial", "classinform", "photo", "memo"),
#         (dictlen, searchlen, classmateriallen, classInformlen, photolen, memolen))
#
# plt.bar(("SNS", "WEB", "TIME", "WEBTOON", "MMS", "GAME", "EMAIL"),
#         (snslen, weblen, timelen, webtoonlen, mmslen, gamelen, emaillen))
# plt.show()



# #회귀분석
# plt.figure(figsize=(8, 8))
# # rawData = rawData[rawData.Frequency <= 22]
# slope, intercept, r, p, std = stats.linregress(rawData["TOP10DurationEntropy"], rawData["TOP10FrequencyEntropy"])
# ry = polyval([slope, intercept], rawData["TOP10DurationEntropy"])
#
# print(slope, intercept, r, p, std)
# plt.plot(rawData["TOP10DurationEntropy"], rawData["TOP10FrequencyEntropy"], 'k.')
# plt.plot(rawData["TOP10DurationEntropy"], ry, 'r.-')
# plt.title('regression')
# plt.xlabel("TOP10DurationEntropy")
# plt.ylabel("TOP10FrequencyEntropy")
# plt.show()


# # 티 테스트
# surveyFreArray = []
# exIndexList = []
# for index, row in enumerate(zip(surveyData["FrequencyForClass"], surveyData["FrequencyForNot"])):
#     surveyFreArray.append(row[0] + row[1])
#     if row[0] + row[1] < 40:
#         None
#     else:
#         exIndexList.append(index)
# for index, row in enumerate(rawData["Frequency"]):
#     if row < 23:
#         None
#     else:
#         exIndexList.append(index)
#
# A1 = [float(row) for index, row in enumerate(surveyFreArray) if index not in exIndexList]
# A2 = [round(row, 3) for index, row in enumerate(rawData["Frequency"]) if index not in exIndexList]
# tTestResult = stats.ttest_rel(A2, A1)
# print("The T-statistic is %.3f and the p-value is %.3f" % tTestResult)