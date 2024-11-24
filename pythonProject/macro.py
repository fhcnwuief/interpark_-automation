import time
import easyocr
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys


# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 크롬 드라이버 생성
driver = webdriver.Chrome(options=chrome_options)

# 페이지 로딩이 완료될 때 까지 기다리는 코드
driver.implicitly_wait(3)

# 사이트 접속하기
driver.get(url='https://ticket.interpark.com/Gate/TPLogin.asp')

# <<로그인>>

# 에러 수정
# 필요한 정보들이 Iframe에 존재(전체 Frame과는 별개)
# driver를 Iframe으로 교체
iframes = driver.find_elements(By.TAG_NAME, "iframe")
driver.switch_to.frame(iframes[0])

# css 요소 찾기(1) - id 입력
id_input = driver.find_element(By.CSS_SELECTOR,'#userId')
# 여기에 개인정보 삽입
id_input.send_keys("******")
time.sleep(1)
# css 요소 찾기(2) - pw 입력
pw_input = driver.find_element(By.CSS_SELECTOR,'#userPwd')
# 여기에 개인정보 삽입
pw_input.send_keys("******")
time.sleep(1)
# button 클릭
button = driver.find_element(By.CSS_SELECTOR,'#btn_login')
button.click()
time.sleep(1)

#<<공연 사이트 접근>>
my_url = "https://tickets.interpark.com/goods/24002862" # 링크 나중에 수정
driver.get(my_url)
time.sleep(0.3)

# 닫기 버튼 클릭
button = driver.find_element(By.XPATH, "//*[@id='popup-prdGuide']/div/div[3]/button")
button.click()
time.sleep(1)

#<<날짜 선택>>
want_day = 23
find_day = driver.find_element(By.XPATH, "//li[text()='"+str(want_day)+"']")
find_day.click()

#<<예매하기 버튼>>
go_button = driver.find_element(By.CSS_SELECTOR, "a.sideBtn.is-primary")
go_button.click()

# 최대 10초간 팝업 창이 나타날 때까지 대기
wait = WebDriverWait(driver, 10)
wait.until(EC.number_of_windows_to_be(2))  # 예상하는 창의 개수를 설정합니다. 이 경우에는 2개의 창이 되어야 합니다.

# 모든 창 핸들을 가져옵니다.
window_handles = driver.window_handles

# 현재 창의 핸들을 가져옵니다.
current_window_handle = driver.current_window_handle
print('current_window_handle',current_window_handle)
# 새로 열린 창 핸들을 찾습니다.
new_window_handle = None
for handle in window_handles:
    if handle != current_window_handle:
        new_window_handle = handle
        break

# 새로 열린 창으로 이동합니다.
if new_window_handle:
    driver.switch_to.window(new_window_handle)
else:
    print("새로운 창이 열리지 않았습니다.")

# 아이프레임으로 이동
print(driver.current_window_handle)
driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="ifrmSeat"]'))



# 좌석 탐색
def select():
    print(driver.window_handles)
    print(driver.current_window_handle)
    driver.switch_to.window(driver.window_handles[-1])
    driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="ifrmSeat"]'))

    # 좌석등급 선택
    driver.find_element(By.XPATH,'//*[@id="GradeRow"]/td[1]/div/span[2]').click() # 여기도 수정 필요

    while True:
        # 세부 구역 선택
        driver.find_element(By.XPATH, '//*[@id="GradeDetail"]/div/ul/li[1]/a').click() # 여기도 수정 필요

        # 좌석선택 아이프레임으로 이동
        driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="ifrmSeatDetail"]'))

        # 좌석이 있으면 좌석 선택
        try:
            driver.find_element(By.XPATH, '//*[@id="Seats"]').click()
            # 결제 함수 실행
            payment()
            print('select payment')
            break

        # 좌석이 없으면 다시 조회
        except:
            print('******************************다시선택')
            driver.switch_to.default_content()
            driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="ifrmSeat"]'))
            driver.find_element(By.XPATH, '/html/body/form[1]/div/div[1]/div[3]/div/p/a/img').click()
            time.sleep(1)


# 결제하기
def payment():
    # 좌석선택 완료 버튼 클릭
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="ifrmSeat"]'))
    driver.find_element(By.XPATH, '//*[@id="NextStepImage"]').click()

    # 가격선택
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmBookStep']"))
    select = Select(driver.find_element(By.XPATH, '//*[@id="PriceRow001"]/td[3]/select'))
    select.select_by_index(1)
    driver.switch_to.default_content()
    driver.find_element(By.XPATH, '//*[@id="SmallNextBtnImage"]').click()

    # 예매자 확인
    driver.switch_to.frame(driver.find_element(By.XPATH, "//*[@id='ifrmBookStep']"))
    driver.find_element(By.XPATH, '//*[@id="YYMMDD"]').send_keys('생년월일 입력')
    driver.switch_to.default_content()
    driver.find_element(By.XPATH, '//*[@id="SmallNextBtnImage"]').click()

    # 결제방식 선택
    driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="ifrmBookStep"]'))
    driver.find_element(By.XPATH, '//*[@id="Payment_22004"]/td/input').click()

    select2 = Select(driver.find_element(By.XPATH, '//*[@id="BankCode"]'))
    select2.select_by_index(1)
    driver.switch_to.default_content()
    driver.find_element(By.XPATH, '//*[@id="SmallNextBtnImage"]').click()

    # 동의 후, 결제하기
    driver.switch_to.frame(driver.find_element(By.XPATH, '//*[@id="ifrmBookStep"]'))
    driver.find_element(By.XPATH, '//*[@id="checkAll"]').click()
    driver.switch_to.default_content()
    driver.find_element(By.XPATH, '//*[@id="LargeNextBtnImage"]').click()



# 부정예매방지문자 OCR 생성
reader = easyocr.Reader(['en'])

# 부정예매방지 문자 이미지 요소 선택
capchaPng = driver.find_element(By.XPATH, '//*[@id="imgCaptcha"]')

# 부정예매방지문자 입력
while capchaPng:
    result = reader.readtext(capchaPng.screenshot_as_png, detail=0)
    capchaValue = result[0].replace(' ', '').replace('5', 'S').replace('0', 'O').replace('$', 'S').replace(',', '') \
        .replace(':', '').replace('.', '').replace('+', 'T').replace("'", '').replace('`', '') \
        .replace('1', 'L').replace('e', 'Q').replace('3', 'S').replace('€', 'C').replace('{', '').replace('-', '')

    # 입력
    driver.find_element(By.XPATH, '//*[@id="divRecaptcha"]/div[1]/div[3]').click()
    chapchaText = driver.find_element(By.XPATH, '//*[@id="txtCaptcha"]')
    chapchaText.send_keys(capchaValue)

    # 입력완료 버튼 클릭
    driver.find_element(By.XPATH, '//*[@id="divRecaptcha"]/div[1]/div[4]/a[2]').click()

    # 입력이 잘 됐는지 확인하기
    display = driver.find_element(By.XPATH, '//*[@id="divRecaptcha"]').is_displayed()
    # 입력 문자가 틀렸을 때 새로고침하여 다시입력
    if display:
        driver.find_element(By.XPATH, '//*[@id="divRecaptcha"]/div[1]/div[1]/a[1]').click()
    # 입력 문자가 맞으면 select 함수 실행
    else:
        print('we can select now')
        select()
        break

# 3초 시간제한 이후 드라이버 종료
# time.sleep(3)
# driver.quit()
