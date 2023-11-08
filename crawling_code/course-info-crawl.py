from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

import sys
import io

import csv

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding="utf-8")


def are_arrays_equal(arr1, arr2):
    # Check if dimensions are the same
    if len(arr1) != len(arr2):
        return False

    # Check each element in corresponding positions
    for i in range(len(arr1)):
        if arr1[i] != arr2[i]:
            return False

    return True


file_name_index = 1
data = []
major_data = []

last_rows = []
tmp_rows = []


def extract_course_info(browser, college_name, major):
    global last_rows
    global tmp_rows

    tmp_rows = []

    rows = browser.find_elements(By.CSS_SELECTOR, "#nexacontainer .GridRowControl")

    # 각 Row들에 대해 data 저장 작업
    for idx, row in enumerate(rows):
        if idx > 10:
            elements = row.find_elements(
                By.CSS_SELECTOR, ".nexacontentsbox.nexacenteralign"
            )

            course_name = None
            professor = None
            class_time = None

            for i, element in enumerate(elements):
                if i == 1:
                    class_code = element.text
                if i == 2:
                    course_name = element.text
                if i == 3:
                    professor = element.text
                if i == 6:
                    class_time = element.text
                if i == 7:
                    class_type = element.text

            if major and course_name and professor and class_time:
                if major == "에너지과학연계전공" or major == "인공지능융합전공":
                    class_type = ""
                elif major == "데이터사이언스융합전공":
                    class_type = "일반수업"
                if [
                    major,
                    course_name,
                    professor,
                    class_time,
                ] not in data:
                    data.append(
                        [
                            class_code,
                            college_name,
                            major,
                            course_name,
                            professor,
                            class_time,
                            class_type,
                        ]
                    )
                    tmp_rows.append(
                        [
                            class_code,
                            college_name,
                            major,
                            course_name,
                            professor,
                            class_time,
                            class_type,
                        ]
                    )

                    print(
                        "data row:",
                        class_code,
                        college_name,
                        major,
                        course_name,
                        professor,
                        class_time,
                        class_type,
                    )

    return data


# 카테고리 리스트
allowed_categories = [
    ## "공과대학",
    ## "사회과학대학",
    ## "생명공학대학",
    ## "성균나노과학기술원",
    "성균융합원",
    ## "소프트웨어대학",
    ## "소프트웨어융합대학",
    ## "스포츠과학대학",
    ## "약학대학",
    ## "의과대학",
    ## "자연과학대학",
    ## "정보통신대학",
    ## "학부대학",
]


chrome_browser = subprocess.Popen(
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe "
    r"--remote-debugging-port=9222 "
    r'--user-data-dir="C:\Temp\chrome"'
)

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--ignore-certificate-errors")
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
options.add_argument(
    "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36"
)

browser = webdriver.Chrome(options=options)

browser.get(
    "https://kingoinfo.skku.edu/gaia/nxui/outdex.html?language=KO&menuId=NHSSU030840M"
)

time.sleep(5)


# BeautifulSoup을 사용하여 페이지 소스 파싱
soup = BeautifulSoup(browser.page_source, "html.parser")

# 학사-전공과목 클릭
target_tag = browser.find_element(
    By.XPATH,
    "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[5]/div/div/div/div[1]/div/div[4]/div",
)

if target_tag:
    target_tag.click()
    print("학사 전공 과목 클릭")

time.sleep(2)

# 자연과학버튼 오디오 클릭
audio_button = browser.find_element(
    By.XPATH,
    "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[3]/div/div[5]/div/div[3]/div/div[2]/div/div/div/div[5]/div/div[2]/div/img",
)

audio_button.click()

print("오디오 버튼 클릭")


view_button = browser.find_element(
    By.XPATH,
    "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[3]/div/div[5]/div/div[3]/div/div[2]/div/div/div/div[8]/div",
)

view_button.click()  # 조회 버튼 클릭


# arrow 더보기 버튼 클릭
arrowbtn = browser.find_element(
    By.XPATH,
    "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[3]/div/div[5]/div/div[3]/div/div[2]/div/div/div/div[9]/div/div[2]/div",
)
arrowbtn.click()


# 드롭다운에서 모든 태그 가져오기
dropdown_tags = browser.find_elements(By.XPATH, '//*[@id="nexacontainer"]/*')

