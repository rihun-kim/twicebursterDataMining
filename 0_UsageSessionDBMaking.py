from twicebursterDataMining.RH_Library import *
from Bunker.Marines import *

from multiprocessing import Process
import copy

def multiUsaging(startIndex, endIndex):
    for studentIndex in range(startIndex, endIndex):
        studentDataPath = getStudentDataPathing(studentIndex)
        print(studentDataPath)

        try:
            #
            #
            # 시작과 끝부분 자르기
            LOCK = 0
            apnoArray1 = []
            for row in sqlite3.connect(studentDataPath + "\\APNODATABASE.db").execute("SELECT TIMESTAMP, TYPE, PACKAGE FROM APNOTABLE;"):
                if row[0] >= "2017.12.18_00.00.00.000":
                    break
                if LOCK == 1:
                    apnoArray1.append(row)
                elif "screenOn" in row[2]:
                    apnoArray1.append(row)
                    LOCK = 1
            for index in range(len(apnoArray1)-1, 0, -1):
                if "screenOff" in apnoArray1[index][2]:
                    break
                apnoArray1.pop(index)

            #
            #
            # 스크린 On/Off 시간 구하기
            LOCK = 0
            onTimeArray1, offTimeArray1 = [], []
            onTimeArray2, offTimeArray2 = [], []
            for row in apnoArray1:
                if "screenOn" == row[2]:
                    if LOCK == 1:
                        onTimeArray1.pop()
                        onTimeArray2.pop()
                    onTimeArray1.append(row[0])
                    onTimeArray2.append(row)
                    LOCK = 1
                elif LOCK == 1 and "screenOff" == row[2]:
                    offTimeArray1.append(row[0])
                    offTimeArray2.append(row)
                    LOCK = 0

            #
            #
            # 스크린 On/Off로 영역 구하기
            # 깡통 제거하기
            for screenTimeIndex, screenTimeRow in enumerate(zip(onTimeArray1, offTimeArray1)):
                screenElapsedTime = elapsedTimeCalculating(screenTimeRow[0], screenTimeRow[1])
                if screenElapsedTime >= 3600:
                    intervalArray = []
                    for apnoRow in apnoArray1:
                        if screenTimeRow[0] <= apnoRow[0] <= screenTimeRow[1]:
                            intervalArray.append(apnoRow[0])
                        elif screenTimeRow[1] < apnoRow[0]:
                            break

                    startIndex = 0
                    for intervalIndex in range(1, len(intervalArray)):
                        if ("POSTED" in intervalArray[intervalIndex][1]) \
                                or ("RUNNING" in intervalArray[intervalIndex][1] and "video" not in intervalArray[intervalIndex][2].lower()) \
                                or ("RUNNING" in intervalArray[intervalIndex][1] and "movie" not in intervalArray[intervalIndex][2].lower()) \
                                or ("RUNNING" in intervalArray[intervalIndex][1] and "youtube" not in intervalArray[intervalIndex][2].lower()) \
                                or ("RUNNING" in intervalArray[intervalIndex][1] and "afreeca" not in intervalArray[intervalIndex][2].lower()) \
                                or ("REMOVED" in intervalArray[intervalIndex][1]):
                            continue
                        else:
                            if elapsedTimeCalculating(intervalArray[startIndex], intervalArray[intervalIndex]) >= 3000:
                                onTimeArray1[screenTimeIndex] = "x"
                                offTimeArray1[screenTimeIndex] = "x"
                                break
                            else:
                                startIndex = intervalIndex
            #
            #
            # 데이터 뽑아내기
            screenOnOffTimeArray = []
            for row in zip(onTimeArray1, offTimeArray1):
                if row[0] == "x":
                    continue
                screenOnOffTimeArray.append(["screen", row[0], row[1], secToTimeFormatting(elapsedTimeCalculating(row[0], row[1])), timeToSecFormating(secToTimeFormatting(elapsedTimeCalculating(row[0], row[1])))])

            #
            #
            # 노티로 영역 구하기
            apnoDic = {}
            for row in apnoArray1:
                apnoDic[(row[0], row[2])] = [row[0], row[1], row[2], ""]
            for row in onTimeArray2:
                if (row[0], row[2]) in apnoDic.keys():
                    apnoDic[(row[0], row[2])][3] = "on"
            for row in offTimeArray2:
                if (row[0], row[2]) in apnoDic.keys():
                    apnoDic[(row[0], row[2])][3] = "off"

            LOCK = 0
            apnoArray2 = []
            for row in apnoDic.values():
                if row[3] == "on":
                    apnoArray2.append([row[0], row[1], row[2], "on"])
                    LOCK = 1
                    continue
                if row[3] == "off":
                    apnoArray2.append([row[0], row[1], row[2], "off"])
                    LOCK = 0
                    continue
                if LOCK == 0:
                    apnoArray2.append(row)
                else:
                    apnoArray2.append([row[0], row[1], row[2], "using"])

            LOCK = 0
            notiOnTimeArray, notiOffTimeArray = [], []
            for row in apnoArray2:
                if LOCK == 1 and "" != row[3]:
                    notiOnTimeArray.pop()
                    LOCK = 0
                elif LOCK == 0 and "" == row[3] and ("TOUCH" in row[1] or "KEY" in row[1] or "RUNNING" in row[1]):
                    notiOnTimeArray.append(row[0])
                    LOCK = 1
                elif LOCK == 1 and "" == row[3] and "screenOff" == row[2]:
                    notiOffTimeArray.append(row[0])
                    LOCK = 0

            #
            #
            # 깡통 제거하기
            for notiTimeIndex, notiTimeRow in enumerate(zip(notiOnTimeArray, notiOffTimeArray)):
                notiElapsedTime = elapsedTimeCalculating(notiTimeRow[0], notiTimeRow[1])
                if notiElapsedTime >= 3600:
                    intervalArray = []
                    for apnoRow in apnoArray2:
                        if notiTimeRow[0] <= apnoRow[0] <= notiTimeRow[1]:
                            intervalArray.append(apnoRow)
                        elif notiTimeRow[1] < apnoRow[0]:
                            break

                    startIndex = 0
                    for intervalIndex in range(1, len(intervalArray)):
                        if ("POSTED" in intervalArray[intervalIndex][1]) \
                                or ("RUNNING" in intervalArray[intervalIndex][1] and "video" not in intervalArray[intervalIndex][2].lower()) \
                                or ("RUNNING" in intervalArray[intervalIndex][1] and "movie" not in intervalArray[intervalIndex][2].lower()) \
                                or ("RUNNING" in intervalArray[intervalIndex][1] and "youtube" not in intervalArray[intervalIndex][2].lower()) \
                                or ("RUNNING" in intervalArray[intervalIndex][1] and "afreeca" not in intervalArray[intervalIndex][2].lower()) \
                                or ("REMOVED" in intervalArray[intervalIndex][1]):
                            continue
                        else:
                            if elapsedTimeCalculating(intervalArray[startIndex][0], intervalArray[intervalIndex][0]) >= 3000:
                                notiOnTimeArray[notiTimeIndex] = "x"
                                notiOffTimeArray[notiTimeIndex] = "x"
                                break
                            else:
                                startIndex = intervalIndex

            #
            #
            # 데이터 뽑아내기
            notiOnOffTimeArray = []
            for row in zip(notiOnTimeArray, notiOffTimeArray):
                if row[0] == "x":
                    continue
                notiOnOffTimeArray.append(["noti", row[0], row[1], secToTimeFormatting(elapsedTimeCalculating(row[0], row[1])), timeToSecFormating(secToTimeFormatting(elapsedTimeCalculating(row[0], row[1])))])

            #
            #
            # 합쳐서 데이터베이스로 만들기
            totalOnOffTimeArray = copy.deepcopy(notiOnOffTimeArray)
            for row in screenOnOffTimeArray:
                totalOnOffTimeArray.append(list(row))

            totalOnOffTimeArray = sorted(totalOnOffTimeArray, key=lambda row: row[1])
            USAGEDATABASEMAKING(studentDataPath + "\\USAGEDATABASE.db", totalOnOffTimeArray)

        except Exception as e:
            print("[ EXCEPTION ]" + studentDataPath)
            print(e.with_traceback(e))

if __name__ == '__main__':
    procs = []
    for index in range(0, 9):
        startIndex = 0 if index == 0 else index * 10
        endIndex = startIndex + 10 if index != 8 else startIndex + 4

        proc = Process(target=multiUsaging, args=(startIndex, endIndex))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()










