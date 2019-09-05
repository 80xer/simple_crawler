# =*-coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
from functools import reduce
import json
import csv
import datetime as dt
import os

now = dt.datetime.now()
# Mock User Agent
HEADER = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encodoing': 'gzip, deflate',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0'
}


def get_html(url: str):
    resp = requests.get(url, headers=HEADER)
    if resp.status_code == 200:
        return resp.text
    return ""


def template_generater(keywords, templates):
    generated = {}
    for idx, (key, val) in enumerate(templates.items()):
        generated[key] = list(map(lambda x: (x, val + x), keywords))
    return generated


def crawl_naver_blog(urls):
    page = 5
    _answer = []
    for keyword, url in urls:
        for elem in range(page):
            _html = get_html(url+"&start=" + str(elem*10+1))  # pagenation
            _soup = bs(_html, 'html.parser')
            _blocks = _soup.find_all("li", {"class": "sh_blog_top"})
            for _block in _blocks:
                _answer.append(naver_blog_block(keyword, _block))
    x = json.loads(json.dumps(_answer))
    f = csv.writer(open(os.path.dirname(os.path.abspath(__file__)) +
                        "/["+now.strftime("%m_%d_%H")+"]_naver_blog.csv", "w", newline=""))
    f.writerow(["date", "source", "keyword", "title",
                "passage", "author", "count", "link"])
    for x in x:
        f.writerow([x["date"], x["source"], x["keyword"], x["title"],
                    x["passage"], x["author"], x["count"], x["link"]])
    return


def string_date_to_number_date(str_date):
    if '일 전' in str_date:
        days = int(str_date[:str_date.index("일 전")])
        str_date = dt.datetime.today() - dt.timedelta(days=days)
    elif '시간 전' in str_date:
        hours = int(str_date[:str_date.index("시간 전")])
        str_date = dt.datetime.today() - dt.timedelta(hours=hours)
    elif '어제' in one['date']:
        str_date = dt.datetime.today() - dt.timedelta(days=1)
    else:
        return str_date
    return str_date.strftime("%Y.%m.%d.")


def naver_blog_block(keyword, _block):
    one = {}
    one['date'] = _block.find("dd", {"class": "txt_inline"}).string
    one['date'] = string_date_to_number_date(one['date'])
    one['source'] = 'naver_blog'
    one['keyword'] = keyword
    one['title'] = _block.find(
        "a", {"class": "sh_blog_title _sp_each_url _sp_each_title"}).contents
    one['title'] = list(map(lambda x: str(x.string) if hasattr(
        x, 'string') else str(x), one['title']))
    one['title'] = reduce(lambda x, y: x + y, one['title'])
    one['passage'] = _block.find("dd", {"class": "sh_blog_passage"}).contents
    one['passage'] = list(map(lambda x: str(x.string) if hasattr(
        x, 'string') else str(x), one['passage']))
    one['passage'] = reduce(lambda x, y: x + y, one['passage'])
    one['author'] = _block.find("a", {"class": "txt84"}).string
    one['count'] = "-1"
    one['link'] = _block.find("a", {"class": "url"})["href"]
    return one


def crawl_naver_cafe(urls):
    page = 5
    answer = []
    for keyword, url in urls:
        for elem in range(page):
            html = get_html(url+"&start=" + str(elem*10+1))  # pagenation
            soup = bs(html, 'html.parser')
            blocks = soup.find_all("li", {"class": "sh_cafe_top"})
            for block in blocks:
                answer.append(naver_cafe_block(keyword, block))
    x = json.loads(json.dumps(answer))
    f = csv.writer(open(os.path.dirname(os.path.abspath(__file__)) +
                        "/["+now.strftime("%m_%d_%H")+"]_naver_cafe.csv", "w", newline=""))
    f.writerow(["date", "source", "keyword", "title",
                "passage", "author", "count", "link"])
    for x in x:
        f.writerow([x["date"], x["source"], x["keyword"], x["title"],
                    x["passage"], x["author"], x["count"], x["link"]])
    return


