from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json

# ✅ 크롬 드라이버 옵션 설정 (리눅스 서버용)
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # 최신 방식의 headless
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# ✅ 드라이버 실행
driver = webdriver.Chrome(options=chrome_options)

# ✅ 타겟 URL (요기요 BHC 경북왜관점)
url = "https://www.yogiyo.co.kr/mobile/#/323861/"
driver.get(url)

# ✅ 페이지 로딩 대기
time.sleep(5)

# ✅ 스크롤 내리면서 리뷰 수집
reviews = set()
scroll_attempts = 0

while len(reviews) < 100 and scroll_attempts < 20:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    elements = driver.find_elements(By.CSS_SELECTOR, "p.ng-binding")
    for e in elements:
        text = e.text.strip()
        if text:
            reviews.add(text)
    scroll_attempts += 1

# ✅ 드라이버 종료
driver.quit()

# ✅ JSON 파일 저장
review_list = [{"text": r} for r in list(reviews)[:100]]

with open("bhc_reviews.json", "w", encoding="utf-8") as f:
    json.dump(review_list, f, ensure_ascii=False, indent=2)

print("✅ 크롤링 완료! 리뷰 개수:", len(review_list))
