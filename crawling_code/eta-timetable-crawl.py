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
            "Course Name": subject_name,
            "Professor": professor_name,
            "Class Room": classroom,
        }

for key, value in subject_info_map.items():
    print(f"{key}: {value}")

########################## 파일 불러와 시간표 정보와 최종 조인 ##########################
import pandas as pd

# 디렉토리 경로
directory_path = "./"

# 불러올 파일명과 경로
course_data_file = "test_course_data.csv"

filepath = os.path.join(directory_path, course_data_file)
course_data = pd.read_csv(filepath, encoding="ansi")

course_data["Course Name"] = course_data["Course Name"].astype(str)
course_data["Professor"] = course_data["Professor"].astype(str)
course_data["Class Room"] = course_data["Class Room"].astype(str)

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

df_empty["Class Time"] = None

# 각 Div에 대해 course_data에서 해당 강의 정보 찾기
for div, course_info in subject_info_map.items():
    rownum = div.replace("Div ", "")
    print("===========")
    print("rownum: ", rownum)
    print("===========")
    course_name = course_info["Course Name"]
    professor = course_info["Professor"]
    class_room = course_info["Class Room"]

    print(course_name, professor)

    # 해당 강의 정보 찾기
    found_course = course_data[
        (course_data["Professor"] == professor)
        & (course_data["Course Name"].str.contains(course_name))
        & (course_data["Class Room"].str.contains(class_room))
        & course_data["Class Time"]
    ]

    # Class Time이 같은 중복 행 제거
    found_course = found_course.drop_duplicates(subset=["Class Time"])

    # 각 행의 데이터를 JSON 형식으로 변환하여 리스트에 추가
    for index, row in found_course.iterrows():
        row_data = row.drop("college_name").to_dict()  # college_name 칼럼을 제외하고 딕셔너리로 변환
        json_data_list.append(row_data)

    print(f"Course information for {div}:")
    # print(found_course.iloc[0])
    print(found_course)

    # 결과 DataFrame에 추가
    df_empty = pd.concat([df_empty, found_course])
df_empty.to_csv(csv_file_path, encoding="ansi", index=False)
print("==============================")
print(json_data_list)
print("==============================")


# import json

# # 데이터를 Node.js 서버로 전송
# url = "http://localhost:8080/timetables/courses"
# headers = {"Content-Type": "application/json"}
# response = requests.post(url, data=json.dumps(json_data_list), headers=headers)

# if response.status_code == 200:
#     print("데이터 전송 성공")
# else:
#     print("데이터 전송 실패")
