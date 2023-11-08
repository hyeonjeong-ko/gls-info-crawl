from selenium import webdriver
from html import unescape
import numpy as np

import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding="utf-8")

url = "https://everytime.kr/@dFVaBrnPAC561ItzJ4Or"  # 대상 페이지 URL로 변경

options = webdriver.ChromeOptions()
# 창 숨기는 옵션 추가
options.add_argument("headless")

options.add_argument("no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(
    "user-agent={Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36}"
)


# 웹 드라이버 설정 (Chrome 사용 예시)
driver = webdriver.Chrome(options=options)  # chromedriver의 경로로 변경

driver.implicitly_wait(3)

# 웹 페이지 열기
driver.get(url)

# 페이지의 HTML 가져오기 (바이트 문자열)
html = driver.page_source  # .encode("utf-8")

# 페이지의 HTML 출력
# print(html)

# 웹 드라이버 종료
driver.quit()

import requests
from bs4 import BeautifulSoup


soup = BeautifulSoup(html, "html.parser")
subject_divs = soup.find_all(
    "div", class_=lambda value: value and value.startswith("subject")
)


# subject로 시작하는 div 태그 개수 출력
print("Total div tags starting with 'subject':", len(subject_divs))

# 과목 정보를 저장
subject_info_map = {}

for index, div in enumerate(subject_divs, start=1):
    h3_tag = div.find("h3")
    em_tag = div.find("em")
    span_tag = div.find("span")

    subject_name = h3_tag.text if h3_tag else None
    professor_name = em_tag.text if em_tag else None
    classroom = span_tag.text if span_tag and span_tag.text else None

    # classroom 정보가 없을시 저장되지않는다.
    if classroom is not None:  # or subject_name is not None
        # 맵 자료구조에 저장
        subject_info_map[f"Div {index}"] = {
            "course_name": subject_name,
            "professor": professor_name,
            "class_room": classroom,
        }

for key, value in subject_info_map.items():
    print(f"{key}: {value}")

########################## 파일 불러와 시간표 정보와 최종 조인 ##########################
import pandas as pd

# 디렉토리 경로
directory_path = "major_course_data/"

# 불러올 파일명과 경로
course_data_file = "merged_course_data.csv"

filepath = os.path.join(directory_path, course_data_file)
course_data = pd.read_csv(filepath, encoding="ansi")

course_data["class_code"] = course_data["class_code"].astype(str)  # 118 추가된부분

course_data["course_name"] = course_data["course_name"].astype(str)
course_data["professor"] = course_data["professor"].astype(str)
course_data["class_room"] = course_data["class_room"].astype(str)
course_data["class_type"] = course_data["class_type"].astype(str)

# 교수명이 "차수영"인 행 검색
# result = course_data[
#     (course_data["Professor"] == "차수영")
#     & (course_data["Course Name"].str.contains("소프트웨어공학개론"))
# ]

# print("Rows where Professor is '차수영':")
# print(result)


csv_file_path = "user_timetable.csv"

# 빈 데이터프레임 생성
df_empty = pd.DataFrame()

json_data_list = []

# 딕셔너리를 데이터프레임으로 변환하여 추가
for key, value in subject_info_map.items():
    df_temp = pd.DataFrame(value, index=[key])
    # df_empty = pd.concat([df_empty, df_temp])

    # df_empty.to_csv(csv_file_path, encoding="ansi", index=False)

df_empty["class_time"] = None

# 각 Div에 대해 course_data에서 해당 강의 정보 찾기
for div, course_info in subject_info_map.items():
    rownum = div.replace("Div ", "")
    print("===========")
    print("rownum: ", rownum)
    print("===========")
    course_name = course_info["course_name"]
    professor = course_info["professor"]
    class_room = course_info["class_room"]

    print(course_name, professor)

    # 해당 강의 정보 찾기
    found_course = course_data[
        (course_data["professor"] == professor)
        & (course_data["course_name"].str.contains(course_name))
        & (course_data["class_room"].str.contains(class_room))
        & course_data["class_time"]
    ]

    # Class Time이 같은 중복 행 제거
    found_course = found_course.drop_duplicates(subset=["class_time"])
    #    found_course = found_course.drop_duplicates(subset=["course_name"])

    # 각 행의 데이터를 JSON 형식으로 변환하여 리스트에 추가
    for index, row in found_course.iterrows():
        row_data = (
            row.drop("college_name").drop("department_name").to_dict()
        )  # college_name 칼럼을 제외하고 딕셔너리로 변환
        json_data_list.append(row_data)

    print(f"Course information for {div}:")
    print(found_course)

    # 결과 DataFrame에 추가
    df_empty = pd.concat([df_empty, found_course])
df_empty.to_csv(csv_file_path, encoding="ansi", index=False)

###
# 중복된 'class_code'를 추적할 집합 생성
seen_codes = set()

# 중복된 'class_code'를 가진 항목을 필터링하여 새로운 리스트를 생성
unique_json_data_list = []
for data in json_data_list:
    if data["class_code"] not in seen_codes:
        unique_json_data_list.append(data)
        seen_codes.add(data["class_code"])

# 'college_name'을 제거
for data in unique_json_data_list:
    if "college_name" in data:
        del data["college_name"]

###
print("==============================")
print(unique_json_data_list)
print("==============================")


# import json

# 유저의 시간표 데이터를 서버 db로 전송!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# import sqlite3

# # 연결 및 커서 생성
# conn = sqlite3.connect("skkedula-v1.db")
# cursor = conn.cursor()


# # Students
# # cursor.execute("SELECT ID FROM Students WHERE User_ID=?", ("1",))


# # Student_ID 설정
# student_id = 1  # 사용자의 ID로 가정

# # user_id = cursor.fetchone()[0]

# # 주어진 데이터로부터 Course_ID 추출
# course_ids = [data["class_code"] for data in unique_json_data_list]


# # Enrollments 테이블에 수강정보 삽입
# for course_id in course_ids:
#     cursor.execute(
#         """
#         SELECT * FROM Enrollments WHERE Student_ID = ? AND Course_ID = ?
#         """,
#         (student_id, course_id),
#     )
#     existing_data = cursor.fetchone()  # 이미 있는 데이터가 있는지 확인

#     if not existing_data:
#         cursor.execute(
#             """
#             INSERT INTO Enrollments (Student_ID, Course_ID)
#             VALUES (?, ?)
#             """,
#             (student_id, course_id),
#         )
# # 변경사항 저장
# conn.commit()

# # 연결 종료
# conn.close()
