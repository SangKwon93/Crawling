
import csv
from getpass import getpass
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# 트위터 데이터 추출 함수
def get_tweet_data(block):
    block =driver.find_element(By.CSS_SELECTOR,'div.css-1dbjc4n')
    username = block.find_element(By.XPATH,'//div[@data-testid="User-Names"]').text.split('\n')[0]
    handle= block.find_element(By.XPATH,'//div[@data-testid="User-Names"]').text.split('\n')[1]
    try:
        post_date = block.find_element(By.XPATH,'.//time').get_attribute('datetime')
    except NoSuchElementException:
        return
    content = block.find_element(By.XPATH,'.//div[@data-testid="tweetText"]').text
    reply_count = block.find_element(By.XPATH,'.//div[@data-testid="reply"]').text
    retweet_count=block.find_element(By.XPATH,'.//div[@data-testid="retweet"]').text
    likes_count=block.find_element(By.XPATH,'.//div[@data-testid="like"]').text

    tweet=(username,handle,post_date,content,reply_count,retweet_count,likes_count)
    return tweet

# driver 생성하기
def get_chrome_driver():
 
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), # 가장 많이 바뀐 부분
        options=options
    )
    return driver


driver = get_chrome_driver()
driver.get('http://www.twitter.com/login')
driver.maximize_window()
# time.sleep(10)
ID='apfhda7@gmail.com'
PN=getpass()
PW=getpass()

# 아이디 입력 구간에 마우스 가져다 놓기
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]')))
login_cursor =driver.find_element(By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]')
login_cursor.click()

# ID 입력
xpath_id='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input'
id_input = driver.find_element(By.XPATH,xpath_id)
id_input.send_keys(ID)

# 다음 입력
xpath_next= '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]'
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_next)))
next = driver.find_element(By.XPATH,xpath_next)
next.click()

# 폰번호 입력
xpath_phone = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input'
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_phone)))
phone=driver.find_element(By.XPATH,xpath_phone)
phone.click()
phone_input =driver.find_element(By.XPATH,xpath_phone)
phone_input.send_keys(PN)

# 로그인 enter
xpath_enter = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input'
enter = driver.find_element(By.XPATH,xpath_enter)
enter.send_keys(Keys.ENTER)

# 비밀번호 입력
xpath_pw='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_pw)))
pw=driver.find_element(By.XPATH,xpath_pw)
pw.send_keys(PW)

# 두번째 엔터
enter2=driver.find_element(By.XPATH,xpath_pw)
enter2.send_keys(Keys.RETURN)

# 검색
xpath_search='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input'
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath_search)))
search_input=driver.find_element(By.XPATH,xpath_search)

search_input.send_keys('#tesla')
search_input.send_keys(Keys.RETURN)

# 최신순 탭
xpath_latest='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]/a/div/div/span'
driver.find_element(By.XPATH,xpath_latest).click()


# 트위터 데이터 리스트에 넣기
data=[]
tweet_ids=set()
last_position=driver.execute_script("return window.pageYOffset;")
scrolling=True

while scrolling :
    articles=driver.find_elements(By.XPATH,'//div[@data-testid="cellInnerDiv"]')
    #time.sleep(2)
    for article in articles[-3:]:
        tweet=get_tweet_data(article)
        if tweet:
            tweet_id=''.join(tweet)
            if tweet_id not in tweet_ids:
                tweet_ids.add(tweet_id)
                data.append(tweet)

    # 스크롤 작동
    scroll_action=0

    # 스크롤 최적화
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        time.sleep(2)
        current_position= driver.execute_script("return window.pageYOffset;")
        if last_position==current_position:
            scroll_action +=1

            if scroll_action >=3:
                scrolling= False
                break
            else:
                time.sleep(2)
        else:
            last_position=current_position
            break


# csv 파일로 저장하기
with open('tesla.csv','w',newline='',encoding="utf-8") as f:
    header=['username','handle','time','content','likes','retweets',"reply"]
    writer=csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)

driver.quit()