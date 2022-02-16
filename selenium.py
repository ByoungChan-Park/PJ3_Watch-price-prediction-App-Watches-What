from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import csv

#브라우저생성
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome('C:/chromedriver.exe',options=options)
driver.maximize_window()

#URL+page
url ='''https://www.chrono24.kr/search/index.htm?countryIds=US&currencyId=KRW&dosearch=true&manufacturerIds=44&manufacturerIds=27&manufacturerIds=192&manufacturerIds=194&manufacturerIds=252&manufacturerIds=112&manufacturerIds=211&manufacturerIds=236&manufacturerIds=438&manufacturerIds=518&manufacturerIds=30&manufacturerIds=32&manufacturerIds=18&manufacturerIds=187&manufacturerIds=1&manufacturerIds=188&manufacturerIds=221&manufacturerIds=200&manufacturerIds=124&manufacturerIds=168&manufacturerIds=245&manufacturerIds=103&manufacturerIds=127&manufacturerIds=149&manufacturerIds=226&maxAgeInDays=0&pageSize=120&priceFrom=120000&redirectToSearchIndex=true&resultview=block&sortorder=0&year=2012&year=2011&year=2022&year=2010&year=2021&year=2020&year=2019&year=2018&year=2017&year=2016&year=2015&year=2014&year=2013'''
page = '&showpage='

#URL+page리스트 작성
page_list = []
for page_num in list(range(3,179)):
    pages = url+page+str(page_num)
    page_list.append(pages)
    
#data저장할 csv파일 생성
f = open(r"C:/Users/dignd/Section3/practice/project/data3.csv", 'w', encoding='utf-8', newline='')
csvWriter = csv.writer(f)

#url이 page_list안에 있을경우 페이지 접속 > 해당페이지 아이템링크 prod_list에 담기 반복실행(+배너닫기, 스크롤내려서 아이템 로딩)
prod_list = []
for page_url in page_list:
    driver.get(page_url)
    driver.implicitly_wait(1)
    close_btn_xpath = '//a[@class="btn btn-primary btn-full-width js-cookie-submit wt-consent-layer-accept-all gdpr-layer-accept consent-layer-accept"]'
    while True:
        try:
            close_btn = driver.find_element(By.XPATH, close_btn_xpath)
            close_btn.click()
            time.sleep(2)
        except:
            break

    minus_btn_xpath = '//i[@class="i-minus"]'
    while True:
        try:
            minus_btn = driver.find_element(By.XPATH, minus_btn_xpath)
            minus_btn.click()
            time.sleep(2)
        except:
            break

    before_h = driver.execute_script("return window.scrollY") #처음 스크롤위치

    while True:
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END) #스크롤 마지막까지 내리기
        time.sleep(1) #업데이트시간
        after_h = driver.execute_script("return window.scrollY") #내린 후 스크롤 위치
        if after_h == before_h:
            break
        before_h = after_h
    time.sleep(1)

    page = driver.find_elements(By.CSS_SELECTOR,".article-item-container")
    for item in page:        
        try:
            link = item.find_element(By.CSS_SELECTOR,"a").get_attribute('href')
            prod_list.append(link)
        except:
            break

#담긴 아이템링크(prod_list)로 들어가 상세 제원가져오기

for prod in prod_list:
    if prod != 'https://www.chrono24.kr/about-us.htm':
        driver.get(prod)
        try:
            prod_name = driver.find_element(By.CSS_SELECTOR, "#detail-page-dealer > section.data.m-b-6 > div:nth-child(2) > div > div.col-sm-12.col-md-10.m-b-2.m-t-4 > div.media-flex.align-self-start.d-none.d-sm-flex > div.media-flex-body > h1").text
        except:
            prod_name = '정보없음'
        try:
            brand = driver.find_element(By.CSS_SELECTOR, '#jq-specifications > div > div.row.text-lg.m-b-6 > div.col-xs-24.col-md-12.m-b-6.m-b-md-0 > table > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(2) > a').text
        except:
            brand = '정보없음'
        try :
            model = driver.find_element(By.CSS_SELECTOR, "#jq-specifications > div > div.row.text-lg.m-b-6 > div.col-xs-24.col-md-12.m-b-6.m-b-md-0 > table > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(2) > a").text
        except:
            model = '정보없음'
        try:
            component = driver.find_element(By.CSS_SELECTOR, "#jq-specifications > div > div.row.text-lg.m-b-6 > div.col-xs-24.col-md-12.m-b-6.m-b-md-0 > table > tbody:nth-child(1) > tr:nth-child(11) > td:nth-child(2) > div").text
        except:
            component = '정보없음'
        try : 
            movement = driver.find_element(By.CSS_SELECTOR, "#jq-specifications > div > div.row.text-lg.m-b-6 > div.col-xs-24.col-md-12.m-b-6.m-b-md-0 > table > tbody:nth-child(2) > tr:nth-child(2) > td.font-all-content").text
        except:
            movement = "정보없음"
        try :
            glass = driver.find_element(By.CSS_SELECTOR, "#jq-specifications > div > div.row.text-lg.m-b-6 > div.col-xs-24.col-md-12.m-b-6.m-b-md-0 > table > tbody:nth-child(3) > tr:nth-child(6) > td.font-all-content").text
        except :
            try:
                glass = driver.find_element(By.CSS_SELECTOR, "#jq-specifications > div > div.row.text-lg.m-b-6 > div.col-xs-24.col-md-12.m-b-6.m-b-md-0 > table > tbody:nth-child(2) > tr:nth-child(4) > td:nth-child(2)").text
            except : 
                glass = "정보없음"
        try:
            price = driver.find_element(By.CSS_SELECTOR, "#detail-page-dealer > section.data.m-b-6 > div:nth-child(2) > div > div.col-sm-12.col-md-10.m-b-2.m-t-4 > div:nth-child(2) > div.m-b-4 > div.detail-page-price.wt-detail-page-price > span.price-md.m-b-1 > span > span").text
        except:
            price = '정보없음'

        csvWriter.writerow([prod_name, brand, model, component, movement, glass, price])


