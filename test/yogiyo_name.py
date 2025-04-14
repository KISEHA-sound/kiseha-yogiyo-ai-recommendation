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

# ✅ 페이지 접속
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

time.sleep(3)

# ✅ 스크롤 내려 음식점 목록 더 로딩
print("📜 음식점 리스트 더 불러오기 (스크롤)")
for i in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    print(f"  ↪️ 스크롤 {i+1}/5")

# ✅ 음식점 이름 수집
restaurants = []
print("📦 음식점 정보 수집 중...")
try:
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "restaurant-name")))
    rows = driver.find_elements(By.CLASS_NAME, "restaurant-name")
    print(f"🔎 발견된 음식점 수: {len(rows)}개")

    for row in rows:
        name = row.text.strip()
        if name:
            restaurants.append({"name": name})
            print(f"✅ 수집됨: {name}")
except Exception as e:
    print(f"❌ 음식점 수집 실패: {e}")

driver.quit()

# ✅ JSON 저장
filename = "yogiyo_restaurants_by_review.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(restaurants, f, ensure_ascii=False, indent=2)

print(f"\n🎉 음식점 {len(restaurants)}개 수집 완료 → '{filename}' 저장됨")
