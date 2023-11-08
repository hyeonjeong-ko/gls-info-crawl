import sqlite3

# SQLite DB 연결
conn = sqlite3.connect("skkedula-v1.db")
cursor = conn.cursor()
cursor.execute("""DROP TABLE IF EXISTS Students""")  #

# Enrollments 테이블 생성
cursor.execute(
    """
    CREATE TABLE Enrollments (
        Enrollment_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Student_ID INTEGER,
        Course_ID VARCHAR
    )
"""
)

# Students 테이블 생성
cursor.execute(
    """
    CREATE TABLE Students (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        User_ID VARCHAR,
        Name TEXT,
        PW VARCHAR
    )
"""
)


# 데이터 추가
cursor.execute(
    """
    INSERT INTO Students (User_id, Name, PW)
    VALUES (?, ?, ?)
""",
    ("1", "hj", "1"),
)


# 변경사항 저장
conn.commit()

# 연결 종료
conn.close()
