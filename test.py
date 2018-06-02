import pandas as pd
import matplotlib.pyplot as plot
from pandas.plotting import scatter_matrix
from scipy import stats, polyval, spatial
import numpy as np
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, minmax_scale, normalize, scale

from twicebursterDataMining.wx import LABEL_COLOR_MAP
from twicebursterDataMining.RH_Library import *



surveyData = pd.read_csv("C:\\Users\\rihun\\Dropbox (KAIST Dr.M)\\htdocs\\Hatchery\\EvolutionChamber\\POST SURVEY1.csv",
                         names=["FrequencyForClass", "SessionForClass", "DICT", "SEARCH", "CLASSINFORM", "CLASSMATERIAL", "PHOTO", "MEMO", "FrequencyForNot",
                                "SessionForNot", "MMS", "SNS", "EMAIL", "WEB", "TIME", "GAME", "WEBTOON"])

rawData = pd.read_csv("C:\\Users\\rihun\\Dropbox (KAIST Dr.M)\\htdocs\\Hatchery\\EvolutionChamber\\Data1.csv",
                      names=["Frequency", "Session", "Duration", "SessionAppNum", "Sex", "HighSchool", "UsageRatio",
                             "TOP10DurationEntropy", "TOP10FrequencyEntropy", "SAS", "SCORE", "SCROLL", "KEY", "SHORT", "SILENT", "VIBRATE", "NORMAL", "LATE"])

binDurationData = pd.read_csv("C:\\Users\\rihun\\Dropbox (KAIST Dr.M)\\htdocs\\Hatchery\\EvolutionChamber\\studentBinDurationDic.csv",
                      names=["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10", "B11", "B12", "B13", "B14", "B15"])

binFrequencyData = pd.read_csv("C:\\Users\\rihun\\Dropbox (KAIST Dr.M)\\htdocs\\Hatchery\\EvolutionChamber\\studentBinFrequencyDic.csv",
                      names=["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10", "B11", "B12", "B13", "B14", "B15"])


# plt.scatter(rawData["LATE"], rawData["SessionAppNum"])
# plt.show()


from matplotlib import pyplot as plt
import pandas as pd
import sklearn.datasets
from sklearn.metrics import roc_curve, auc
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB

# CLASS_MAP = {
#     "LogisticReg" : ('-', LogisticRegression()),
#     "GaussianNB" : ("--", GaussianNB()),
#     "DecisionTree" : (".-", DecisionTreeClassifier(max_depth=5)),
#     "RandomForest" : (":", RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1))
# }
#
# Y = (rawData["SAS"] >= 30)
# X = rawData[["SCROLL", "KEY"]]
#
# X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.7)
# for name, (line_fmt, model) in CLASS_MAP.items():
#     model.fit(X_train, Y_train)
#     preds = model.predict_proba(X_test)
#     pred = pd.Series(preds[:, 1])
#     fpr, tpr, thresholds = roc_curve(Y_test, pred)
#     auc_score = auc(fpr, tpr)
#     label = "%s : auc = %f" % (name, auc_score)
#     plt.plot(fpr, tpr, line_fmt, linewidth=3, label=label)
#
# plt.plot([0,1], [0,1], "--")
# plt.xlim([0.0, 1.0])
# plt.ylim([0.0, 1.0])
# plt.legend(loc="lower right")
# plt.title("Compare")
# plt.xlabel("Recall")
# plt.ylabel("Precision")
# plt.show()


#
# ds = sklearn.datasets.load_iris()
# df = pd.DataFrame(ds["data"], columns=ds["feature_names"])
# code_species_map = dict(zip(range(3), ds["target_names"]))
# df["species"] = [code_species_map[c] for c in ds["target"]]
# X, Y = df[df.columns[:3]], (df["species"] == "virginica")
# X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = .8)
# print(Y_train)
#
# for name, (line_fmt, model) in CLASS_MAP.items():
#     model.fit(X_train, Y_train)
#     preds = model.predict_proba(X_test)
#     pred = pd.Series(preds[:,1])
#     fpr, tpr, thresholds = roc_curve(Y_test, pred)
#     auc_score = auc(fpr, tpr)
#     label = "%s : auc = %f" % (name, auc_score)
#     plt.plot(fpr, tpr, line_fmt, linewidth=5, label=label)
#
# plt.legend(loc="lower right")
# plt.title("Compare")
#
# plt.plot([0, 1], [0, 1], "--")
# plt.xlim([0.0, 1.0])
# plt.ylim([0.0, 1.05])
# plt.xlabel("Recall")
# plt.ylabel("Precision")
# plt.show()


























