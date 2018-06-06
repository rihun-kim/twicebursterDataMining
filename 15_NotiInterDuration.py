from twicebursterDataMining.RH_Library import *
from Bunker.Marines import *
import matplotlib.pyplot as plt
from scipy import stats

#
#
# 수업시간 스마트폰 앱 Duration, Frequency 상관관계
studentsNotiInterDurationArray = []
for studentIndex in range(0, 84):
    studentDataPath = getStudentDataPathing(studentIndex)
    print(studentDataPath)

    #
    #
    # 데이터 준비하기
    notiDic = {}
    for row in sqlite3.connect(studentDataPath + "\\CLASSUSAGEDATABASE.db").execute("SELECT ENTRANCETIME, STARTTIME FROM CLASSUSAGETABLE WHERE TYPE=='noti'"):
        if row[0] in notiDic.keys():
            notiDic[row[0]].append(row[1])
        else:
            notiDic[row[0]] = [row[1]]

    #
    #
    #
    interNotiDuration = []
    for notiArray in notiDic.values():
        if len(notiArray) == 1:
            continue
        else:
            prevTime = ""
            temp = []
            for index, time in enumerate(notiArray):
                if index == 0:
                    prevTime = time
                else:
                    temp.append(elapsedTimeCalculating(prevTime, time ))
                    prevValue = time

        for row in temp:
            interNotiDuration.append(row)

    if len(interNotiDuration) != 0:
        studentsNotiInterDurationArray.append([studentIndex, round(sum(interNotiDuration) / len(interNotiDuration), 3)])

#
#
# 노티 인터듀레이션 박스플롯 그리기
# plt.boxplot(studentsNotiInterDurationArray)
# plt.show()

for row in studentsNotiInterDurationArray:
    print(row)
