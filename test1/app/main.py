from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys  
import time
import pandas as pd


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
driver = webdriver.Chrome('/usr/src/chrome/chromedriver', chrome_options=chrome_options)
url = f'http://121.78.246.85:9090/lc2/'
driver.get(url)
print("url 접속하기")


#intraMainFrame로 이동하기
driver.switch_to.frame('intaMainFrame')
soup = BeautifulSoup(driver.page_source, "html.parser")
login = driver.find_element(By.NAME, "a_id")
login.send_keys("2420000410001")
time.sleep(1)
login.send_keys(Keys.ENTER)
password = driver.find_element(By.NAME, "a_passwd")
password.send_keys("2578")
time.sleep(1)
select_element = driver.find_element(By.NAME, "s_id")
select_object = Select(select_element)
select_object.select_by_value("L00002")
time.sleep(1)
login_button = driver.find_element(By.NAME, "Image1")
login_button.click()
print("로그인 완료")


# 'driver.window_handles'는 현재 열려 있는 모든 창의 핸들(고유 식별자)을 리스트로 반환합니다.
# 이 리스트의 마지막 항목은 가장 최근에 열린 창의 핸들입니다.
new_window_handle = driver.window_handles[-1]

# 'driver.switch_to.window()' 함수를 사용하여 새 창으로 컨텍스트를 전환합니다.
driver.switch_to.window(new_window_handle)

# 이제 새 창의 내부에서 웹 요소를 찾거나 상호 작용할 수 있습니다.
# 예를 들어, 새 창의 제목을 출력할 수 있습니다.
print(driver.title)



driver.switch_to.frame('fr_frame1')
soup = BeautifulSoup(driver.page_source, "html.parser")
soup


from selenium.webdriver.common.action_chains import ActionChains

# "재고관리Ⅱ" 메뉴를 찾습니다.
menu = driver.find_element(By.LINK_TEXT, "재고관리Ⅱ")

# "재고관리Ⅱ" 메뉴에 마우스를 올립니다.
ActionChains(driver).move_to_element(menu).perform()

# 잠시 대기합니다. 메뉴가 완전히 로드될 때까지 시간이 필요할 수 있습니다.
time.sleep(2)

# "쇼핑물품절관리" 메뉴를 찾아 클릭합니다.
submenu = driver.find_element(By.LINK_TEXT, "쇼핑물품절관리")
submenu.click()


driver.switch_to.parent_frame()
driver.switch_to.frame('fr_frame2')


# 총재고 목록에서 데이터 가져오는 버튼 클릭하기
driver.switch_to.frame('fr_fr1')
driver.execute_script("srch()")

time.sleep(120)


driver.switch_to.parent_frame()
driver.switch_to.frame('fr_fr2')
print("데이터 검색")

driver.switch_to.frame('iFrame1')
table_element = driver.find_element(By.XPATH, "//table")
table_html = table_element.get_attribute("outerHTML")
df = pd.read_html(table_html)[0]

column_mapping = {
    0: '등록일',
    1: '제품명',
    2: '규격',
    3: '주문코드',
    4: '합계',
    5: '본사',
    6: '용산허브',
    7: '일산창고'
}

df = df.rename(columns=column_mapping)

columns_to_drop = [8, 9, 10]
df = df.drop(columns=columns_to_drop)

df['합계']  = df["합계"].astype("Int64")
df['본사']  = df["본사"].astype("Int64")
df['용산허브']  = df["용산허브"].astype("Int64")
df['일산창고']  = df["일산창고"].astype("Int64")

from sqlalchemy import create_engine
from urllib.parse import quote_plus
password = quote_plus('!!@Ll752515')

engine = create_engine(f'mysql+pymysql://fred:{password}@fred1234.synology.me/fred')
df.to_sql(name='comsmart_database', con=engine, index=False, if_exists = 'replace')
engine.dispose()