# # plt.scatter(rawData["SILENT"], rawData["Frequency"])
# df = pd.DataFrame(rawData["VIBRATE"])
# df["SCROLL"] = rawData["SCROLL"]
# # res.plot(x="SILENT", y="Frequency", kind="scatter", logx=True)
#
# scale = StandardScaler()
# scale.fit(df[["VIBRATE", "SCROLL"]])
# scaled_X = scale.transform(df[["VIBRATE", "SCROLL"]])
#
# df["scaled_x"] = scaled_X[:,0]
# df["scaled_y"] = scaled_X[:,1]

#DBSCAN
# from sklearn.cluster import DBSCAN
# dbscan = DBSCAN(eps=0.5, min_samples=5) #기본값이다.
# cluster = dbscan.fit_predict(scaled_X)
# df["cluster"] = cluster
#
# #clustering 결과 확인
# plt.scatter(x=df.scaled_x, y=df.scaled_y, c=df.cluster)
# plt.xlabel("x")
# plt.ylabel("y")
#
# plt.show()




# df = pd.DataFrame(X, columns=["x", "y"])
#
# kmeans = KMeans(n_clusters=4).fit([[row1, row2] for row1, row2 in zip(rawData["SILENT"], binFrequencyData["B1"])])
# label_color = [LABEL_COLOR_MAP[l] for l in kmeans.labels_]
# plt.scatter(rawData["SILENT"], binFrequencyData["B1"], c=label_color)
# plt.show()










# Frequency 각 빈
# binSlope = []
# for i in range(1, 15):
#     # print("B" + str(i), "B" + str(i + 1))
#     binSlope.append(round(binFrequencyData["B"+str(i)].corr(binFrequencyData["B"+str(i+1)]), 3))
#
# binSlope.insert(5, 0.92)
# print(binSlope)
# plt.plot(range(1, 16), binSlope, c='r')
# plt.xticks(range(1, 16, 1))
#
# plt.show()
#
# binSTD = []
# for binIndex in binFrequencyData:
#     binSTD.append(round(binFrequencyData[binIndex].std(), 3))
#
# plt.plot(range(1, 16), binSTD, c='b')
# plt.xticks(range(1, 16, 1))
#
# plt.show()
#
# # # Duration 각 빈
# binSlope = []
# for i in range(1, 15):
#     # print("B" + str(i), "B" + str(i + 1))
#     binSlope.append(round(binDurationData["B"+str(i)].corr(binDurationData["B"+str(i+1)]), 3))
#
# binSlope.insert(5, 0.87)
# print(binSlope)
# plt.plot(range(1, 16), binSlope, c='r')
# plt.xticks(range(1, 16, 1))
# # plt.ylim(0, 1)
# plt.show()
#
# binSTD = []
# for binIndex in binDurationData:
#     binSTD.append(round(binDurationData[binIndex].std(), 3))
#
# plt.plot(range(1, 16), binSTD, c='b')
# plt.xticks(range(1, 16, 1))
#
# plt.show()




# binSTD = []
# for binIndex in binFrequencyData:
#     binSTD.append(round(binFrequencyData[binIndex].std(), 3))
# #
# # print(binSTD)
# # print(minmax_scale(binSTD))
#
# plt.plot(range(1, 16), binSlope, c='r')
# plt.plot(range(1, 16), binSTD, c='b')
# plt.xticks(range(1, 16, 1))
# plt.ylim(0, 1)
# plt.show()









# # 각 빈과 그 다음빈간의 의 기울기값
# binSlope = []
# for i in range(1, 15):
#     # print("B" + str(i), "B" + str(i + 1))
#     binSlope.append(round(binDurationData["B"+str(i)].corr(binDurationData["B"+str(i+1)]), 3))
#
# binSlope.insert(5, 0.87)
# print(minmax_scale(binSlope))
#
# binSTD = []
# for binIndex in binDurationData:
#     binSTD.append(round(binDurationData[binIndex].std()))
#
# print(minmax_scale(binSTD))
#
# plt.plot(range(1, 16), minmax_scale(binSlope), c='r')
# plt.plot(range(1, 16), minmax_scale(binSTD), c='b')
# plt.xticks(range(1, 16 ,1))
# plt.show()

