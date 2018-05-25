from twicebursterDataMining.RH_Library import *
from Bunker.Marines import *
from multiprocessing import Process
import matplotlib.pyplot as plt
import numpy as np

# #
# #
# # 수업시 사용한 앱 사용내역 데이터베이스 만들기
# def multiClassAPNO(startIndex, endIndex):
#     for studentIndex in range(startIndex, endIndex):
#         studentDataPath = getStudentDataPathing(studentIndex)
#         print(studentDataPath)
#
#         try:
#             #
#             #
#             # 데이터 준비하기
#             apnoUsageArray = []
#             for row in sqlite3.connect(studentDataPath + "\\APNODATABASE.db").execute("SELECT TIMESTAMP, TYPE, PACKAGE FROM APNOTABLE"):
#                 apnoUsageArray.append(row)
#
#             classUsageArray = []
#             for row in sqlite3.connect(studentDataPath + "\\CLASSUSAGEDATABASE.db").execute("SELECT CLASSNAME, TYPE, STARTTIME, ENDTIME FROM CLASSUSAGETABLE"):
#                 classUsageArray.append(row)
#
#             #
#             #
#             # 데이터 뽑아내기
#             classApnoArray = []
#             for index, classUsageRow in enumerate(classUsageArray):
#                 classUsageType, classUsageOnTime, classUsageOffTime = classUsageRow[1], classUsageRow[2], classUsageRow[3]
#
#                 if classUsageType == "screen":
#                     runApnoIndex, runApnoArray = 0, []
#                     touchAction, previousAppNeedy, usageOnTimeIndex = False, False, 0
#                     for apnoUsageRowIndex, apnoUsageRow in enumerate(apnoUsageArray):
#                         if classUsageOnTime <= apnoUsageRow[0] <= classUsageOffTime:
#                             if apnoUsageRow[0] == classUsageOnTime and apnoUsageRow[2] == "screenOn":
#                                 runApnoArray.append([-1, apnoUsageRow[0], apnoUsageRow[1], apnoUsageRow[2]])
#                                 usageOnTimeIndex = apnoUsageRowIndex
#                             elif apnoUsageRow[0] == classUsageOffTime and apnoUsageRow[2] == "screenOff":
#                                 runApnoArray.append([-1, apnoUsageRow[0], apnoUsageRow[1], apnoUsageRow[2]])
#                                 runApnoArray.insert(0, [classUsageType, touchAction, previousAppNeedy, usageOnTimeIndex])
#                                 break
#                             elif apnoUsageRow[1] == "POSTED" or apnoUsageRow[1] == "REMOVED":
#                                 runApnoArray.append([-999, apnoUsageRow[0], apnoUsageRow[1], apnoUsageRow[2]])
#                             elif apnoUsageRow[1] == "RUNNING":
#                                 runApnoIndex += 1
#                                 runApnoArray.append([runApnoIndex, apnoUsageRow[0], apnoUsageRow[1], apnoUsageRow[2]])
#                             elif len(runApnoArray) != 0:
#                                 runApnoArray.append([runApnoIndex, apnoUsageRow[0], apnoUsageRow[1], apnoUsageRow[2]])
#                                 if not touchAction and ("TOUCH" in apnoUsageRow[1] or "KEY" in apnoUsageRow[1]):
#                                     touchAction = True
#                                 if not previousAppNeedy and runApnoIndex == 0:
#                                     previousAppNeedy = True
#
#                     #
#                     #
#                     # 깡통버리기 및 이전에 사용하다가 화면만 끈 앱 찾기
#                     if touchAction:
#                         if previousAppNeedy:
#                             for index in range(runApnoArray[0][3], 0, -1):
#                                 if apnoUsageArray[index][1] == "RUNNING":
#                                     runApnoArray.insert(2, [0, runApnoArray[1][1], apnoUsageArray[index][1], apnoUsageArray[index][2]])
#                                     break
#                         if previousAppNeedy:
#                             for row in runApnoArray:
#                                 if (row[0] != "screen") and (int(row[0]) >= 0):
#                                     row[0] = int(row[0]) + 1
#                                 classApnoArray.append(row)
#                         else:
#                             for row in runApnoArray:
#                                 classApnoArray.append(row)
#
#                 elif classUsageType == "noti":
#                     runApnoIndex, runApnoArray = 0, []
#                     touchAction, previousAppNeedy, usageOnTimeIndex = False, False, 0
#                     for apnoUsageRowIndex, apnoUsageRow in enumerate(apnoUsageArray):
#                         if classUsageOnTime <= apnoUsageRow[0] <= classUsageOffTime:
#                             if apnoUsageRow[0] == classUsageOnTime:
#                                 usageOnTimeIndex = apnoUsageRowIndex
#
#                             if apnoUsageRow[0] == classUsageOffTime and apnoUsageRow[2] == "screenOff":
#                                 runApnoArray.append([-1, apnoUsageRow[0], apnoUsageRow[1], apnoUsageRow[2]])
#                                 runApnoArray.insert(0, [classUsageType, touchAction, previousAppNeedy, usageOnTimeIndex])
#                                 break
#                             elif apnoUsageRow[1] == "POSTED" or apnoUsageRow[1] == "REMOVED":
#                                 runApnoArray.append([-999, apnoUsageRow[0], apnoUsageRow[1], apnoUsageRow[2]])
#                             elif apnoUsageRow[1] == "RUNNING":
#                                 runApnoIndex += 1
#                                 runApnoArray.append([runApnoIndex, apnoUsageRow[0], apnoUsageRow[1], apnoUsageRow[2]])
#                             else:
#                                 runApnoArray.append([runApnoIndex, apnoUsageRow[0], apnoUsageRow[1], apnoUsageRow[2]])
#                                 if not touchAction and ("TOUCH" in apnoUsageRow[1] or "KEY" in apnoUsageRow[1]):
#                                     touchAction = True
#                                 if not previousAppNeedy and runApnoIndex == 0:
#                                     previousAppNeedy = True
#
#                     #
#                     #
#                     # 깡통버리기 및 노티로 시작한 앱 찾기
#                     if touchAction:
#                         if previousAppNeedy:
#                             for index in range(runApnoArray[0][3], 0, -1):
#                                 if apnoUsageArray[index][1] == "RUNNING":
#                                     runApnoArray.insert(1, [0, runApnoArray[1][1], apnoUsageArray[index][1], apnoUsageArray[index][2]])
#                                     break
#                         if previousAppNeedy:
#                             for row in runApnoArray:
#                                 if (row[0] != "noti") and (int(row[0]) >= 0):
#                                     row[0] = int(row[0]) + 1
#                                 classApnoArray.append(row)
#                         else:
#                             for row in runApnoArray:
#                                 classApnoArray.append(row)
#
#             CLASSAPNODATABASEMAKING(studentDataPath + "\\CLASSAPNODATABASE.db", classApnoArray)
#         except Exception as e:
#             print("[ EXCEPTION ]" + studentDataPath)
#             print(e.with_traceback(e))
#
# if __name__ == '__main__':
#     procs = []
#     for index in range(0, 9):
#         startIndex = 0 if index == 0 else index * 10
#         endIndex = startIndex + 10 if index != 8 else startIndex + 4
#
#         proc = Process(target=multiClassAPNO, args=(startIndex, endIndex))
#         procs.append(proc)
#         proc.start()
#
#     for proc in procs:
#         proc.join()

