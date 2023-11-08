import sys
import io
import csv
import pandas as pd
import os

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding="utf-8")

# 카테고리 리스트
allowed_categories = [
    "공과대학",
    "사회과학대학",
    "생명공학대학",
    "성균나노과학기술원",
    "성균융합원",
    "소프트웨어대학",
    "소프트웨어융합대학",
    "스포츠과학대학",
    "약학대학",
    "의과대학",
    "자연과학대학",
    "정보통신대학",
    "학부대학",
]


# 합칠 CSV 파일들이 들어있는 디렉토리 경로
directory_path = "major_course_data/"

# 결과를 저장할 파일명과 경로
output_file = "major_course_data/merged_course_data.csv"

# 빈 DataFrame 생성
merged_data = pd.DataFrame()

# 디렉토리 내의 모든 CSV 파일에 대해 반복
for filename in os.listdir(directory_path):
    if filename.endswith(".csv") and filename.startswith("course_data"):
        # CSV 파일을 DataFrame으로 읽어오기
        filepath = os.path.join(directory_path, filename)
        data = pd.read_csv(filepath, encoding="ansi")

        # Class Room 정보 추출
        data["class_room"] = data["class_time"].str.extract(r"【(\d+)")

        ##############################################################
        # 시간 형식 변환하여 새로운 열 생성
        day_map = {"월": 1, "화": 2, "수": 3, "목": 4, "금": 5, "토": 6, "일": 7}

        for index, row in data.iterrows():
            try:
                if "미지정" in row["class_time"]:
                    data.at[index, "class_time_number"] = "미지정"
                elif "일반수업" in row["class_time"]:
                    data.at[index, "class_time_number"] = "일반수업"
                else:
                    class_times = row["class_time"].split(
                        ","
                    )  # 각 행의 "class_time" 값을 쉼표로 분할

                    extracted_values = []

                    for time in class_times:
                        day, raw_time = time[0], time[1:]

                        # 시간을 분할하여 형식 맞게 조정
                        day_code = day_map[day[0]]
                        start_time = raw_time.split("-")[0].replace(":", "")
                        end_time = raw_time.split("-")[1].split("【")[0].replace(":", "")

                        extracted_values.append(f"{day_code}_{start_time}{end_time}")

                    data.at[index, "class_time_number"] = ", ".join(extracted_values)

            except Exception as e:
                print(f"에러 발생: {e}")
                data.at[index, "class_time_number"] = ""  # 에러 발생 시 해당 행을 빈 값("")으로 설정

        ##############################################################

        # 현재 CSV 파일의 데이터를 누적하여 추가
        merged_data = pd.concat([merged_data, data], ignore_index=True)

# 결과를 하나의 CSV 파일로 저장
merged_data.to_csv(output_file, encoding="ansi", index=False)
