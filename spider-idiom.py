#!/usr/bin/env python
# coding=utf-8

"""
@Author       : Li Baoyan
@Date         : 2020-02-15 11:08:48
@Github       : https://github.com/This-username-is-available
@LastEditTime : 2020-02-27 12:01:20
@LastEditors  : Li Baoyan
@Description  : 
"""


import asyncio
import bs4
import aiohttp
import json


def flat(nums):
    res = []
    for i in nums:
        if isinstance(i, list):
            res.extend(flat(i))
        else:
            res.append(i)
    return res


async def main(pn, pool):  # 启动
    async with aiohttp.ClientSession() as session:  # 给所有的请求，创建同一个session
        sem = asyncio.Semaphore(pool)
        tasks = []
        for x in range(pn):
            task = asyncio.ensure_future(fetch(session, x, sem))
            tasks.append(task)
        a = await asyncio.gather(*tasks)
        return a


async def fetch(session, pn, sem):  # 开启异步请求
    async with sem:
        url = "https://hanyu.baidu.com/s"
        params = {"wd": "成语", "pn": str(pn)}
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
        }

        async with session.get(url, params=params, headers=headers, timeout=10) as resp:
            idiom_html = await resp.text("utf-8", "ignore")
            idiom_html = bs4.BeautifulSoup(idiom_html, "lxml")
            idioms = idiom_html.find_all(name="a", class_="check-red")
            idioms = [idiom.contents[0].string.strip() for idiom in idioms]
            print(idioms)
            return idioms


loop = asyncio.get_event_loop()
a = loop.run_until_complete(main(1546, 10))
a = flat(a)
with open("idiom.json", "w") as idiom_file:
    json.dump(a, idiom_file, ensure_ascii=False)
loop.close()
