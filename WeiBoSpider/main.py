import aiohttp
import asyncio
import os
import json
import logging
from aiohttp import ClientResponseError, ClientConnectionError
from urllib.parse import urlparse
from fake_useragent import UserAgent
from utils.save import Save
from utils.ExamFolder import examfolder, examfile, get_newest_file
from utils.read import Read

# 设置日志配置
logging.basicConfig(filename='./log/spider.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


# 从评论和转发页面的url中提取uid和log_id
def parseurl(url, index):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    return path_parts[index]


async def main(lid, cookie, resourse_path):
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
            logging.info(f"{resourse_path}/{lid_file} 已经存在")
            newest_comment_file_path, newest_comment_file = get_newest_file(resourse_path)
            if examfile(newest_comment_file_path):
                logging.info(f"{newest_comment_file_path} 已经存在")
                comment_dic_data = Read(newest_comment_file_path).readjson
                max_id = comment_dic_data["data"]["max_id"]
                print(max_id)
            # 从json文件中读取数据
            dic_data = Read(f"{resourse_path}/{lid_file}").readjson
            idstr = dic_data["idstr"]
            mid = dic_data["mid"]
            comment_start_url = f"https://m.weibo.cn/comments/hotflow?id={idstr}&mid={mid}"
            try:
                async with session.get(comment_start_url, headers=headers) as resp:
                    logging.info(f"请求 {comment_start_url}")
                    comment_json_data = await resp.json()
                    # 提取 max_id
                    max_id = comment_json_data["data"]["max_id"]
                    save.savetojson(f'{max_id}.json', comment_json_data)
                    logging.info(f"Successfully saved data to {max_id}.json")
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
        "_T_WM": "21978021763",
        "WEIBOCN_FROM": "1110006030",
        "MLOGIN": "1",
        "SUBP": "0033WrSXqPxfM725Ws9jqgMF55529P9D9WWvc7kYlevW-XfIjufSw6fw5JpX5K-hUgL.FoMX1hBX1K"
                "-Ee0M2dJLoIEBLxKnLBKMLBKeLxK-LB.qLBKMLxK-LBonL1h-LxK-LBonL1h-t",
        "SCF": "AvFoZD3kAPxQ06Glnrx-G4GAtMXfH4eyQH1IMTqZVewOAcGfjILPTfjphRt9Fc5PsLK83hupOz4aIVrfTASE4a8.",
        "SUB": "_2A25LfwtoDeRhGeFK41YV-SvOyDuIHXVo9QKgrDV6PUJbktB-LVHMkW1NQvXDSY45vmFNDjJTyegc0XVJbXpTxMG9",
        "SSOLoginState": "1719368503",
        "ALF": "1721960503",
        "XSRF-TOKEN": "aa9161",
        "mweibo_short_token": "dede862b40"
    }

    asyncio.run(main(log_id, cookies, file_path))