# X = np.array([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14]] for row in
#               zip(binFrequencyData["B1"], binFrequencyData["B2"], binFrequencyData["B3"], binFrequencyData["B4"], binFrequencyData["B5"],
#                   binFrequencyData["B6"], binFrequencyData["B7"], binFrequencyData["B8"], binFrequencyData["B9"], binFrequencyData["B10"],
#                   binFrequencyData["B11"], binFrequencyData["B12"], binFrequencyData["B13"], binFrequencyData["B14"], binFrequencyData["B15"])])
# pca = PCA(n_components=15)
# pca.fit(X)
# Z = pca.transform(X)

# print(Z[0])

# kmeans = KMeans(n_clusters=2).fit([[row1, row2] for row1, row2 in zip(Z[:, 0], Z[:, 1])])
#
# print(binData["B1"], binData["B2"])
#
# label_color = [LABEL_COLOR_MAP[l] for l in kmeans.labels_]
# plt.scatter(Z[1:, 0], Z[1:, 1])
# PLOTING3D(Z[:, 0], Z[:, 1], Z[:, 2])
# plt.scatter(Z[:, 1], [0 for row in range(0, len(Z))], s=9)
# plt.show()


# # studentsData = []
# binData = binFrequencyData
# # print(binData)
#
# # for index in range(0, 84):
# #     studentsData.append([row for row in binData[index]])
#
# # for index, row in enumerate(studentsData):
# #     print(np.mean(row))
#
# # print(studentsData)
# #
# # X = sorted(studentsData, key=lambda row: np.mean(row))
# # plt.boxplot([x for x in X])
# # plt.show()
#
# studentData = []
# for binIndex in binData:
#     tempDic = {}
#     for row in binFrequencyData[binIndex]:
#         tempDic[row] = 0
#     tempArray = sorted(binFrequencyData[binIndex])
#     for index, row in enumerate(tempArray):
#         tempDic[row] = index+1
#     studentData.append([row for row in tempDic.values()])
#
# # for row in studentData:
# #     print(row)
#
# X = np.array(studentData).T
# X = sorted(X, key=lambda row: np.mean(row))
# plt.boxplot([x for x in X])
# plt.show()





