# encoding: utf-8
'''
@author: ltxu
@file: HtmlParser.py
@time: 19-3-20 下午10:05
@desc:   网页分析器
'''

from lxml import etree


class HtmlParser:
    def parse_article(self,page_url, html_cont):  #html_cont下载的网页内容
        '''

        :param page_url:
        :param html_cont:
        :return:
        '''
        html = etree.HTML(html_cont)
        new_titles = []
        tbodys = html.xpath('//*[@id="threadlisttableid"]/tbody[contains(@id,"normalthread")]')
        for tbody in tbodys:
            a = tbody.xpath('.//tr/th/a')[1]
            title = a.text
            # print(title)
            href = a.attrib['href']
            article_url = 'http://rs.xidian.edu.cn/' + href
            author = tbody.xpath('.//tr/td[@class="by"]/cite/a')[0].text

            span = tbody.xpath('.//tr/td[@class="by"]/em/span')[0]
            if span.xpath('child::*'):     # 最近发布的文章,会如此显示:<span><span title="2019-3-18">前天&nbsp;17:26</span></span>
                time = span.xpath('./span')[0].attrib['title']
            else:
                time = span.text

            # print(author, time)
            new_titles.append({'title':title, 'article_url':article_url, 'author':author, 'time': time})

        return new_titles

    def parse_next_page(self, page_url, html_cont):
        '''

        :param page_url:
        :param html_cont:
        :return:
        '''
        html = etree.HTML(html_cont)
        pg = html.xpath('//div[@class="pg"]')[0]
        nxt = pg.xpath('child::a[@class="nxt"]')
        if nxt:
            return 'http://rs.xidian.edu.cn/' + nxt[0].attrib['href']
        else:
            return None


if __name__ == '__main__':
    from HtmlDownloader import HtmlDownloader
    page_url = ''
    while True:
        html = HtmlDownloader().download(page_url)
        test = HtmlParser()
        next_page = test.parse_next_page(page_url,html)
        print(next_page)
        page_url = next_page
        if not next_page:
            break

