from twicebursterDataMining.RH_Library import *
from Bunker.Marines import *
import matplotlib.pyplot as plt

#
#
# 학생별 수업시간 인터렉션 비율 구하기
studentsData = []
for studentIndex in range(0, 84):
    studentDataPath = getStudentDataPathing(studentIndex)
    print(studentDataPath)

    #
    #
    # 인터렉션 데이터 추출하기
    scroll, key, short, long = 0, 0, 0, 0
    for row in sqlite3.connect(studentDataPath + "\\CLASSAPNODATABASE.db").execute("SELECT * FROM CLASSAPNOTABLE"):
        if "SCROLL" in row[2]:
            scroll += 1
        elif "KEY" in row[2]:
            key += 1
        elif "SHORT" in row[2]:
            short += 1
        elif "LONG" in row[2]:
            long += 1

    interactionSum = scroll + short + long + key
    long = round((long / interactionSum), 3)
    short = round((short / interactionSum) + long, 3)
    key = round((key / interactionSum) + short, 3)
    scroll = 1

    studentsData.append([scroll, key, short, long])

#
#
# 인터렉션 비율 그래프 그리기
top4Color = ['#0054FF', '#00D8FF', '#1DDB16', '#FF5E00']
for studentIndex, eachStudentData in enumerate(studentsData):
    for index, value in enumerate(eachStudentData):
        plt.bar(studentIndex, value, color=top4Color[index])

plt.xlabel("")
plt.ylabel("")
plt.show()