#
#
# 수업시간 평균 앱 갯수 및 세션 내 평균 앱 갯수 구하기
studentsData = []
for studentIndex in range(0, 84):
    studentDataPath = getStudentDataPathing(studentIndex)
    print(studentDataPath)

    #
    #
    # 세션 내 앱 갯수 추출하기
    deleteAppDic = {"com.lge.signboard":"", "com.lge.launcher2":"", "com.android.systemui":"", "com.lge.launcher3":"", "com.sec.android.app.launcher":"",
                    "com.buzzpia.aqua.launcher":"", "com.skp.launcher":"", "com.campmobile.launcher":"", "com.phone.launcher.android":"", "com.fihtdc.foxlauncher":"", "android":"",
                    "com.cashwalk.cashwalk":""}
    sessionAppNumArray, stack = [], []
    for index, row in enumerate(sqlite3.connect(studentDataPath + "\\CLASSAPNODATABASE.db").execute("SELECT * FROM CLASSAPNOTABLE")):
        if row[2] == "RUNNING":
            stack.append(row)
        elif row[3] == "screenOff":
            startApp = ""
            sessionAppNum = 0
            while stack:
                stackRow = stack.pop()
                if (startApp != stackRow[3]) and (stackRow[3] not in deleteAppDic.keys()):
                    sessionAppNum += 1
                    startApp = stackRow[3]
            sessionAppNumArray.append(sessionAppNum)

    #
    #
    # 수업시간 갯수 추출하기
    tempDic = {}
    for row in sqlite3.connect(studentDataPath + "\\CLASSUSAGEDATABASE.db").execute("SELECT * FROM CLASSUSAGETABLE"):
        if (row[1], row[2]) not in tempDic.keys():
            tempDic[(row[1], row[2])] = 1

    classNumSum = len(tempDic)
    sessionAppNumSum = sum(sessionAppNumArray)

    # 수업시간 평균 앱 갯수 = 모든 세션내 앱 갯수 / 모든 수업시간 갯수
    # 세션 내 평균 앱 갯수 = 모든 세션내 앱 갯수 / 모든 세션 갯수
    studentsData.append([round((sessionAppNumSum/classNumSum), 3), round(sessionAppNumSum / len(sessionAppNumArray), 3)])

#
#
# 누적 막대그래프 그리기
studentIndex = [i for i in range(0, 84)]
studentsData = sorted(studentsData, key=lambda row: row[0])

p1 = plt.bar(studentIndex, [row[0] for row in studentsData])
p2 = plt.bar(studentIndex, [row[1] for row in studentsData])

plt.show()



























