from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import tempfile

options = Options()
options.binary_location = "/usr/bin/google-chrome"
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--headless=new')  # VM 호환성 위해 최신 headless 모드 사용

# 충돌 방지를 위한 임시 유저 디렉토리 생성
import tempfile
user_data_dir = tempfile.mkdtemp(prefix="chrome-profile-")
options.add_argument(f'--user-data-dir={user_data_dir}')

driver = webdriver.Chrome(options=options)
driver.get("https://www.google.com")
print("✅ 크롬 실행 성공!")
driver.quit()