# # 빈 데이터 그리기
# binData = binFrequencyData
# startXlim, endXlim = 0, 4
# startYlim, endYlim = 0, 4
#
# fig = plt.figure()
#
# ax1 = fig.add_subplot(3, 5, 1);     ax2 = fig.add_subplot(3, 5, 2);     ax3 = fig.add_subplot(3, 5, 3);     ax4 = fig.add_subplot(3, 5, 4);     ax5 = fig.add_subplot(3, 5, 5);
# ax6 = fig.add_subplot(3, 5, 6);     ax7 = fig.add_subplot(3, 5, 7);     ax8 = fig.add_subplot(3, 5, 8);     ax9 = fig.add_subplot(3, 5, 9);     ax10 = fig.add_subplot(3, 5, 10);
# ax11 = fig.add_subplot(3, 5, 11);   ax12 = fig.add_subplot(3, 5, 12);   ax13 = fig.add_subplot(3, 5, 13);   ax14 = fig.add_subplot(3, 5, 14);   ax15 = fig.add_subplot(3, 5, 15);
#
# ax1.yaxis.set_label_position("right");      ax2.yaxis.set_label_position("right");      ax3.yaxis.set_label_position("right");      ax4.yaxis.set_label_position("right")
# ax5.yaxis.set_label_position("right");      ax5.yaxis.set_label_position("right");      ax6.yaxis.set_label_position("right");      ax7.yaxis.set_label_position("right");
# ax8.yaxis.set_label_position("right");      ax9.yaxis.set_label_position("right");      ax10.yaxis.set_label_position("right");     ax11.yaxis.set_label_position("right");
# ax12.yaxis.set_label_position("right");     ax13.yaxis.set_label_position("right");     ax14.yaxis.set_label_position("right");     ax15.yaxis.set_label_position("right");
#
# ax1.scatter(binData["B1"], binData["B2"], s=1);     ax1.set_xlabel('0-5');      ax1.set_ylabel('5-10');     ax1.set_xlim(startXlim, endXlim);       ax1.set_ylim(startYlim, endYlim);
# slope, intercept, r, p, std = stats.linregress(binData["B1"], binData["B2"])
# ry = polyval([slope, intercept], binData["B1"])
# ax1.plot(binData["B1"], ry, 'r.-', linewidth=0.5, markersize=0.5)
#
# ax2.scatter(binData["B2"], binData["B3"], s=1);     ax2.set_xlabel('5-10');     ax2.set_ylabel('10-15');    ax2.set_xlim(startXlim, endXlim);       ax2.set_ylim(startYlim, endYlim);
# slope, intercept, r, p, std = stats.linregress(binData["B2"], binData["B3"])
# ry = polyval([slope, intercept], binData["B2"])
# ax2.plot(binData["B2"], ry, 'r.-', linewidth=0.5, markersize=0.5)
#
# ax3.scatter(binData["B3"], binData["B4"], s=1);     ax3.set_xlabel('10-15');    ax3.set_ylabel('15-20');    ax3.set_xlim(startXlim, endXlim);       ax3.set_ylim(startYlim, endYlim);
# slope, intercept, r, p, std = stats.linregress(binData["B3"], binData["B4"])
# ry = polyval([slope, intercept], binData["B3"])
# ax3.plot(binData["B3"], ry, 'r.-', linewidth=0.5, markersize=0.5)
#
# ax4.scatter(binData["B4"], binData["B5"], s=1);     ax4.set_xlabel('15-20');    ax4.set_ylabel('20-25');    ax4.set_xlim(startXlim, endXlim);       ax4.set_ylim(startYlim, endYlim);
# slope, intercept, r, p, std = stats.linregress(binData["B4"], binData["B5"])
# ry = polyval([slope, intercept], binData["B4"])
# ax4.plot(binData["B4"], ry, 'r.-', linewidth=0.5, markersize=0.5)
#
# ax5.scatter(binData["B5"], binData["B6"], s=1);     ax5.set_xlabel('20-25');    ax5.set_ylabel('25-30');    ax5.set_xlim(startXlim, endXlim);       ax5.set_ylim(startYlim, endYlim);
# slope, intercept, r, p, std = stats.linregress(binData["B5"], binData["B6"])
# ry = polyval([slope, intercept], binData["B5"])
# ax5.plot(binData["B5"], ry, 'r.-', linewidth=0.5, markersize=0.5)
#
# ax6.scatter(binData["B6"], binData["B7"], s=1);     ax6.set_xlabel('25-30');    ax6.set_ylabel('30-35');    ax6.set_xlim(startXlim, endXlim);       ax6.set_ylim(startYlim, endYlim);
# slope, intercept, r, p, std = stats.linregress(binData["B6"], binData["B7"])
# ry = polyval([slope, intercept], binData["B6"])
# ax6.plot(binData["B6"], ry, 'r.-', linewidth=0.5, markersize=0.5)
#
# ax7.scatter(binData["B7"], binData["B8"], s=1);     ax7.set_xlabel('30-35');    ax7.set_ylabel('35-40');    ax7.set_xlim(startXlim, endXlim);       ax7.set_ylim(startYlim, endYlim);
# slope, intercept, r, p, std = stats.linregress(binData["B7"], binData["B8"])
# ry = polyval([slope, intercept], binData["B7"])
# ax7.plot(binData["B7"], ry, 'r.-', linewidth=0.5, markersize=0.5)
#
# ax8.scatter(binData["B8"], binData["B9"], s=1);     ax8.set_xlabel('35-40');    ax8.set_ylabel('40-45');    ax8.set_xlim(startXlim, endXlim);       ax8.set_ylim(startYlim, endYlim);
# slope, intercept, r, p, std = stats.linregress(binData["B8"], binData["B9"])
# ry = polyval([slope, intercept], binData["B8"])
# ax8.plot(binData["B8"], ry, 'r.-', linewidth=0.5, markersize=0.5)
#
# ax9.scatter(binData["B9"], binData["B10"], s=1);    ax9.set_xlabel('40-45');    ax9.set_ylabel('50-55');    ax9.set_xlim(startXlim, endXlim);       ax9.set_ylim(startYlim, endYlim);
# slope, intercept, r, p, std = stats.linregress(binData["B9"], binData["B10"])
# ry = polyval([slope, intercept], binData["B9"])
# ax9.plot(binData["B9"], ry, 'r.-', linewidth=0.5, markersize=0.5)
#
# ax10.scatter(binData["B10"], binData["B11"], s=1);  ax10.set_xlabel('45-50');   ax10.set_ylabel('50-55');   ax10.set_xlim(startXlim, endXlim);      ax10.set_ylim(startYlim, endYlim);
# slope, intercept, r, p, std = stats.linregress(binData["B10"], binData["B11"])
# ry = polyval([slope, intercept], binData["B10"])
# ax10.plot(binData["B10"], ry, 'r.-', linewidth=0.5, markersize=0.5)
#
# ax11.scatter(binData["B11"], binData["B12"], s=1);   ax11.set_xlabel('50-55');   ax11.set_ylabel('55-60');   ax11.set_xlim(startXlim, endXlim);  ax11.set_ylim(startYlim, endYlim);
# slope, intercept, r, p, std = stats.linregress(binData["B11"], binData["B12"])
# ry = polyval([slope, intercept], binData["B11"])
# ax11.plot(binData["B11"], ry, 'r.-', linewidth=0.5, markersize=0.5)
#
# ax12.scatter(binData["B12"], binData["B13"], s=1);  ax12.set_xlabel('55-60');   ax12.set_ylabel('60-65');    ax12.set_xlim(startXlim, endXlim);  ax12.set_ylim(startYlim, endYlim);
# slope, intercept, r, p, std = stats.linregress(binData["B12"], binData["B13"])
# ry = polyval([slope, intercept], binData["B12"])
# ax12.plot(binData["B12"], ry, 'r.-', linewidth=0.5, markersize=0.5)
#
# ax13.scatter(binData["B13"], binData["B14"], s=1);  ax13.set_xlabel('60-65');   ax13.set_ylabel('65-70');   ax13.set_xlim(startXlim, endXlim);  ax13.set_ylim(startYlim, endYlim);
# slope, intercept, r, p, std = stats.linregress(binData["B13"], binData["B14"])
# ry = polyval([slope, intercept], binData["B13"])
# ax13.plot(binData["B13"], ry, 'r.-', linewidth=0.5, markersize=0.5)
#
# ax14.scatter(binData["B14"], binData["B15"], s=1);  ax14.set_xlabel('65-70');   ax14.set_ylabel('70-75');   ax14.set_xlim(startXlim, endXlim);  ax14.set_ylim(startYlim, endYlim);
# slope, intercept, r, p, std = stats.linregress(binData["B14"], binData["B15"])
# ry = polyval([slope, intercept], binData["B14"])
# ax14.plot(binData["B14"], ry, 'r.-', linewidth=0.5, markersize=0.5)
#
# plt.subplots_adjust(hspace = 0.5, wspace = 0.5)
# plt.show()







