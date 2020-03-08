#!/usr/bin/env python
# coding=utf-8

"""
@Author       : Li Baoyan
@Date         : 2020-02-27 17:52:32
@Github       : https://github.com/This-username-is-available
@LastEditTime : 2020-02-27 18:31:36
@LastEditors  : Li Baoyan
@Description  : 
"""


#!/usr/bin/env python
# coding=utf-8

"""
@Author       : Li Baoyan
@Date         : 2020-02-15 11:08:48
@Github       : https://github.com/This-username-is-available
@LastEditTime : 2020-02-26 18:16:24
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


def update_dicts(a):
    b = {}
    for x in a:
        b.update(x)
    return b


def get_def(idiom_html):
    try:
        passage_texts = (
            bs4.BeautifulSoup(idiom_html, "lxml")
            .find(name="div", class_="content means imeans", id="basicmean-wrapper")
            .find(name="div", class_="tab-content")
            .find_all(name=["p", "dt"])
        )
        a = "".join(
            [passage_text.contents[0].string.strip() for passage_text in passage_texts]
        ).replace("\n", "")
        return a
    except:
        try:
            passage_texts = (
                bs4.BeautifulSoup(idiom_html, "lxml")
                .find(name="div", class_="content", id="baike-wrapper")
                .find(name="div", class_="tab-content")
                .find_all(name=["p", "dt"])
            )
            a = (
                "".join(
                    [passage_text.contents[0].string for passage_text in passage_texts]
                )
                .replace(" ", "")
                .replace("\n", "")
            )
            return a
        except:
            return False


async def main(idioms, pool):  # 启动
    async with aiohttp.ClientSession() as session:  # 给所有的请求，创建同一个session
        sem = asyncio.Semaphore(pool)
        tasks = []
        for idiom in idioms:
            task = asyncio.ensure_future(fetch(session, idiom, sem))
            tasks.append(task)
        a = await asyncio.gather(*tasks)
        return a


async def fetch(session, idiom, sem):  # 开启异步请求
    async with sem:
        while True:
            try:
                if get_def(idiom):
                    output_idiom = {idiom: get_def}
                else:
                    output_idiom = {idiom: "wtfsmg"}
            except:
                pass
        print(output_idiom)
        return output_idiom


with open("idiom.json", "r", encoding="utf-8") as idiom_file:
    idioms = json.load(idiom_file)
loop = asyncio.get_event_loop()
a = loop.run_until_complete(main(idioms, 20))
a = update_dicts(a)
with open("definition.json", "w", encoding="utf-8") as idiom_file:
    json.dump(a, idiom_file, ensure_ascii=False)
loop.close()
