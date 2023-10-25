import sys
import io
import csv
import pandas as pd
import os

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding="utf-8")

# 디렉토리 경로
directory_path = "./"

# 불러올 파일명과 경로
course_data_file = "merged_course_data.csv"
user_timetable_file = ""

filepath = os.path.join(directory_path, course_data_file)
course_data = pd.read_csv(filepath, encoding="ansi")


# 합칠 CSV 파일들이 들어있는 디렉토리 경로
# directory_path = "./"

# # 결과를 저장할 파일명과 경로
# output_file = "merged_course_data.csv"

# # 빈 DataFrame 생성
# merged_data = pd.DataFrame()

# # 디렉토리 내의 모든 CSV 파일에 대해 반복
# for filename in os.listdir(directory_path):
#     if filename.endswith(".csv") and filename.startswith("course_data"):
#         # CSV 파일을 DataFrame으로 읽어오기
#         filepath = os.path.join(directory_path, filename)
#         data = pd.read_csv(filepath, encoding="ansi")

#         # 현재 CSV 파일의 데이터를 누적하여 추가
#         merged_data = pd.concat([merged_data, data], ignore_index=True)

# # 결과를 하나의 CSV 파일로 저장
# merged_data.to_csv(output_file, encoding="ansi", index=False)
