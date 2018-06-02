from twicebursterDataMining.RH_Library import *
from Bunker.Marines import *
import matplotlib.pyplot as plt

#
#
# 학생수/신청과목수 그래프 그리기
clsCreditDic = {}
for row in sqlite3.connect(getDatabasePathing("SCHEDULEDATABASE.db")).execute("SELECT ID, CREDIT FROM SCHEDULETABLE"):
    clsCreditDic[row[0]] = row[1]

studentsDic = {}
for row in sqlite3.connect(getDatabasePathing("METADATABASE.db")).execute("SELECT ID, CLASSES FROM METATABLE"):
    clses = row[1].split("~")

    creditSum = 0
    for cls in clses:
        creditSum += int(clsCreditDic.get(cls))

    if creditSum in studentsDic.keys():
        studentsDic[creditSum] += 1
    else:
        studentsDic[creditSum] = 1

# plt.bar(studentsDic.keys(), studentsDic.values())
# plt.xticks(range(9, 25, 1))
# plt.yticks(range(0, 20, 1))
# plt.xlabel("Registered credits of classes")
# plt.ylabel("Number of students")
# plt.show()

#
#
# 학점/신청과목수 그래프 그리기
classes = []
for row in sqlite3.connect(getDatabasePathing("METADATABASE.db")).execute("SELECT * FROM METATABLE"):
    temp = row[5].split("~")
    for clss in temp:
        classes.append(clss)

classDic = {}
for row in sqlite3.connect(getDatabasePathing("SCHEDULEDATABASE.db")).execute("SELECT * FROM SCHEDULETABLE"):
    startTime = datetime.datetime.strptime(list(row)[4][3:8], "%H:%M")
    endTime = datetime.datetime.strptime(list(row)[4][12:], "%H:%M")
    classDic[row[0]] = str(endTime - startTime)

cntDic = {}
for row in classes:
    if classDic[row] in cntDic:
        cntDic[classDic[row]] += 1
    else:
        cntDic[classDic[row]] = 1

# x_num = ["1;15:00", "1:45:00", "2:45:00", "3:00:00", "3:15:00"]
# y_cnt = [353, 30, 59, 1, 2]
# plt.bar(x_num, y_cnt)
# plt.yticks(range(0, 360, 20))
# plt.xlabel("Registered Classes' Time")
# plt.ylabel("Number of students' class")
# plt.show()