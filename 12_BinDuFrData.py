from twicebursterDataMining.RH_Library import *
from Bunker.Marines import *
import matplotlib.pyplot as plt

#
#
# 전체학생 Bin 평균의 Duration, Frequency 박스플롯
studentsData = []
for studentIndex in range(0, 1):
    studentDataPath = getStudentDataPathing(studentIndex)
    print(studentDataPath)

    outClasses = ["프로그래밍기초", "일반물리학실험", "일반화학실헝", " 역사학특강", "사회과학특강", "영문학특강", "발상과 표현", "심리철학", "AdvancedEnglish", "빛,생명,그리고색체", "문제해결기법", "EnglishPresentation&Discussion"]
    for scheduleRow in sqlite3.connect(getDatabasePathing("SCHEDULEDATABASE.db")).execute("SELECT * FROM SCHEDULETABLE"):
        skip = False
        for cls in outClasses:
            if cls in scheduleRow[0]:
                skip = True
                break
        if not skip:
            if scheduleRow[4][3:8] == scheduleRow[5][3:8]:
                print("true")
            else:
                print("false", scheduleRow)


    # entranceTimeArray, exitTimeArray = [], []
    # for attendanceArray in sqlite3.connect(getDatabasePathing("ATTENDANCEDATABASE.db")).execute("SELECT * FROM ATTENDANCETABLE WHERE ID=='"+getStudentID(studentIndex)+"'"):
    #     for row in attendanceArray:
    #         if row[0:4] == "2017":
    #             for val1, val2 in row.split("~"):
    #                 entranceTimeArray.append(val1)
    #                 exitTimeArray.append(val2)
    #
    # for row1, row2 in (entranceTimeArray, exitTimeArray):
    #     print(row1, row2)


    # for row in sqlite3.connect(getStudentDataPathing(studentIndex) + "\\CLASSUSAGEDATABASE.db").execute("SELECT * FROM CLASSUSAGETABLE"):
    #     print(row)








