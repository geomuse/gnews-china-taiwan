from dataclasses import dataclass
import requests

from bs4 import BeautifulSoup
import os , sys
import numpy as np

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC

current_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(current_dir, "..\..")
path = r'c:\Users\boonh\Downloads\genv'
sys.path.append(path)

from notification_bot.telegram_chat import telegram_send
from notification_bot.loguru_notification import loguru_notf
logger = loguru_notf(current_dir)
logger.add('streamlit.')

from data_collection_bot.http_status import check_status
import streamlit as st

# 设置Chrome浏览器驱动路径
driver_path = 'C:/Users/boonh/Downloads/genv/data_collection_bot/geckodriver-v0.33.0-linux64'

@dataclass
class news_download:
    def init_browser(self):
        service = Service(executable_path=driver_path)
        options = webdriver.FirefoxOptions()
        return service , options

    def run(self,url):
        # service , options = self.init_browser()
        browser = webdriver.Firefox()
        browser.get(url)

    def get_one(self,url):
        response = requests.get(url)
        if check_status(response.status_code) in [200]:
            soup = BeautifulSoup(response.text,'html.parser')
            title  = soup.find_all('ul',{'class':'list'})
            a_link = soup.find_all('a',{'class','listS_h'})
            text = f"{title[0].text}"
            link = f"{a_link[0].text}"
            text = text.split()
        data1 = []
        for _ , __ in enumerate(text):
            data1.append(__)
            print(link)
        return data1
    
    def get_two(self,url):
        response = requests.get(url)
        if check_status(response.status_code) in [200]:
            soup = BeautifulSoup(response.text,'html.parser')
            title = soup.find_all('div',{'class':'part_pictxt_3 lazyload'})
            text = f"{title[0].text}"
            text = text.split()
        data2 = []
        for _ , __ in enumerate(text):
            data2.append(__)    
        return data2
    
    def get_three(self,url):
        response = requests.get(url)
        if check_status(response.status_code) in [200]:
            soup = BeautifulSoup(response.text,'html.parser')
            title = soup.find_all('ul',{'class':'list'})
            # text = f"{title[0].text}"
            sub_soup = BeautifulSoup(str(title),'html.parser')
            sub = sub_soup.find_all('a',{'class':'ph'})
            print(sub)
        sub_data = []
        for _ , __ in enumerate(sub):
            sub_data.append(__)
        return sub_data

@dataclass    
class shiny:
    def init_streamlit(self,data,title):
        st.title(title)
        st.dataframe(data, width=1000, height=700)
        st.write('.')
        
if __name__ == '__main__':

    url1 = 'https://news.ltn.com.tw/list/breakingnews/world'
    url2 = 'https://www.ettoday.net/news/focus/%E5%9C%8B%E9%9A%9B/'
    url3 = 'https://news.ltn.com.tw/list/breakingnews/world'
    nd = news_download()
    s = shiny()

    data1 = nd.get_one(url1)
    data2 = nd.get_two(url2)
    data3 = nd.get_three(url3)

    col1 , col2 , col3 = st.columns(3)

    with col1:
        s.init_streamlit(data1,'自由时报.')
    
    with col2:
        s.init_streamlit(data2,'ettdoys.')

    with col3:
        s.init_streamlit(data3,'自由时报.')

    ts = telegram_send()
    ts.send_message('200.')

    