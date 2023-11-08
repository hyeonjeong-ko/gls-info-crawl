import pandas as pd
import sqlite3

# 코스데이터 삽입

# 데이터베이스 연결
conn = sqlite3.connect("skkedula-v1.db")
cursor = conn.cursor()

# CSV 파일에서 데이터 읽기
data = pd.read_csv("major_course_data/merged_course_data.csv", encoding="ansi")

cursor.execute("""DROP TABLE IF EXISTS Courses""")  #

# SQLite에 테이블 생성
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS Courses (
        Course_ID TEXT PRIMARY KEY,
        Course_name TEXT,
        Professor TEXT,
        Time TEXT,
        Room_num TEXT,
        Class_type TEXT,
        Year INTEGER,
        Semester INTEGER
    )
"""
)

# 데이터 삽입
for _, row in data.iterrows():
    cursor.execute(
        """
        INSERT OR REPLACE INTO Courses (Course_ID, Course_name, Professor, Time, Room_num, Class_type, Year, Semester)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            row["class_code"],
            row["course_name"],
            row["professor"],
            row["class_time_number"],
            row["class_room"],
            row["class_type"],
            2023,  # Year: 2023
            2,  # Semester: 2
        ),
    )

# 변경사항 저장 및 연결 종료
conn.commit()
conn.close()
