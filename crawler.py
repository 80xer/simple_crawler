# =*-coding: utf-8 -*-

import requests
from typing import Optional
from bs4 import BeautifulSoup as bs
from functools import reduce
import json
import datetime as dt
from pprint import pprint

now = dt.datetime.now()
# Mock User Agent HEADER
HEADER = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encodoing": "gzip, deflate",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0",
}

NAVER_BLOG_PAGE_NUM = 1
NAVER_CAFE_PAGE_NUM = 1
DAUM_CAFE_PAGE_NUM = 1

NAVER_BLOG = "naver_blog"
NAVER_CAFE = "naver_cafe"
DAUM_CAFE = "daum_cafe"


def get_html(url: str) -> Optional[str]:
    resp = requests.get(url, headers=HEADER)
    if resp.status_code == 200:
        return resp.text
    return None


def crawl_naver_blog_per_keyword(url: str, keyword: str, page: int) -> list:
    r = []
    for num in range(page):
        html = get_html(url + "&start=" + str(num * 10 + 1))
        soup = bs(html, "html.parser")
        blocks = soup.find_all("li", {"class": "sh_blog_top"})
        r.extend([naver_blog_block(keyword, b) for b in blocks])
    return {keyword: r}


def crawl_naver_blog(url: str, keywords: list) -> list:
    page = NAVER_BLOG_PAGE_NUM
    return [crawl_naver_blog_per_keyword(url + k, k, page) for k in keywords]


def date_string_to_number(str_date):
    if "일 전" in str_date:
        days = int(str_date[: str_date.index("일 전")])
        str_date = dt.datetime.today() - dt.timedelta(days=days)
    elif "시간 전" in str_date:
        hours = int(str_date[: str_date.index("시간 전")])
        str_date = dt.datetime.today() - dt.timedelta(hours=hours)
    elif "어제" in str_date:
        str_date = dt.datetime.today() - dt.timedelta(days=1)
    else:
        return str_date
    return str_date.strftime("%Y.%m.%d.")


def naver_blog_block(keyword, _block):
    one = {}
    one["date"] = _block.find("dd", {"class": "txt_inline"}).string
    one["date"] = date_string_to_number(one["date"])
    one["source"] = "naver_blog"
    one["keyword"] = keyword
    one["title"] = _block.find(
        "a", {"class": "sh_blog_title _sp_each_url _sp_each_title"}
    ).contents
    one["title"] = list(
        map(lambda x: str(x.string) if hasattr(x, "string") else str(x), one["title"])
    )
    one["title"] = reduce(lambda x, y: x + y, one["title"])
    one["passage"] = _block.find("dd", {"class": "sh_blog_passage"}).contents
    one["passage"] = list(
        map(lambda x: str(x.string) if hasattr(x, "string") else str(x), one["passage"])
    )
    one["passage"] = reduce(lambda x, y: x + y, one["passage"])
    one["author"] = _block.find("a", {"class": "txt84"}).string
    one["link"] = _block.find("a", {"class": "url"})["href"]
    return one


def crawl_naver_cafe_per_keyword(url: str, keyword: str, page: int) -> list:
    r = []
    for num in range(page):
        html = get_html(url + "&start=" + str(num * 10 + 1))
        soup = bs(html, "html.parser")
        blocks = soup.find_all("li", {"class": "sh_cafe_top"})
        r.extend([naver_cafe_block(keyword, b) for b in blocks])
    return {keyword: r}


def crawl_naver_cafe(url, keywords):
    page = NAVER_CAFE_PAGE_NUM
    return [crawl_naver_cafe_per_keyword(url + k, k, page) for k in keywords]


def naver_cafe_block(keyword, _block):
    one = {}
    one["date"] = _block.find("dd", {"class": "txt_inline"}).string
    one["date"] = date_string_to_number(one["date"])
    one["source"] = "naver_cafe"
    one["keyword"] = keyword
    one["title"] = _block.find("a", {"class": "sh_cafe_title"}).contents
    one["title"] = list(
        map(lambda x: str(x.string) if hasattr(x, "string") else str(x), one["title"])
    )
    one["title"] = reduce(lambda x, y: x + y, one["title"])
    one["passage"] = _block.find("dd", {"class": "sh_cafe_passage"}).contents
    one["passage"] = list(
        map(lambda x: str(x.string) if hasattr(x, "string") else str(x), one["passage"])
    )
    one["passage"] = reduce(lambda x, y: x + y, one["passage"])
    one["author"] = _block.find("a", {"class": "txt84"}).string
    one["link"] = _block.find("a", {"class": "url"})["href"]
    return one


def crawl_daum_cafe_per_keyword(url: str, keyword: str, page: int) -> list:
    r = []
    for num in range(page):
        url = url + keyword
        html = get_html(url + "&p=" + str(num + 1))
        soup = bs(html, "html.parser")
        blocks = soup.find("div", {"id": "cafeColl"}).find_all(
            "div", {"class": "cont_inner"}
        )
        r.extend([daum_cafe_block(keyword, b) for b in blocks])
    return {keyword: r}


def crawl_daum_cafe(url, keywords):
    page = DAUM_CAFE_PAGE_NUM
    return [crawl_daum_cafe_per_keyword(url + k, k, page) for k in keywords]


def daum_cafe_block(keyword, _block):
    one = {}
    one["date"] = _block.find("span", {"class": "f_nb date"}).string
    one["source"] = "daum_cafe"
    one["keyword"] = keyword
    one["title"] = _block.find("a", {"class": "f_link_b"}).contents
    one["title"] = list(
        map(lambda x: str(x.string) if hasattr(x, "string") else str(x), one["title"])
    )
    one["title"] = reduce(lambda x, y: x + y, one["title"])
    one["passage"] = _block.find("p", {"class": "f_eb desc"}).contents
    one["passage"] = list(
        map(lambda x: str(x.string) if hasattr(x, "string") else str(x), one["passage"])
    )
    one["passage"] = reduce(lambda x, y: x + y, one["passage"])
    one["author"] = _block.find("a", {"class": "f_nb"}).string
    one["link"] = _block.find("a", {"class": "f_url"})["href"]
    return one


def save_to_dynamo(platform: str, results: list):
    return results


if __name__ == "__main__":
    with open("keywords.json") as t:
        keywords = json.load(t)["keywords"]
    switcher = {
        "naver_blog": crawl_naver_blog,
        "naver_cafe": crawl_naver_cafe,
        "daum_cafe": crawl_daum_cafe,
    }
    url = {
        "naver_blog": "https://search.naver.com/search.naver?where=post&sm=tab_jum&query=",
        "naver_cafe": "https://search.naver.com/search.naver?where=article&sm=tab_jum&query=",
        "daum_cafe": "https://search.daum.net/search?w=cafe&nil_search=btn&DA=NTB&enc=utf8&ASearchType=1&lpp=10&rlang=0&q=",
    }
    for key in switcher.keys():
        results = switcher[key](url[key], keywords)
        pprint(save_to_dynamo(key, results))
