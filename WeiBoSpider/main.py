from typing import Dict, Any

import aiohttp
import asyncio
import os
import json
import logging
import time
from aiohttp import ClientResponseError, ClientConnectionError
from urllib.parse import urlparse
from fake_useragent import UserAgent
from utils.save import Save
from utils.ExamFolder import examfolder, examfile, get_newest_file, len_folder
from utils.read import Read

# 设置日志配置
logging.basicConfig(filename='./log/spider.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


# 从评论和转发页面的url中提取uid和log_id
def parseurl(url, index):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    return path_parts[index]


async def parse_page_func(data, idstr, cookie, resourse_path):
    async with aiohttp.ClientSession() as session:
        session.cookie_jar.update_cookies(cookie)
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random,
        }
        # 申明存储对象
        save = Save(resourse_path)
        comment_start_url = 'https://weibo.com/ajax/statuses/buildComments?'
        try:
            async with session.get(comment_start_url, headers=headers, params=data) as resp:
                logging.info(
                    f"Request {comment_start_url}?flow={data['flow']}&id={data['id']}&is_show_bulletin={data['is_show_bulletin']}&max_id={data['max_id']}&uid={data['uid']}")
                comment_json_data = await resp.json()
                # 提取 max_id
                max_id = comment_json_data["data"]["max_id"]
                save.savetojson(f'{max_id}.json', comment_json_data)
                logging.info(f"Successfully saved data to {max_id}.json")
                params = {
                    "flow": 0,
                    "id": idstr,
                    "is_show_bulletin": 2,
                    "max_id": max_id,
                    "uid": uid
                }
        except (ClientResponseError, ClientConnectionError, json.JSONDecodeError) as e:
            logging.error(f"An error occurred: {e}")
        """递归回调"""
        time.sleep(5)
        logging.info(f"已经爬取{len_folder(resourse_path)}")
        await parse_page_func(data, idstr, cookie, resourse_path)


async def main(lid, uid, cookie, resourse_path):
    async with aiohttp.ClientSession() as session:
        session.cookie_jar.update_cookies(cookie)
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random,
        }
        # 申明存储对象
        save = Save(resourse_path)
        lid_file = f"{lid}.json"
        # 判断lid_file文件是否存在
        if examfile(f"{resourse_path}/{lid_file}"):
            logging.info(f"{resourse_path}/{lid_file} has existed")
            # 从json文件中读取数据
            logging.info(f"Read {resourse_path}/{lid_file}")
            dic_data = Read(f"{resourse_path}/{lid_file}").readjson
            idstr = dic_data["idstr"]
            mid = dic_data["mid"]
            # 获取最新创建的评论文件路径
            newest_comment_file_path, newest_comment_file = get_newest_file(resourse_path)
            # 判断最新评论文件是否存在
            if examfile(newest_comment_file_path):
                logging.info(f"{newest_comment_file_path} has existed")
                comment_dic_data = Read(newest_comment_file_path).readjson
                max_id = comment_dic_data["data"]["max_id"]
                # 构造请求参数
                params = {
                    "flow": 0,
                    "id": idstr,
                    "is_show_bulletin": 2,
                    "max_id": max_id,
                    "uid": uid
                }
                await parse_page_func(params, idstr, cookie, resourse_path)
            else:
                comment_start_url = f"https://weibo.com/ajax/statuses/buildComments?flow=0&id={idstr}&is_show_bulletin=2&uid={uid}"
                try:
                    async with session.get(comment_start_url, headers=headers) as resp:
                        logging.info(f"Request {comment_start_url}")
                        comment_json_data = await resp.json()
                        # 提取 max_id
                        max_id = comment_json_data["data"]["max_id"]
                        save.savetojson(f'{max_id}.json', comment_json_data)
                        logging.info(f"Successfully saved data to {max_id}.json")
                        params = {
                            "flow": 0,
                            "id": idstr,
                            "is_show_bulletin": 2,
                            "max_id": max_id,
                            "uid": uid
                        }
                        await parse_page_func(params, idstr, cookie, resourse_path)
                except (ClientResponseError, ClientConnectionError, json.JSONDecodeError) as e:
                    logging.error(f"An error occurred: {e}")
        else:
            logging.info(f"{resourse_path}/{lid_file} has not existed")
            show_url = f'https://weibo.com/ajax/statuses/show?id={lid}&locale=zh-CN'
            try:
                async with session.get(show_url, headers=headers) as resp:
                    json_data = await resp.json()
                    save.savetojson(f'{lid}.json', json_data)
                    logging.info(f"Successfully saved data to {lid}.json")
            except (ClientResponseError, ClientConnectionError, json.JSONDecodeError) as e:
                logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    link = "https://weibo.com/1684936355/N2dFY6Ieo#comment"
    root_path = "./resourse"
    # 检查资源文件是否在
    examfolder(root_path)
    uid = parseurl(link, -2)
    log_id = parseurl(link, -1)
    # 检查并创建单个微博用户文件夹
    examfolder(f"{root_path}/{uid}")
    # 检查并创建单个微博文件夹
    file_path = examfolder(f"{root_path}/{uid}/{log_id}")
    cookies = {
        "SINAGLOBAL": "1536185175636.2178.1714698937748",
        "ULV": "1719226489208:2:1:1:2560786771228.3296.1719226489206:1714698937757",
        "WBPSESS": "bGZvSbittzOUUaWPWi8OqsuMWKbrUWxfVU4WWEwgRmBs9z-g_pyqHcC2IbNTcnmPqoXdQ_HRYvKatP_WGh-hfepq7bhcIompolmJ4YmWQMMwUc7GpbgTjBLXuwUeHD1A4b3x_-TGNY28I7Lz9WHFMw==",
        "ALF": "1722002911",
        "SUB": "_2A25LeFCPDeRhGeFK41YV-SvOyDuIHXVo9OxHrDV8PUJbkNAbLRj2kW1NQvXDSUXojb_XtuxdiO5oYYVzOyd8XYlW",
        "SUBP": "0033WrSXqPxfM725Ws9jqgMF55529P9D9WWvc7kYlevW-XfIjufSw6fw5JpX5KMhUgL.FoMX1hBX1K-Ee0M2dJLoIEBLxKnLBKMLBKeLxK-LB.qLBKMLxK-LBonL1h-LxK-LBonL1h-t",
        "XSRF-TOKEN": "nIWTh7nt4GpgkNZby2bwSwQ4"
    }

    asyncio.run(main(log_id, uid, cookies, file_path))
