# encoding: utf-8
'''
@author: ltxu
@file: SpiderMan.py
@time: 19-3-21 上午9:05
@desc: 爬虫控制器
'''

from HtmlParser import HtmlParser
from HtmlDownloader import HtmlDownloader
from URLManager import URLManager
from WebPageSaver import WebPageSaver, FAIL, DONE, TIMEOUT
import traceback
import os
import time

class SpiderMan:
    def __init__(self):
        self.manager = URLManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.saver = WebPageSaver()

    def crawl(self, root_url, dir_path, old_urls_file=None, timeout_file=None, fail_file=None):
        '''
        爬取网页的主方法
        :param root_url: 根URL 通常是睿思某一板块的第一页,最好按发布时间排序
        :param dir_path: 保存路径不支持中文及其他非英文语言
        :param old_urls_file: 保存旧URL的文件 pkl格式
        :param timeout_file:  保存超时的文件 为方便查看 最好为txt文件
        :param fail_file:   保存失败的文件 为方便查看 最好为txt文件
        :return:
        '''
        count_DONE = 0
        timeout_list = []
        fail_list = []
        saver_login_flag = False
        page_url = root_url

        #检查文件路径
        if not old_urls_file:
            old_urls_file = os.path.join(os.getcwd(), 'old_urls.pkl')
        if not timeout_file:
            timeout_file = os.path.join(os.getcwd(), 'timeout_list_'+time.strftime("%Y_%d_%b_%H_%M_%S", time.localtime()) + ".txt" )
        if not fail_file:
            fail_file = os.path.join(os.getcwd(), 'fail_list_'+time.strftime("%Y_%d_%b_%H_%M_%S", time.localtime()) + ".txt" )

        try:
            while page_url:
                self.manager.old_urls = self.manager.load_progress(old_urls_file)
                html_cont = self.downloader.download(page_url)
                new_articles = self.parser.parse_article(page_url, html_cont)
                new_articles_urls = [article['article_url'] for article in new_articles]
                self.manager.add_new_urls(new_articles_urls)

                while self.manager.new_urls_size():
                    new_url = self.manager.get_new_url()
                    print(new_url)

                    if not saver_login_flag:
                        self.saver.login()
                        saver_login_flag = True

                    status = self.saver.saveWebPage(new_url, dir_path=dir_path)
                    if status == FAIL:
                        fail_list.append(new_url)
                    elif status == DONE:
                        count_DONE += 1
                        self.manager.add_old_url(new_url)
                    elif status == TIMEOUT:
                        timeout_list.append(new_url)
                    # break

                self.manager.save_progress(path=old_urls_file, data=self.manager.old_urls)
                page_url = self.parser.parse_next_page(page_url, html_cont)
        except:
            traceback.print_exc()
        finally:
            self.manager.save_progress(path=old_urls_file, data=self.manager.old_urls)
            print("爬取结束,共爬取{}篇文章,成功{}篇,失败{}篇,保存超时{}篇".format(len(timeout_list)+count_DONE+len(fail_list),
                                                             count_DONE,len(fail_list), len(timeout_list)))
            print('fail_list:', fail_list)
            print('timeout_list:', timeout_list)
            with open(fail_file, 'a+') as f:
                for fail_url in fail_list:
                    f.write(fail_url + "\n")
            with open(timeout_file, 'a+') as f:
                 for fail_url in timeout_list:
                     f.write(fail_url + "\n")
            self.saver.close_webdriver()




if __name__ == '__main__':
    spider = SpiderMan()
    root_url = ''
    dir_path = "/home/ltxu/PycharmProjects/ruisiSpider/saved_pages"
    old_urls_file = "/home/ltxu/PycharmProjects/ruisiSpider/old_urls.pkl"
    spider.crawl(root_url, dir_path, old_urls_file)