univ_tag_list = []
for index, tag in enumerate(dropdown_tags, start=1):
    univ_tag_list.append(tag.text)

# 각 태그의 텍스트 및 인덱스 출력 / 수행작업
for index, tag in enumerate(univ_tag_list, start=1):
    tag_text = tag
    # 자연 과학 캠퍼스 학부만 선택
    if tag_text and (tag_text in allowed_categories):  # 학부마다
        data = []
        major_data = []
        전달txt = tag_text
        print("Tag", index, "Text:", tag_text)

        # arrow 더보기 버튼 클릭
        arrowbtn = browser.find_element(
            By.XPATH,
            "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[3]/div/div[5]/div/div[3]/div/div[2]/div/div/div/div[9]/div/div[2]/div",
        )
        arrowbtn.click()

        univ_input_btn = browser.find_element(
            By.XPATH,
            "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[3]/div/div[5]/div/div[3]/div/div[2]/div/div/div/div[9]/div/div[1]/input",
        )

        univ_input_btn.clear()
        college_name = tag_text.replace(" ", "")
        univ_input_btn.send_keys(college_name)
        univ_input_btn.send_keys(Keys.RETURN)  # enter!

        time.sleep(3)

        # 세부 학부 드롭다운 클릭
        drop_button = browser.find_element(
            By.XPATH,
            "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[3]/div/div[5]/div/div[3]/div/div[2]/div/div/div/div[10]/div/div[2]/div",
        )

        drop_button.click()

        department_elements = browser.find_elements(
            By.CSS_SELECTOR, ".combolist .nexacontentsbox"
        )

        print(f"{tag_text} 대학 세부 학부 목록:")
        for element in department_elements:
            department_name = element.text
            if department_name:
                major_data.append(department_name)
                print("세부전공명:", department_name)

        # major
        for idx, major in enumerate(major_data):
            scroll_count = 0

            print(
                "##################################### 크롤링시작-major #####################################:",
                major,
            )
            major_name = major.lstrip()
            print("major_name:", major_name)

            # 세부 학부 드롭다운 클릭
            drop_button = browser.find_element(
                By.XPATH,
                "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[3]/div/div[5]/div/div[3]/div/div[2]/div/div/div/div[10]/div/div[2]/div",
            )

            drop_button.click()

            time.sleep(2)

            mdiv = browser.find_element(
                By.XPATH,
                "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[3]/div/div[5]/div/div[3]/div/div[2]/div/div/div/div[10]",
            )
            # 세부 학부 드롭다운 클릭
            mdiv.click()

            if idx != 0:
                mdiv.send_keys(Keys.ARROW_DOWN)
                mdiv.send_keys(Keys.RETURN)

            view_button.click()  # 조회 버튼 클릭
            view_button.click()  # 조회 버튼 클릭
            rows = browser.find_elements(
                By.CSS_SELECTOR, "#nexacontainer .GridRowControl"
            )

            time.sleep(8)

            view_button.click

            extract_course_info(browser, college_name, major)  # 동적로딩한 것들을 스크래핑

            # Check if the scrollbar exists
            try:
                scrollbar_div = browser.find_element(
                    By.XPATH,
                    "/html/body/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div/div/div/div[1]/div/div/div/div[3]/div/div[5]/div/div[3]/div/div[1]/div[3]/div/div[2]/div",
                )

                while scroll_count < 170:  # Scroll 200 times
                    print("스크롤 내리기 시작")
                    # Arrow 스크롤 내리기
                    for i in range(10):
                        scrollbar_div.click()
                    time.sleep(2)

                    extract_course_info(browser, college_name, major)
                    last_rows = tmp_rows
                    scroll_count += 10

            except:
                print("스크롤바 없음.")
            print(
                "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
            )

            print(len(data))
            print(
                "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
            )
            print("scraping 완료")

        # CSV file path
        csv_file_path = f"major_course_data/course_data_{college_name}.csv"

        # Write the data to a CSV file
        with open(csv_file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "class_code",
                    "college_name",
                    "department_name",
                    "course_name",
                    "professor",
                    "class_time",
                    "class_type",
                ]
            )  # Write header
            for row_data in data:
                writer.writerow(row_data)

        print("Data saved to:", csv_file_path)

        file_name_index += 1

browser.quit()
