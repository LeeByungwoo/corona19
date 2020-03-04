import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from cralwer.spread import worksheet
from pytz import timezone

URL = "https://seoul.go.kr/coronaV/coronaStatus.do?tab=1"


def remove_tag(content):
    cleanr = re.compile("<.*?>|")
    cleantext = re.sub(cleanr, "", content).strip()
    return cleantext


def main():
    conora_list = []
    req = requests.get(URL)

    # 200일 경우
    if req.status_code == 200:

        html = req.text
        soup = BeautifulSoup(html, "html.parser")
        cralwer_time = datetime.now(timezone("Asia/Seoul")).strftime(
            "%Y-%m-%d %H:%M"
        )

        # 대한 민국 기준
        result = soup.select("div > div.status > div.status-korea > h4 > span")
        # 대한민국 확진자 수
        result += soup.select(
            "div > div.status > div.status-korea > div > div.num.knum1 > p.counter"
        )
        # 대한민국 사망자 수
        result += soup.select(
            "div > div.status > div.status-korea > div > div.num.knum2 > p.counter"
        )
        result += soup.select(
            "div > div.status > div.status-korea > div > div.num.knum3 > p.counter"
        )

        # 서울 시간 기준
        result += soup.select(
            "#tab-cont1 > div > div.status > div.status-seoul > h4 > span"
        )
        # 서울 확진자 수
        result += soup.select(
            "div > div.status > div.status-seoul > div.cell.cell1 > div > p.counter"
        )
        # 서울 세부 내용
        result += soup.select(
            "#move-cont1 > div:nth-child(2) > h5:nth-child(3) > strong"
        )

        for word in result:
            conora_list.append(remove_tag(str(word)))

        worksheet.append_row(
            [
                cralwer_time,
                conora_list[0],
                int((conora_list[1]).replace(',', '')),
                int(conora_list[2]),
                int(conora_list[3]),
                conora_list[4],
                conora_list[5],
#                 conora_list[6]
            ],
            2,
        )


if __name__ == "__main__":
    main()
