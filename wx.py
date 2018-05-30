# from twicebursterDataMining.RH_Library import *
# from Bunker.Marines import *
# import numpy as np
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