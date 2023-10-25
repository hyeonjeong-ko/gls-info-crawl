import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os
import subprocess

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

# options = webdriver.ChromeOptions()
# options.add_experimental_option("excludeSwitches", ["enable-logging"])


# csv저장 파일 생성
filename = "everytime_info.csv"
# 파일이 존재하지 않으면 새로 만들기
if not os.path.exists(filename):
    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        title = "전공영역1	전공영역2	구분	학수번호-분반	교과목명	교수	시간	학점	담은 인원	정원	비고".split("\t")
        writer.writerow(title)


browser = webdriver.Chrome(options=options)

# everytime 시간표로 이동
browser.get("https://everytime.kr/timetable")

time.sleep(4)

# 로그인
id = "toyu7870"
pw = "rhguswjd125"

import pyperclip

browser.execute_script("document.getElementsByName('userid')[0].value ='" + id + "'")
browser.execute_script("document.getElementsByName('password')[0].value ='" + pw + "'")


time.sleep(3)

# 체크박스 엘리먼트를 찾음 (이 부분은 웹 페이지의 HTML 구조에 따라 다를 수 있음)
# checkbox = browser.find_element(By.XPATH, '//*[@id="recaptcha-anchor"]/div[1]')
# WebDriverWait를 사용하여 체크박스가 클릭 가능할 때까지 기다림


loginbtn = browser.find_element(By.XPATH, '//*[@id="container"]/form/p[3]/input')

WebDriverWait(browser, 20).until(
    EC.frame_to_be_available_and_switch_to_it(
        (By.CSS_SELECTOR, "iframe[title='reCAPTCHA']")
    )
)
WebDriverWait(browser, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.recaptcha-checkbox-border"))
).click()


time.sleep(6)

loginbtn.click()


try:
    searchbtn = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "search"))
    )  # 입력창이 뜰 때까지 대기
finally:
    pass


searchbtn.click()
time.sleep(6)

# 전공,영역 클릭
browser.find_element(By.XPATH, '//*[@id="subjects"]/div[1]/a[3]').click()


# ===========================
soup = BeautifulSoup(browser.page_source, "lxml")
cate1 = soup.find_all("li", attrs={"class": "parent"})
print(len(cate1))

# 상위카테고리 선택
for cate1 in range(1, len(cate1) + 1):
    if cate1 < 19:
        continue
    try:
        cate_first = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="subjectCategoryFilter"]/div/ul/li[{}]'.format(cate1),
                )
            )
        )  # 입력창이 뜰 때까지 대기
    finally:
        pass
    # 전공영역1 저장
    catetxt = cate_first.text

    if catetxt in allowed_categories:
        try:
            # ex_소프트웨어 융합 대학 클릭
            cate_first.click()

            # 하위카테고리 li 갯수 확인
            soup = BeautifulSoup(browser.page_source, "lxml")
            child = soup.find("ul", attrs={"class": "unfolded"}).find_all(
                "li", attrs={"class": "child"}
            )
            cate_len = len(child)

            # category-하위전공 선택(반복선택작업)
            for i in range(1, cate_len + 1):
                major = browser.find_element(
                    By.XPATH,
                    '//*[@id="subjectCategoryFilter"]/div/ul/ul[{}]/li[{}]'.format(
                        cate1, i
                    ),
                ).text

                browser.find_element(
                    By.XPATH,
                    '//*[@id="subjectCategoryFilter"]/div/ul/ul[{}]/li[{}]'.format(
                        cate1, i
                    ),
                ).click()

                time.sleep(7)

                # page 갱신
                # soup = BeautifulSoup(browser.page_source, "lxml")

                # ======
                # div 속 스크롤 모두 내리기 ======
                itemlist = browser.find_element(By.CLASS_NAME, "list")

                verical_ordinate = 100
                for i in range(0, 10):
                    print(verical_ordinate)
                    browser.execute_script(
                        "arguments[0].scrollTop = arguments[1]",
                        itemlist,
                        verical_ordinate,
                    )
                    verical_ordinate += 2500
                    time.sleep(2)

                # div 속 스크롤 모두 내리기 끝
                # page 재 갱신
                soup = BeautifulSoup(browser.page_source, "lxml")
                # ===

                listdiv = soup.find("div", attrs={"class": "list"})
                data_rows = listdiv.find("tbody").find_all("tr")

                # 맵 자료구조에 데이터 추가
                for row in data_rows:
                    columns = row.find_all("td")
                    if len(columns) <= 1:
                        continue
                    data = [column.get_text().strip() for column in columns]
                    data.insert(0, major)  # 전공2 라벨
                    data.insert(0, catetxt)  # 전공1 라벨
                    del data[-4]

                    # 파일이 존재하면 append 모드로 열고, 존재하지 않으면 write 모드로 열어서 데이터 추가
                    with open(
                        filename,
                        "a" if os.path.exists(filename) else "w",
                        encoding="utf-8-sig",
                        newline="",
                    ) as f:
                        writer = csv.writer(f)
                        writer.writerow(data)
                        print(data)
                        print("-" * 50)

        finally:
            pass

            # 전공,영역 클릭
    browser.find_element(By.XPATH, '//*[@id="subjects"]/div[1]/a[3]').click()
