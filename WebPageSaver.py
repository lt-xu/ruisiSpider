# encoding: utf-8
'''
@author: ltxu
@file: WebPageSaver.py
@time: 19-3-19 下午11:52
@desc:
'''


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pykeyboard
import os

class WebPageSaver:
    def saveWebPage(self, driver, url, dir_path=None):
        '''
        保存网页
        :param driver: selenium.webdriver
        :param url: 网页url
        :param dir_path: 保存路径不支持中文及其他非英文语言
        :return: None
        '''

        driver.get(url)
        time.sleep(1)

        # 滑到底部
        js = "window.scrollTo(0,document.body.scrollHeight)"
        driver.execute_script(js)
        time.sleep(1)

        # webdriver.ActionChains尝试失败
        # webdriver.ActionChains(drivo[er).key_down(Keys.CONTROL).send_keys("S").key_up(Keys.CONTROL).perform() #失败
        # webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform() #成功

        # 检查路径
        str = ""  # str为保存路径,受k.type_string()方法的限制，位置只能为英文
        if dir_path:
            if dir_path[-1] != "/":
                dir_path += '/'
        str += dir_path
        # 检查文件夹是否存在
        if not os.path.exists(str):
            print("path does not exist!->" + str + ' url:' + url)
            return
        # 检查是否有重名网页
        if os.path.exists(str + driver.title + '.html'):
            print('web page exists!->' + str + driver.title + '.html url:' + url)
            return

        # 实现ctrl s
        k = pykeyboard.PyKeyboard()
        k.press_key(k.control_key)
        k.press_key("s")
        k.release_key("s")
        k.release_key(k.control_key)
        time.sleep(1)

        # 键入路径
        k.tap_key(k.home_key)
        k.type_string(str)  # 只能是键盘上有的字母数字
        time.sleep(1)
        k.tap_key(k.enter_key)
        print("saving web page: " + str + driver.title + ".html")

        # 检查是否保存成功，若10s内未成功则退出
        for i in range(100):
            time.sleep(0.1)
            if os.path.exists(str + driver.title + '.html'):
                print("saved successfully!")
                break
        else:
            print("save failly!->" + str + driver.title + '.html url:' + url)


if __name__ == '__main__':
    drive = webdriver.Firefox()
    url = r"http://rs.xidian.edu.cn/forum.php?mod=viewthread&tid=979023"
    webpage_saver = WebPageSaver()
    webpage_saver.saveWebPage(drive, url, dir_path="/home/ltxu/PycharmProjects/ruisiSpider/saved_pages")
    drive.close()