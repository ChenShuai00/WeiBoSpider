import aiohttp
import asyncio
import os
from urllib.parse import urlparse
from fake_useragent import UserAgent
from utils.save import Save
from utils.ExamFolder import ExamFolder
from utils.read import Read


# 从评论和转发页面的url中提取mblogid
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
        if os.path.exists(f"{resourse_path}/{lid}.json"):
            dic_data = Read(f"{resourse_path}/{lid}.json").readjson()
            print(dic_data["id"])
        else:
            show_url = f'https://weibo.com/ajax/statuses/show?id={lid}&locale=zh-CN'
            async with session.get(show_url, headers=headers) as resp:
                json_data = await resp.json()
                save = Save(resourse_path, f'{lid}.json', json_data)
                save.savetojson()


if __name__ == "__main__":
    link = "https://weibo.com/1684936355/N2dFY6Ieo#comment"
    root_path = "./resourse"
    # 检查资源文件是否在
    exam = ExamFolder()
    exam.examfolder(root_path)
    uid = parseurl(link,-2)
    log_id = parseurl(link, -1)
    # 检查并创建单个微博用户文件夹
    exam.examfolder(f"{root_path}/{uid}")
    # 检查并创建单个微博文件夹
    file_path = exam.examfolder(f"{root_path}/{uid}/{log_id}")
    cookies = {
        'XSRF-TOKEN': '5dSDvK-NUjBm6_GslnWfsw-0',
        'WBPSESS': 'bGZvSbittzOUUaWPWi8OqsuMWKbrUWxfVU4WWEwgRmBs9z-g_pyqHcC2IbNTcnmPqoXdQ_HRYvKatP_WGh'
                   '-hfar5GWk5m4UddWWbJzCKHHIgAA2rvcYF1SiBvpw2ju-olfvkSvNU_S-f5XA6AA5WFg==',
        'ALF': '1721891468',
        'SUB': '_2A25Lfh3cDeRhGeFK41YV-SvOyDuIHXVo8h8UrDV8PUJbkNAGLVjnkW1NQvXDSX3QeNGAhldRSPPtmI3mXDgffPuS',
        'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WWvc7kYlevW-XfIjufSw6fw5JpX5KMhUgL.FoMX1hBX1K'
                '-Ee0M2dJLoIEBLxKnLBKMLBKeLxK-LB.qLBKMLxK-LBonL1h-LxK-LBonL1h-t',
    }

    asyncio.run(main(log_id, cookies, file_path))
