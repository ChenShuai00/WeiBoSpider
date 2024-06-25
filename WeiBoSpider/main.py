import aiohttp
import asyncio
from urllib.parse import urlparse
from fake_useragent import UserAgent
from utils.save import Save


# 从评论和转发页面的url中提取mblogid
def parseUrl(url):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    log_id = path_parts[-1] if path_parts else None
    return log_id


async def main(lid, cookie, resourse_path):
    async with aiohttp.ClientSession() as session:
        session.cookie_jar.update_cookies(cookie)
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random,
        }
        show_url = f'https://weibo.com/ajax/statuses/show?id={lid}&locale=zh-CN'
        async with session.get(show_url, headers=headers) as resp:
            data = await resp.json()
            s = Save(resourse_path, f'{lid}.json', data)
            s.saveToJson()



if __name__ == "__main__":
    link = "https://weibo.com/1684936355/N2dFY6Ieo#comment"
    resourse_path = "./resourse"
    log_id = parseUrl(link)
    cookies = {
        'XSRF-TOKEN': '5dSDvK-NUjBm6_GslnWfsw-0',
        'WBPSESS': 'bGZvSbittzOUUaWPWi8OqsuMWKbrUWxfVU4WWEwgRmBs9z-g_pyqHcC2IbNTcnmPqoXdQ_HRYvKatP_WGh'
                   '-hfar5GWk5m4UddWWbJzCKHHIgAA2rvcYF1SiBvpw2ju-olfvkSvNU_S-f5XA6AA5WFg==',
        'ALF': '1721891468',
        'SUB': '_2A25Lfh3cDeRhGeFK41YV-SvOyDuIHXVo8h8UrDV8PUJbkNAGLVjnkW1NQvXDSX3QeNGAhldRSPPtmI3mXDgffPuS',
        'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WWvc7kYlevW-XfIjufSw6fw5JpX5KMhUgL.FoMX1hBX1K'
                '-Ee0M2dJLoIEBLxKnLBKMLBKeLxK-LB.qLBKMLxK-LBonL1h-LxK-LBonL1h-t',
    }

    asyncio.run(main(log_id, cookies, resourse_path))