def naver_cafe_block(keyword, _block):
    one = {}
    one['date'] = _block.find("dd", {"class": "txt_inline"}).string
    one['date'] = string_date_to_number_date(one['date'])
    one['source'] = 'naver_cafe'
    one['keyword'] = keyword
    one['title'] = _block.find("a", {"class": "sh_cafe_title"}).contents
    one['title'] = list(map(lambda x: str(x.string) if hasattr(
        x, 'string') else str(x), one['title']))
    one['title'] = reduce(lambda x, y: x + y, one['title'])
    one['passage'] = _block.find("dd", {"class": "sh_cafe_passage"}).contents
    one['passage'] = list(map(lambda x: str(x.string) if hasattr(
        x, 'string') else str(x), one['passage']))
    one['passage'] = reduce(lambda x, y: x + y, one['passage'])
    one['author'] = _block.find("a", {"class": "txt84"}).string
    one['count'] = "-1"  # implement
    one['link'] = _block.find("a", {"class": "url"})["href"]
    return one


def crawl_daum_cafe(urls):
    page = 5
    _answer = []
    for keyword, url in urls:
        for elem in range(page):
            _html = get_html(url+"&p=" + str(elem+1))
            _soup = bs(_html, 'html.parser')
            _blocks = _soup.find("div", {"id": "cafeColl"}).find_all(
                "div", {"class": "cont_inner"})
            for _block in _blocks:
                _answer.append(daum_cafe_block(keyword, _block))
    x = json.loads(json.dumps(_answer))
    f = csv.writer(open(os.path.dirname(os.path.abspath(__file__)) +
                        "/["+now.strftime("%m_%d_%H")+"]_daum_cafe.csv", "w", newline=""))
    f.writerow(["date", "source", "keyword", "title",
                "passage", "author", "count", "link"])
    for x in x:
        f.writerow([x["date"], x["source"], x["keyword"], x["title"],
                    x["passage"], x["author"], x["count"], x["link"]])
    return


def daum_cafe_block(keyword, _block):
    one = {}
    one['date'] = _block.find("span", {"class": "f_nb date"}).string
    one['source'] = 'daum_cafe'
    one['keyword'] = keyword
    one['title'] = _block.find("a", {"class": "f_link_b"}).contents
    one['title'] = list(map(lambda x: str(x.string) if hasattr(
        x, 'string') else str(x), one['title']))
    one['title'] = reduce(lambda x, y: x + y, one['title'])
    one['passage'] = _block.find("p", {"class": "f_eb desc"}).contents
    one['passage'] = list(map(lambda x: str(x.string) if hasattr(
        x, 'string') else str(x), one['passage']))
    one['passage'] = reduce(lambda x, y: x + y, one['passage'])
    # cafe/nick 의 형태로 implement 필요
    one['author'] = _block.find("a", {"class": "f_nb"}).string
    one['count'] = "-1"
    one['link'] = _block.find("a", {"class": "f_url"})["href"]
    return one


def crawl_dcinside(urls):
    _answer = []
    for keyword, url in urls:
        _html = get_html(url)
        _soup = bs(_html, 'html.parser')
        _blocks = _soup.find("table", {"class": "gall_list"}).find(
            "tbody").find_all("tr", {"class": "ub-content us-post"})
        for _block in _blocks:
            _answer.append(dcinside_block(keyword, _block))
    x = json.loads(json.dumps(_answer))
    print("dc")
    f = csv.writer(open(os.path.dirname(os.path.abspath(__file__)) +
                        "/["+now.strftime("%m_%d_%H")+"]_dc.csv", "w", newline=""))
    f.writerow(["date", "source", "keyword", "title",
                "passage", "author", "count", "link", "ip"])
    for x in x:
        f.writerow([x["date"], x["source"], x["keyword"], x["title"],
                    x["passage"], x["author"], x["count"], x["link"], x["ip"]])
    return


def dcinside_block(keyword, _block):
    one = {}
    _writer = _block.find("td", {"class": "gall_writer ub-writer"})
    _title = _block.find("td", {"class": "gall_tit ub-word"}).find("a")
    one['date'] = _block.find("td", {"class": "gall_date"}).string
    one['source'] = 'dcinside_toeic'
    one['keyword'] = keyword
    one['title'] = _title.contents[1]
    one['passage'] = "-1"  # implement
    one['author'] = _writer.contents[1]['title']
    one['count'] = _block.find("td", {"class": "gall_count"}).string
    one['link'] = _title["href"]
    one['ip'] = _writer['data-ip']
    return one

if __name__ == "__main__":
    with open('templates.json') as t:
        templates = json.load(t)
    with open('keywords.json') as k:
        keywords = json.load(k)
    generated = template_generater(keywords['keywords'], templates)
    for elem in generated.keys():
        crawl_func = locals()['crawl_'+elem]
        print(elem)
        crawl_func(generated[elem])
