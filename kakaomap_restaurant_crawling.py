import os
from time import sleep
import time
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 서울특별시 구 리스트
gu_list = ['마포구','서대문구','은평구','종로구','중구','용산구','성동구','광진구',
           '동대문구','성북구','강북구','도봉구','노원구','중랑구','강동구','송파구',
           '강남구','서초구','관악구','동작구','영등포구','금천구','구로구','양천구','강서구']

def page_loop(i):
    # i번째 페이지 열기
    for k in range(10): #만약 에러가 뜬다면 어디서 어떤 문제인지 출력, 에러 안뜰때까지 최대 10번 반복한다.
        try:
            xPath = '//*[@id="info.search.page.no' + str(i) + '"]'
            page = driver.find_element_by_xpath(xPath)
            break
        except Exception as e:
            print("ERROR : ",e," -> redo")
            time.sleep(1) #기다려주자
    for k in range(10): #만약 에러가 뜬다면 어디서 어떤 문제인지 출력, 에러 안뜰때까지 최대 10번 반복한다.
        try:
            page.send_keys(Keys.ENTER)
            time.sleep(1) #기다려주자
            break
        except Exception as e:
            print("ERROR : ",e," -> redo")
            time.sleep(1) #기다려주자
            
    place_lists = driver.find_elements_by_css_selector('#info\.search\.place\.list > li') # 현재 페이지의 장소 리스트 생성
 
    for k in range(1, len(place_lists)+1): # 각 장소에 대해서 xpath로 내부 살펴보고 긁어오기
                
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#info\.search\.place\.list > li:nth-child(' + str(i) + ')'))) # 기다려 주자
    
        try: # 식당이름이 존재?
            name_xPath = '//*[@id="info.search.place.list"]/li['+str(k)+']/div[3]/strong/a[2]' # 식당이름
            driver.find_element_by_xpath(name_xPath) #존재하지 않는다면 여기서 에러 발생
        except NoSuchElementException: # 식당이름이 존재하지 않는다면 광고임
            continue #광고는 넘어간다
                        
        try: #아이콘[광고]가 뜨는 xpath가 존재?
            if driver.find_element_by_xpath('//*[@id="info.search.place.list"]/li['+str(k)+']/div[3]/strong/a[2]/span'): # 맨위에 뜨는 광고 맛집은 패스
                name_xPath = '//*[@id="info.search.place.list"]/li['+str(k)+']/div[3]/strong/a[2]' # 식당이름
                name = driver.find_element_by_xpath(name_xPath).get_attribute("innerText")[2:] #[광고]제외하고 식당이름만 저장
        except NoSuchElementException: #존재하지 않는다면
            name_xPath = '//*[@id="info.search.place.list"]/li['+str(k)+']/div[3]/strong/a[2]' # 식당이름
            name = driver.find_element_by_xpath(name_xPath).get_attribute("innerText")
            pass #계속한다.
                    
        category_xPath = '//*[@id="info.search.place.list"]/li['+str(k)+']/div[3]/span' # 구분
        category = driver.find_element_by_xpath(category_xPath).get_attribute("innerText")
        rating_xPath = '//*[@id="info.search.place.list"]/li['+str(k)+']/div[4]/span[1]/em' # 평점
        rating = driver.find_element_by_xpath(rating_xPath).get_attribute("innerText")
        address_xPath = '//*[@id="info.search.place.list"]/li['+str(k)+']/div[5]/div[2]/p[1]' # 주소 # 서울 외 지역 나올수도
        address = driver.find_element_by_xpath(address_xPath).get_attribute("innerText")
        openhours_xPath = '//*[@id="info.search.place.list"]/li['+str(k)+']/div[5]/div[3]/p/a' # 영업시간 # 현재 기준
        openhours = driver.find_element_by_xpath(openhours_xPath).get_attribute("innerText")
        phoneNum_xPath = '//*[@id="info.search.place.list"]/li['+str(k)+']/div[5]/div[4]/span[1]' # 전화번호
        phoneNum = driver.find_element_by_xpath(phoneNum_xPath).get_attribute("innerText")
        scoreCnt_xPath = '//*[@id="info.search.place.list"]/li['+str(k)+']/div[4]/span[1]/a' #리뷰수
        scoreCnt = driver.find_element_by_xpath(scoreCnt_xPath).get_attribute("innerText")
                    
        # 데이터 마이닝? 문자열 안에 ,가 있다면 /로 바꿔주기
        if(name.find(',')!=-1): 
            name = name.replace(',','/')
        if(category.find(',')!=-1):
            category = category.replace(',','/')
        if(rating.find(',')!=-1):
            rating = rating.replace(',','/')
        if(address.find(',')!=-1):
            address = address.replace(',','/')
        if(openhours.find(',')!=-1):
            openhours = openhours.replace(',','/')
        if(phoneNum.find(',')!=-1):
            phoneNum = phoneNum.replace(',','/')
        if(scoreCnt.find(',')!=-1):
            scoreCnt = scoreCnt.replace(',','')
                            
        file = open(fileName, 'a', encoding='utf-8')
        file.write(name + "," + category + "," + str(rating) + "," + address + "," + openhours + "," + phoneNum + "," + scoreCnt + "\n")
        file.close()


