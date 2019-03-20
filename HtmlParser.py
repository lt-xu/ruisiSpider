# encoding: utf-8
'''
@author: ltxu
@file: HtmlParser.py
@time: 19-3-20 下午10:05
@desc:
'''

from lxml import etree


class HtmlParser:
    def parser(self,page_url, html_cont):  #html_cont下载的网页内容
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
            if span.xpath('child::*'):     #最近发布的文章,会如此显示:<span><span title="2019-3-18">前天&nbsp;17:26</span></span>
                time = span.xpath('./span')[0].attrib['title']
            else:
                time = span.text

            # print(author, time)
            new_titles.append({'title':title, 'article_url':article_url, 'author':author, 'time': time})

        return new_titles







if __name__ == '__main__':
    from HtmlDownloader import HtmlDownloader
    for i in range(1,5):
        page_url = 'http://rs.xidian.edu.cn/forum.php?mod=forumdisplay&fid=560&page={}'.format(i)
        html = HtmlDownloader().download(page_url)
        test = HtmlParser()
        new_titles = test.parser(page_url,html_cont=html)
        print(new_titles)

