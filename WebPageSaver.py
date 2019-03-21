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
import pickle
import re

import traceback

DONE = 1  #保存成功
FAIL = -1 #保存失败
UNDO = 0  #中途退出


class WebPageSaver:

    def __init__(self):
        self.driver = webdriver.Firefox()


    def login(self):
        '''
        登录
        :return:
        '''
        try:
            cookies_file = 'cookie.pkl'
            if not os.path.exists(cookies_file):
                self.driver.get('http://rs.xidian.edu.cn/forum.php')
                print('请在60s内登录成功')
                time.sleep(60)
                print('等待结束')
                cookies = self.driver.get_cookies()
                # print(cookies)
                with open(cookies_file, 'wb') as f:
                    pickle.dump(cookies, f)
                print('cookies saved in ' + cookies_file)
            else:
                with open(cookies_file, 'rb') as f:
                    cookies = pickle.load(f)
                    # print(cookies)

            self.driver.get('http://rs.xidian.edu.cn/forum.php')
            self.driver.delete_all_cookies()

            for cookie in cookies:
                for k in {'name', 'value', 'domain', 'path', 'expiry'}:
                    if k not in list(cookie.keys()):
                        if k == 'expiry':
                            t = time.time()
                            cookie[k] = int(t)  # 时间戳s
                self.driver.add_cookie({k: cookie[k] for k in {'name', 'value', 'domain', 'path', 'expiry'}})

            self.driver.get('http://rs.xidian.edu.cn/forum.php')
        except:
            traceback.print_exc()


    def saveWebPage(self, url, dir_path=None):
        '''
        保存网页
        :param url: 网页url
        :param dir_path: 保存路径不支持中文及其他非英文语言
        :return: 成功保存返回DONE的值 各种原因中途退出返回UNDO的值 保存失败返回FAIL的值
        '''

        try:
            self.driver.get(url)
            time.sleep(1)

            # 滑到底部
            js = "window.scrollTo(0,document.body.scrollHeight)"
            self.driver.execute_script(js)
            time.sleep(1)
        except Exception as e:
            traceback.print_exc()
            return UNDO

        # webdriver.ActionChains尝试失败
        # webdriver.ActionChains(drivo[er).key_down(Keys.CONTROL).send_keys("S").key_up(Keys.CONTROL).perform() #失败
        # webdriver.ActionChains(self.driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).perform() #成功

        # 检查路径
        # str = ""  # str为保存路径,受k.type_string()方法的限制，位置只能为英文
        # if dir_path:
        #     if dir_path[-1] != "/":
        #         dir_path += '/'
        # str += dir_path

        # if not os.path.isdir(dir_path):
        #     print("此路径不是文件夹!->" + dir_path)
        #     return UNDO

        if not re.fullmatch(r'^[A-Za-z0-9 _/.-]+$', dir_path):
            print('存储文件夹名称中只能包含英文字母 数字 "_" "." "-", 您的输入为:' + dir_path)
            return UNDO

        # 检查文件夹是否存在
        if not os.path.exists(dir_path):
            print("文件夹不存在!->" + dir_path)
            os.makedirs(dir_path)
            print("创建文件夹:" + dir_path)

        # 检查是否有重名网页
        if os.path.exists(os.path.join(dir_path, self.driver.title + '.html')):
            print('网页已存在!->' + os.path.join(dir_path, self.driver.title + '.html') + ' url:' + url)
            return UNDO

        try:
            # 实现ctrl s
            k = pykeyboard.PyKeyboard()
            k.press_key(k.control_key)
            k.press_key("s")
            k.release_key("s")
            k.release_key(k.control_key)
            time.sleep(1)

            # 键入路径
            str = os.path.abspath(dir_path) + os.path.sep

            k.tap_key(k.home_key)
            k.type_string(str)  # 只能是键盘上有的字母数字
            time.sleep(1)
            k.tap_key(k.enter_key)
            print("saving web page: " + os.path.join(str, self.driver.title + ".html"))
        except:
            traceback.print_exc()
            return UNDO

        # 检查是否保存成功，若30s内未成功则退出
        for i in range(300):
            time.sleep(0.1)
            if os.path.exists(os.path.join(str, self.driver.title + ".html")):
                print("保存成功!")
                return DONE
        else:
            print("30s内未保存成功!->" + str + self.driver.title + '.html url:' + url)
            return FAIL



    def close_webdriver(self):
        self.driver.close()


if __name__ == '__main__':
    url = r"http://rs.xidian.edu.cn/forum.php?mod=viewthread&tid=979023"
    webpage_saver = WebPageSaver()
    # webpage_saver.login()
    status = webpage_saver.saveWebPage(url, dir_path="/home/ltxu/PycharmProjects/ruisiSpider/test")
    print(status)