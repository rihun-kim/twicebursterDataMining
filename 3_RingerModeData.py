from twicebursterDataMining.RH_Library import *
from Bunker.Marines import *
import matplotlib.pyplot as plt

#
#
# 링거모드 분포 히스토그램
studentsData = []
for studentIndex in range(0, 84):
    studentDataPath = getStudentDataPathing(studentIndex)
    print(studentDataPath)

    notiArray = []
    for row in sqlite3.connect(getStudentDataPathing(studentIndex) + "\\NOTIFICATIONDATABASE.db").execute("SELECT TIMESTAMP, PACKAGE FROM NOTIFICATIONTABLE WHERE POSTREMOVALRINGER == 'RINGER' AND PACKAGE != 'screenOn' AND PACKAGE != 'screenOff';"):
        notiArray.append(row)

    #
    #
    # 수업시간대 링거모드 추출하기
    classUsageDic, ringerDic = {}, {}
    for classUsageRow in sqlite3.connect(getStudentDataPathing(studentIndex) + "\\CLASSUSAGEDATABASE.db").execute("SELECT ENTRANCETIME FROM CLASSUSAGETABLE;"):
        if classUsageRow not in classUsageDic.keys():
            for notiIndex, notiRow in enumerate(notiArray):
                if classUsageRow[0] <= notiRow[0]:
                    classUsageDic[classUsageRow] = notiArray[notiIndex-1]
                    if notiArray[notiIndex-1][1] in ringerDic.keys():
                        ringerDic[notiArray[notiIndex-1][1]] += 1
                    else:
                        ringerDic[notiArray[notiIndex - 1][1]] = 1
                    break

    studentsData.append(ringerDic)

# #
# #
# # 링거모드 학생별 비율 출력하기
# for eachStudentData in studentsData:
#     vibrate, normal, silent, ringerSum = 0, 0, 0, 0
#     for ringerRow in eachStudentData.items():
#         if "vibrate" in ringerRow[0]:
#             vibrate = ringerRow[1]
#         elif "normal" in ringerRow[0]:
#             normal = ringerRow[1]
#         else:
#             silent = ringerRow[1]
#         ringerSum += ringerRow[1]
#
#     print(round(normal/ringerSum, 3)) #, round(vibrate/ringerSum, 3), round(normal/ringerSum, 3))

# #
# #
# # 링거모드 학생들 데이터 합치기
# vibrateTotal, normalTotal, silentTotal = 0, 0, 0
# for eachStudentData in studentsData:
#     for ringerRow in eachStudentData.items():
#         if "vibrate" in ringerRow[0]:
#             vibrateTotal += ringerRow[1]
#         elif "normal" in ringerRow[0]:
#             normalTotal += ringerRow[1]
#         else:
#             silentTotal += ringerRow[1]
#
# #
# #
# # 링거모드 히스토그램 그리기
# plt.bar(("vibrate", "normal", "silent"), (vibrateTotal, normalTotal, silentTotal))
# plt.xlabel("")
# plt.ylabel("")
# plt.show()
