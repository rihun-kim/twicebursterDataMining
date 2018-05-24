# from twicebursterDatamining.RH_Library import *
# from Bunker.Marines import *
# from multiprocessing import Process
#
# def multiMerging(startIndex, endIndex):
#     for studentIndex in range(startIndex, endIndex):
#         studentDataPath = getStudentDataPathing(studentIndex)
#         print(studentDataPath)
#
#         try:
#             logFiles = [file for root, dirs, files in os.walk(studentDataPath) for file in files if file.find("Log_") == 0]
#
#             appArray, notiArray = [], []
#             for logFile in logFiles:
#                 for row in sqlite3.connect(studentDataPath + "\\" + logFile).execute("SELECT * FROM APPTABLE;"):
#                     if ("20" in row[1]) and (row[2] != "BATTERY") and (row[2] != "ANDROID") and (row[2] != "RINGER"):
#                         appArray.append([timeFormatting(row[1]), row[2], row[3]])
#                 for row in sqlite3.connect(studentDataPath + "\\" + logFile).execute("SELECT * FROM NOTIFICATIONTABLE;"):
#                     if (row[2] != "BATTERY") and (row[2] != "DATA"):
#                         notiArray.append([timeFormatting(row[1]), row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12]])
#             appArray.sort()
#
#             APPDATABASEMAKING(studentDataPath + "\\APPDATABASE.db", appArray)
#             NOTIDATABASEMAKING(studentDataPath + "\\NOTIFICATIONDATABASE.db", notiArray)
#         except Exception as e:
#             print("[ EXCEPTION ]" + studentDataPath)
#             print(e.with_traceback(e))
#
# def multiAPNO(startIndex, endIndex):
#     for studentIndex in range(startIndex, endIndex):
#         studentDataPath = getStudentDataPathing(studentIndex)
#         print(studentDataPath)
#
#         appDic = {}
#         appArray = []
#         for row in sqlite3.connect(studentDataPath + "\\APPDATABASE.db").execute("SELECT * FROM APPTABLE;"):
#             if row not in appDic.keys():
#                 appDic[row] = row
#                 appArray.append(row)
#
#         notiDic = {}
#         notiArray = []
#         for row in sqlite3.connect(studentDataPath + "\\NOTIFICATIONDATABASE.db").execute("SELECT * FROM NOTIFICATIONTABLE;"):
#             if row not in notiDic.keys():
#                 notiDic[row] = row
#                 notiArray.append(row)
#
#         apnoArray = []
#         for row in appArray:
#             apnoArray.append((row[0], row[1], row[2], '', '', '', '', '', '', '', '', ''))
#         for row in notiArray:
#             apnoArray.append(row)
#         apnoArray = sorted(apnoArray, key=lambda row: row[0])
#
#         APNODATABASEMAKING(studentDataPath + "\\APNODATABASE.db", apnoArray)
#
# if __name__ == '__main__':
#     #
#     #
#     # 사용자별로 로그기록 합치기
#     procs = []
#     for index in range(0, 9):
#         startIndex = 0 if index == 0 else index * 10
#         endIndex = startIndex + 10 if index != 8 else startIndex + 4
#
#         proc = Process(target=multiMerging, args=(startIndex, endIndex))
#         procs.append(proc)
#         proc.start()
#
#     for proc in procs:
#         proc.join()
#
#
#     #
#     #
#     # 사용자별로 APPDATABASE 와 NOTIFICATIONDATABASE 합치기
#     procs = []
#     for index in range(0, 9):
#         startIndex = 0 if index == 0 else index * 10
#         endIndex = startIndex + 10 if index != 8 else startIndex + 4
#
#         proc = Process(target=multiAPNO, args=(startIndex, endIndex))
#         procs.append(proc)
#         proc.start()
#
#     for proc in procs:
#         proc.join()