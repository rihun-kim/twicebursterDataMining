from sklearn.model_selection import train_test_split

from twicebursterDataMining.RH_Library import *
from Bunker.Marines import *
import numpy as np
#
# # sql = sqlite3.connect(getDatabasePathing("\\PSYDATABASE.db"))
# #
# # studentsData = []
# # for studentIndex in range(0, 84):
# #     for array in sql.execute("SELECT * FROM '"+getStudentID(studentIndex)+"';"):
# #         if array[0] == "SAS":
# #             temp = []
# #             for row in array:
# #                 if row == None:
# #                     studentsData.append(np.mean(temp))
# #                     break
# #                 if "TOT" in row:
# #                     temp.append(int(row[-2:]))
# #
# # for row in studentsData:
# #     print(row)
#
#
# scoreDic = {"A+":4.3, "A0":4.0, "A-":3.7, "B+":3.3, "B0":3.0, "B-":2.7, "C+":2.3, "C0":2.0, "C-":1.7, "D+":1.3, "D0":1.0, "D-":0.7, "F":0.0}
# studentsData = []
# for index, array in enumerate(sqlite3.connect(getDatabasePathing("\\SCOREDATABASE.db")).execute("SELECT * FROM SCORETABLE")):
#     temp = []
#     for i, row in enumerate(array):
#         if row == "" or i == 16:
#             studentsData.append(np.mean(temp))
#             break
#         elif len(row) <= 3:
#             temp.append(scoreDic[row])
#
# for row in studentsData:
#     print(round(row, 3))

# class75MDic = {}
# for row in sqlite3.connect(getDatabasePathing("SCHEDULEDATABASE.db")).execute("SELECT * FROM SCHEDULETABLE"):
#     startTime = datetime.datetime.strptime(list(row)[4][3:8], "%H:%M")
#     endTime = datetime.datetime.strptime(list(row)[4][12:], "%H:%M")
#     if str(endTime - startTime) == "1:15:00":
#         class75MDic[row[0]] = [row[4], row[5]]
#
# studentsData = {}
# lateCnt = 0
# for row in sqlite3.connect(getDatabasePathing("ATTENDANCEDATABASE.db")).execute("SELECT * FROM ATTENDANCETABLE"):
#     if row[1] not in class75MDic.keys():
#         continue
#
#     if row[0] not in studentsData.keys():
#         studentsData[row[0]] = [0, 0]
#
#     for time in row[2:]:
#         if time == "":
#             continue
#         elif time[17:19] != "00":
#             studentsData[row[0]][0] += 1
#         else:
#             studentsData[row[0]][1] += 1
#
#
# for row in studentsData.items():
#     print(round(row[1][0] / (row[1][0] + row[1][1]), 3))








LABEL_COLOR_MAP = {
    0	: "#0048BA",
1	: "#4C2F27",
2	: "#B0BF1A",
3	: "#7CB9E8",
4	: "#C9FFE5",
5	: "#B284BE",
6	: "#5D8AA8",
7	: "#00308F",
8	: "#72A0C1",
9	: "#AF002A",
10	: "#F2F0E6",
11	: "#F0F8FF",
12	: "#E32636",
13	: "#C46210",
14	: "#EFDECD",
15	: "#D6D6D6",
16	: "#D2D9DB",
17	: "#E52B50",
18	: "#9F2B68",
19	: "#F19CBB",
20	: "#AB274F",
21	: "#D3212D",
22	: "#3B7A57",
23	: "#FFBF00",
24	: "#FF7E00",
25	: "#3B3B6D",
26	: "#391802",
27	: "#804040",
28	: "#D3AF37",
29	: "#34B334",
30	: "#FF8B00",
31	: "#FF9899",
32	: "#431C53",
33	: "#B32134",
34	: "#FF033E",
35	: "#CFCFCF",
36	: "#551B8C",
37	: "#F2B400",
38	: "#9966CC",
39	: "#553592",
40	: "#8A2BE2",
41	: "#4D1A7F",
42	: "#7366BD",
43	: "#4F86F7",
44	: "#1C1CF0",
45	: "#DE5D83",
46	: "#79443B",
47	: "#0095B6",
48	: "#E3DAC9",
49	: "#DDE26A",
50	: "#006A4E",
51	: "#0E9CA5",
52	: "#873260",
53	: "#0070FF",
54	: "#87413F",
55	: "#B5A642",
56	: "#1974D2",
57	: "#FF007F",
58	: "#08E8DE",
59	: "#D19FE8",
60	: "#FFAA1D",
61	: "#3399FF",
62	: "#F4BBFF",
63	: "#CC5500",
64	: "#E97451",
65	: "#8A3324",
66	: "#24A0ED",
67	: "#BD33A4",
68	: "#702963",
69	: "#536872",
70	: "#5F9EA0",
71	: "#A9B2C3",
72	: "#91A3B0",
73	: "#0A1195",
74	: "#DFFF00",
75	: "#7FFF00",
76	: "#FFA600",
77	: "#DE3163",
78	: "#FFB7C5",
79	: "#954535",
80	: "#FFC34D",
81	: "#DE6FA1",
82	: "#A8516E",
83	: "#141414"}








# from matplotlib import pyplot as plt
# import pandas as pd
# import sklearn
# import sklearn.datasets
# from sklearn.metrics import roc_curve, auc
# from sklearn.linear_model import LogisticRegression
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.naive_bayes import GaussianNB
#
# CLASS_MAP = {
#     "LogisticRegression" : ('-', LogisticRegression()),
#     "GaussianNB" : ("--", GaussianNB()),
#     "DecisionTreeClassifier" : (".-", DecisionTreeClassifier(max_depth=5)),
#     "RandomForestClassifier" : (":", RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1))
# }
#
# ds = sklearn.datasets.load_iris()
# df = pd.DataFrame(ds["data"], columns=ds["feature_names"])
# code_species_map = dict(zip(range(3), ds["target_names"]))
# df["species"] = [code_species_map[c] for c in ds["target"]]
# X, Y = df[df.columns[:3]], (df["species"] == "virginica")
#
# X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = .8)
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