# X = np.array([[row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]] for row in
#               zip( rawData["SessionAppNum"], rawData["SAS"], rawData["SCORE"], rawData["SCROLL"], rawData["KEY"], rawData["SHORT"],
#                   rawData["TOP10DurationEntropy"], rawData["TOP10FrequencyEntropy"])])
# pca = PCA(n_components=15)
# pca.fit(binData)
# Z = pca.transform(binData)
#
# print(Z)

# kmeans = KMeans(n_clusters=4).fit([[row1, row2] for row1, row2 in zip(Z[:, 0], Z[:, 1])])

# print(binData["B1"], binData["B2"])

# label_color = [LABEL_COLOR_MAP[l] for l in kmeans.labels_]
# plt.scatter(Z[:, 0], Z[:, 1])
# PLOTING3D(Z[:, 0], Z[:, 1], Z[:, 2])
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
#
# print(round(np.mean(A1), 3), round(np.std(A1), 3))
# print(round(np.mean(A2), 3), round(np.std(A2), 3))

# tTestResult = stats.ttest_rel(A2, A1)
# print("The T-statistic is %.3f and the p-value is %.3f" % tTestResult)


# 티 테스트
frequencyTop10 = [3.386,4.073,4.639,4.703,4.803,4.946,5.567,5.585,5.816,5.894]
frequencyTop90 = [19.736,19.811,19.848,20,20.145,20.163,20.393,21.205,27.743,27.932,]

A1 = [float(row) for index, row in enumerate(frequencyTop10)]
A2 = [round(row, 3) for index, row in enumerate(frequencyTop90)]

print(round(np.mean(A1), 3), round(np.std(A1), 3))
print(round(np.mean(A2), 3), round(np.std(A2), 3))

tTestResult = stats.ttest_rel(A2, A1)
print("The T-statistic is %.3f and the p-value is %.3f" % tTestResult)