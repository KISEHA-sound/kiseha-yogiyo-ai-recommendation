from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time, json, tempfile

# ✅ 셀레니움 옵션 설정
options = Options()
options.add_argument('--headless=new')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--remote-debugging-port=9222')

# ✅ 임시 사용자 디렉토리 생성
user_data_dir = tempfile.mkdtemp()
options.add_argument(f'--user-data-dir={user_data_dir}')

print("🚀 크롬 실행 중...")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

print("🌐 요기요 메인 페이지 접속 중...")
driver.get("https://www.yogiyo.co.kr/mobile/#/")
time.sleep(3)

# ✅ 위치 주소 입력
try:
    print("📍 위치 입력 중...")
    address_input = wait.until(EC.presence_of_element_located((By.NAME, "address_input")))
    address_input.clear()
    address_input.send_keys("서울특별시 서초구 서초동 1498-5 위대한상상")
    time.sleep(1)
    address_input.send_keys(Keys.ENTER)
    print("✅ 위치 입력 및 엔터 완료")
except Exception as e:
    print(f"❌ 위치 입력 실패: {e}")

time.sleep(3)

# ✅ 드롭다운에서 '리뷰 많은 순' 선택
try:
    print("🔍 정렬 드롭다운 클릭 대기 중...")
    드롭다운 = wait.until(EC.element_to_be_clickable((By.XPATH, '//select[@ng-model="session_storage.restaurant_list_sort_order"]')))
    드롭다운.click()
    Select(드롭다운).select_by_value("review_count")
    print("✅ 리뷰 많은 순 선택 완료")
except Exception as e:
    print(f"❌ 드롭다운 처리 실패: {e}")

# ✅ 음식점 스크롤 로딩
print("📜 음식점 리스트 더 불러오기 (스크롤)")
for i in range(10):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    print(f"  ↪️ 스크롤 {i+1}/10")

# ✅ 음식점 카드 클릭 후 리뷰 수집
print("🌟 음식점 클릭 & 리뷰 수집 시작")
reviews_data = []

cards = driver.find_elements(By.CSS_SELECTOR, ".item.clearfix")
print(f"🔍 총 {len(cards)}개 음식점 발견")

for idx in range(45, 50):
    try:
        cards = driver.find_elements(By.CSS_SELECTOR, ".item.clearfix")
        card = cards[idx]
        driver.execute_script("arguments[0].scrollIntoView(true);", card)
        card.click()
        print(f"➡️ {idx+1}번째 음식점 클릭")

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "restaurant-name")))
        상점명 = driver.find_element(By.CLASS_NAME, "restaurant-name").text
        print(f"✅ 상세 페이지 접속: {상점명}")

        # ✅ 클린리뷰 탭 클릭
        try:
            print("🔽 클린리뷰 탭 클릭 중...")
            리뷰탭 = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//a[contains(text(),'클린리뷰')]")
            ))
            driver.execute_script("arguments[0].scrollIntoView(true);", 리뷰탭)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'클린리뷰')]"))).click()
            time.sleep(2)
        except Exception as e:
            print(f"❌ 클린리뷰 탭 클릭 실패: {e}")
            raise e

        # ✅ 리뷰 더 보기 클릭 반복 (최대 5번)
        for _ in range(5):
            try:
                more_btn = driver.find_element(By.CSS_SELECTOR, "li.btn-more a")
                driver.execute_script("arguments[0].scrollIntoView(true);", more_btn)
                more_btn.click()
                print("🔄 더 보기 클릭!")
                time.sleep(1.5)
            except:
                print("⛔ 더 보기 버튼 없음 (혹은 끝까지 도달)")
                break

        # ✅ 리뷰 수집
        리뷰들 = driver.find_elements(By.CSS_SELECTOR, 'p[ng-show="review.comment"]')
        print(f"📝 리뷰 {len(리뷰들)}개 수집 중")

        for r in 리뷰들[:20]:
            reviews_data.append({
                "store": 상점명,
                "review": r.text.strip()
            })

        driver.back()
        time.sleep(2)

    except Exception as e:
        print(f"⚠️ 오류 발생: {e}")
        driver.back()
        time.sleep(2)

# ✅ 크롬 종료 및 결과 저장
driver.quit()
with open("yogiyo_reviews_result1_10.json", "w", encoding="utf-8") as f:
    json.dump(reviews_data, f, ensure_ascii=False, indent=2)

print("\n🎉 리뷰 수집 완료 → 'yogiyo_reviews_result1_10.json' 저장됨")