###################### main함수: 구 별로 검색하기 ######################
for index, gu_name in enumerate(gu_list):
    fileName = gu_name + 'kakaomap_restaurant.csv'
    file = open(fileName, 'w', encoding='utf-8')
    file.write("식당이름" + "," + "구분" + "," + "평점" + "," + "주소" + "," + "영업시간" + "," + "전화번호" + "," + "리뷰수" + "," + "별점건수" + "\n")
    file.close()

    options = webdriver.ChromeOptions()
    options.add_argument('lang=ko_KR')
    chromedriver_path = "C:/Users/dnflc/Downloads/selenium/chromedriver.exe"
    driver = webdriver.Chrome(os.path.join(os.getcwd(), chromedriver_path), options=options)  # chromedriver 열기
    driver.get('https://map.kakao.com/')  # 주소 가져오기
    search_area = driver.find_element_by_xpath('//*[@id="search.keyword.query"]') # 검색 창
    search_area.send_keys(gu_name + ' 맛집')  # 검색어 입력
    driver.find_element_by_xpath('//*[@id="search.keyword.submit"]').send_keys(Keys.ENTER)  # Enter로 검색
    driver.implicitly_wait(0.5) # 기다려 주자
    driver.find_element_by_xpath('//*[@id="info.search.place.more"]').send_keys(Keys.ENTER) # 장소 더보기 누르기
    driver.implicitly_wait(0.5) # 기다려 주자
    # 두 번째 페이지로 이동하게 됨

    # '>' 버튼 찾기
    next_btn = driver.find_element_by_xpath('//*[@id="info.search.page.next"]')

    #카카오맵의 검색결과는 최대 34페이지까지 출력됨
    next_btn_cnt = 6
    last_page_cnt = 4
    
    for j in range(next_btn_cnt+1): # '>'가 있으면 루프를 돈다.(마지막 페이지면 돌지 않는다.)
        if j == next_btn_cnt : # 마지막 info.search.page일 경우
            for i in range(1, last_page_cnt+1): # 존재하는 페이지까지만 돌려준다.
                page_loop(i)
            print('[' , j*5+1 , '-'  , j*5+i , '] 완료') # ex) [31-34] 완료
        else : # 마지막이 아니면
            for i in range(1, 6): # 1~5페이지
                page_loop(i)
            print('[' , j*5+1 , '-'  , j*5+i , '] 완료') # ex) [6-10] 완료
                   
        try: 
            next_btn.send_keys(Keys.ENTER) # '>'버튼 클릭, 6~10페이지로 이동하게 됨
        except NoSuchElementException: #버튼이 존재하지 않는다면
            continue #넘어간다

    print("End of Crawl of ", gu_name)
    driver.close()
driver.quit()