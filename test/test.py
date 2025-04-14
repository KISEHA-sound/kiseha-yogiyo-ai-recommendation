from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)
driver.get("https://www.yogiyo.co.kr/mobile/#/246690")  # 예시: 롯데리아-남부터미널점

time.sleep(3)  # Angular 초기 렌더링 대기

# ✅ "클린리뷰" 탭 클릭
try:
    review_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[@ng-click="toggle_tab(\'review\')"]'))
    )
    review_tab.click()
    print("✅ 리뷰 탭 클릭 완료")
except:
    print("❌ 리뷰 탭 클릭 실패")
    driver.quit()

# ✅ 리뷰 로딩 기다림
time.sleep(2)

# ✅ 리뷰 텍스트 추출
reviews = []
try:
    review_elements = driver.find_elements(By.XPATH, '//p[@ng-show="review.comment"]')
    for r in review_elements[:20]:  # 최신 20개만
        reviews.append({"text": r.text})
except Exception as e:
    print("❌ 리뷰 추출 실패:", e)

driver.quit()

# ✅ JSON 저장
with open("reviews_lotteria.json", "w", encoding="utf-8") as f:
    json.dump(reviews, f, ensure_ascii=False, indent=2)

print("🎉 저장 완료! 리뷰 수:", len(reviews))
