import random
import time
from selenium import webdriver
from selenium.webdriver.support import wait
import pyautogui
from urllib import request
from cv2 import cv2
import numpy as np


class Jd:
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def login(self):
        driver.maximize_window()
        driver.get('https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F%3Fcu%3Dtrue')
        self.xpath_find('//*[@id="content"]/div[2]/div[1]/div/div[3]').click()
        self.xpath_send('//*[@id="loginname"]', self.user)
        self.xpath_send('//*[@id="nloginpwd"]', self.password)
        self.xpath_find('//*[@id="loginsubmit"]').click()

    def xpath_find(self, xpath_f):
        wait.WebDriverWait(driver, 5).until(lambda x:x.find_element_by_xpath(xpath_f))
        element = driver.find_element_by_xpath(xpath_f)
        return element

    def xpath_send(self, xpath_f, key):
        wait.WebDriverWait(driver, 5).until(lambda x:x.find_element_by_xpath(xpath_f))
        element = driver.find_element_by_xpath(xpath_f)
        element.send_keys(key)

    def img_down(self):
        bigimg = self.xpath_find('//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[1]/div[2]/div[1]/img').get_attribute('src')
        request.urlretrieve(bigimg, 'big.png')
        smallimg = self.xpath_find('//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[1]/div[2]/div[2]/img').get_attribute('src')
        request.urlretrieve(smallimg, 'small.png')

    def calculate_distance(self):
        big_rgb = cv2.imread('big.png')
        big_gray = cv2.cvtColor(big_rgb, cv2.COLOR_BGR2GRAY)
        small_rgb = cv2.imread('small.png', 0)
        res = cv2.matchTemplate(big_gray, small_rgb, cv2.TM_CCOEFF_NORMED)
        value = cv2.minMaxLoc(res)
        # print(value)
        x = value[2][0]
        return x

    def get_diff_location(self):
        # 获取图片并灰度化
        block = cv2.imread("small.png", 0)
        template = cv2.imread("big.png", 0)
        # 二值化后的图片名称
        blockName = "block.jpg"
        templateName = "template.jpg"
        # 将二值化后的图片进行保存
        cv2.imwrite(blockName, block)
        cv2.imwrite(templateName, template)
        block = cv2.imread(blockName)
        block = cv2.cvtColor(block, cv2.COLOR_RGB2GRAY)
        block = abs(255 - block)
        cv2.imwrite(blockName, block)
        block = cv2.imread(blockName)
        template = cv2.imread(templateName)
        # 获取偏移量
        result = cv2.matchTemplate(block, template,
                                   cv2.TM_CCOEFF_NORMED)  # 查找block在template中的位置，返回result是一个矩阵，是每个点的匹配结果
        x, y = np.unravel_index(result.argmax(), result.shape)
        print(x,y)
        return y

    def slide_by_pyautogui(self, x):
        a = self.xpath_find('//*[@id="JDJRV-wrap-loginsubmit"]/div/div/div/div[2]/div[3]').location
        pyautogui.moveTo(1220, 590, duration=0.1)
        pyautogui.mouseDown()
        # y = 590 + random.randint(9, 19)
        y = 590 + random.gauss(0,3)
        # print(y)
        pyautogui.moveTo(1220 + int(pow(x * x * random.randint(15, 23) / 20, 0.5)), y, duration=(random.randint(20, 31)) / 100)
        y = 590 + random.gauss(0,3)
        pyautogui.mouseUp()
        # pyautogui.moveTo()
        # pyautogui.mouseUp(1220 + int(pow(x * random.randint(17, 21) / 20, 0.5)), y, duration=(random.randint(20, 31)) / 100)
        # y = 590+random.gauss(0,3)
        pyautogui.moveTo(1220+x, duration=0.3)
        pyautogui.mouseUp()

    def run(self):
        self.login()
        while True:
            self.img_down()
            x = self.calculate_distance()
            self.slide_by_pyautogui(x)
            time.sleep(2)
            result = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div/div[4]/div[2]/div').text
            if '不匹配' in result:
                break


if __name__ == '__main__':
    driver = webdriver.Chrome()
    jd = Jd('用户名', '密码')
    jd.run()
    driver.quit()
