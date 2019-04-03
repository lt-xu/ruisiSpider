# encoding: utf-8
'''
@author: ltxu
@file: HtmlDownloader.py
@time: 19-3-20 下午6:37
@desc: 网页下载器
'''

import requests

class HtmlDownloader:
    def download(self,url):
        '''

        :param url:
        :return:
        '''
        if url is None:
            return None
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers={'User-Agent':user_agent}
        r = requests.get(url,headers=headers)
        if r.status_code==200:
            r.encoding='utf-8'
            return r.text
        return None


if __name__ == '__main__':
    test = HtmlDownloader()
    result = test.download('')
    print(result)