# encoding: utf-8
'''
@author: ltxu
@file: URLManager.py
@time: 19-3-20 下午6:50
@desc:
'''

import hashlib
import pickle


class URLManager(object):
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def has_new_url(self):
        return self.new_urls_size()!=0
    def get_new_url(self):
        new_url = self.new_urls.pop()
        # m = hashlib.md5()
        # m.update(new_url.encode(encoding="utf-8"))
        # new_url_md5 = m.hexdigest()[8:-8]
        # self.old_urls.add(new_url_md5)
        return new_url
    def add_old_url(self, url):
        if url is None:
            return
        m = hashlib.md5()
        m.update(url.encode(encoding="utf-8"))
        url_md5 = m.hexdigest()[8:-8]
        self.old_urls.add(url_md5)

    def add_new_url(self,url):
        if url is None:
            return
        m = hashlib.md5()
        m.update(url.encode(encoding="utf-8"))
        url_md5 = m.hexdigest()[8:-8]
        if url not in self.new_urls and url_md5 not in self.old_urls:
            self.new_urls.add(url)
    def add_new_urls(self,urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)
    def new_urls_size(self):
        return len(self.new_urls)
    def old_url_size(self):
        return len(self.old_urls)

    def save_progress(self, path, data):
        '''
        保存进度
        :param path:文件路径
        :param data:数据
        :return:
        '''
        with open(path, 'wb') as f:
            pickle.dump(data, f)

    def load_progress(self, path):
        '''
        从本地文件加载进度
        :param path:文件路径
        :return:返回set集合
        '''
        print('[+] 从文件加载进度: %s' % path)
        try:
            with open(path, 'rb') as f:
                tmp = pickle.load(f)
                return tmp
        except:
            print('[!] 无进度文件, 创建: %s' % path)
        return set()

if __name__ == '__main__':
    urls = ['abc','bcd']
    a = URLManager()
    a.add_new_urls(urls)
    print(a.get_new_url())
    print(a.old_urls,a.new_urls)