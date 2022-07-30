import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re

# Change this to a relevant path on your computer. This path will be used to create a text file
path_output = "/Users/sebastiansaker/Downloads/data_Jp_Behavox/web_scraped_2channel_tradingsecurities/2channel_stocks_tradingadvice_futures_marketcond.txt"


# Assigns the url to a variable to make it easier to call, change as necessary (only tested on "forum" pages accessed
# from an "indice" page like "IBEX 35")
replaceTags = [
    '<span class="AA">[^<]+',
    '</span>',
    '<a [\w \-\."\'= \/&\?]+>',
    '<a[^>]*>[^<]+',
    '<\/a>',
    '<br/>',
    '<span class="escaped">',
    '</div>',
    '<div class="message">',
    '<span class="escaped">',
    '&gt;&gt;[0-9]+ +'
]

# Assigns the url to a variable to make it easier to call, change as necessary (only tested on "forum" pages accessed
# from an "indice" page like "IBEX 35")
urls = [
    "https://egg.5ch.net/test/read.cgi/stock/1655965952/",
    "https://egg.5ch.net/test/read.cgi/stock/1656054666/",
    "https://egg.5ch.net/test/read.cgi/stock/1655987544/",
    "https://egg.5ch.net/test/read.cgi/stock/1655881271/",
    "https://egg.5ch.net/test/read.cgi/stock/1655820737/",
    "https://egg.5ch.net/test/read.cgi/stock/1656052869/",
    "https://egg.5ch.net/test/read.cgi/stock/1656047485/",
    "https://egg.5ch.net/test/read.cgi/stock/1656042840/",
    "https://egg.5ch.net/test/read.cgi/stock/1656031724/",
    "https://egg.5ch.net/test/read.cgi/stock/1655981232/",
    "https://egg.5ch.net/test/read.cgi/stock/1655699980/",
    "https://egg.5ch.net/test/read.cgi/stock/1655349959/",
    "https://egg.5ch.net/test/read.cgi/stock/1655090579/",
    "https://egg.5ch.net/test/read.cgi/stock/1654703357/",
    "https://egg.5ch.net/test/read.cgi/stock/1654413962/",
    "https://egg.5ch.net/test/read.cgi/stock/1654169195/",
    "https://mao.5ch.net/test/read.cgi/stockb/1642755041/",
    "https://mao.5ch.net/test/read.cgi/stockb/1537872547/",
    "https://mao.5ch.net/test/read.cgi/stockb/1652765999/",
    "https://mao.5ch.net/test/read.cgi/stockb/1648553574/",
    "https://mao.5ch.net/test/read.cgi/stockb/1542157861/",
    "https://mao.5ch.net/test/read.cgi/stockb/1577032713/",
    "https://mao.5ch.net/test/read.cgi/stockb/1638362419/",
    "https://mao.5ch.net/test/read.cgi/stockb/1584076457/",
    "https://mao.5ch.net/test/read.cgi/stockb/1653771778/",
    "https://mao.5ch.net/test/read.cgi/stockb/1648683138/",
    "https://mao.5ch.net/test/read.cgi/stockb/1463449956/",
    "https://mao.5ch.net/test/read.cgi/apple2/1614863339/",
    "https://medaka.5ch.net/test/read.cgi/market/1655960637/",
    "https://medaka.5ch.net/test/read.cgi/market/1655865308/",
    "http://medaka.5ch.net/test/read.cgi/market/1655178501/",
    "https://medaka.5ch.net/test/read.cgi/market/1635234873/",
    "https://medaka.5ch.net/test/read.cgi/market/1627778227/",
    "https://hayabusa9.5ch.net/test/read.cgi/livemarket1/1656080889/",
    "https://hayabusa9.5ch.net/test/read.cgi/livemarket1/1656075632/",
    "http://hayabusa9.5ch.net/test/read.cgi/livemarket1/1656035837/",
    "https://hayabusa9.5ch.net/test/read.cgi/livemarket1/1655174361/",
    "https://hayabusa9.5ch.net/test/read.cgi/livemarket1/1655170269/",
    "https://hayabusa9.5ch.net/test/read.cgi/livemarket2/1656071949/",
    "https://hayabusa9.5ch.net/test/read.cgi/livemarket2/1656078271/",
    "https://hayabusa9.5ch.net/test/read.cgi/livemarket2/1654206245/",
    "https://hayabusa9.5ch.net/test/read.cgi/livemarket2/1655144953/",
    "https://hayabusa9.5ch.net/test/read.cgi/livemarket1/1655129904/",
    "https://hayabusa9.5ch.net/test/read.cgi/livemarket1/1655121315/",
    "https://hayabusa9.5ch.net/test/read.cgi/livemarket1/1655115892/",
    "https://hayabusa9.5ch.net/test/read.cgi/livemarket1/1655110974/",
    "https://hayabusa9.5ch.net/test/read.cgi/livemarket1/1655102641/"

    # "https://mao.5ch.net/test/read.cgi/money/1518326052/",
    # "https://mao.5ch.net/test/read.cgi/money/1612203406/",
    # "https://mao.5ch.net/test/read.cgi/money/1560007576/",
    # "https://mao.5ch.net/test/read.cgi/money/1636224745/",
    # "https://mao.5ch.net/test/read.cgi/money/1634334609/",
    # "https://mao.5ch.net/test/read.cgi/money/1592825385/",
    # "https://mao.5ch.net/test/read.cgi/money/1578188360/",
    # "http://mao.5ch.net/test/read.cgi/money/1544828759/",
    # "https://mao.5ch.net/test/read.cgi/money/1647933155/",
    # "https://mao.5ch.net/test/read.cgi/money/1638275565/",
    # "https://mao.5ch.net/test/read.cgi/money/1631321847/",
    # "https://mao.5ch.net/test/read.cgi/money/1637479364/",
    # "https://mao.5ch.net/test/read.cgi/money/1629961226/",
    # "http://mao.5ch.net/test/read.cgi/money/1615627177/",
    # "https://mao.5ch.net/test/read.cgi/money/1606609203/",
    # "https://mao.5ch.net/test/read.cgi/money/1626595821/",
    # "https://mao.5ch.net/test/read.cgi/money/1621936629/",
    # "https://mao.5ch.net/test/read.cgi/money/1617609178/",
    # "https://mao.5ch.net/test/read.cgi/money/1612305923/",
    # "https://mao.5ch.net/test/read.cgi/money/1635917538/",
    # "https://mao.5ch.net/test/read.cgi/money/1626316743/",
    # "https://mao.5ch.net/test/read.cgi/money/1619326248/",
    # "https://medaka.5ch.net/test/read.cgi/eco/1652890401/",
    # "https://medaka.5ch.net/test/read.cgi/eco/1651728269/",
    # "https://medaka.5ch.net/test/read.cgi/eco/1650350442/",
    # "https://medaka.5ch.net/test/read.cgi/eco/1638899117/",
    # "https://medaka.5ch.net/test/read.cgi/eco/1636197076/",
    # "https://medaka.5ch.net/test/read.cgi/eco/1633442852/",
    # "https://rio2016.5ch.net/test/read.cgi/credit/1654407587/",
    # "https://rio2016.5ch.net/test/read.cgi/credit/1653721040/",
    # "https://rio2016.5ch.net/test/read.cgi/credit/1650283087/",
    # "https://rio2016.5ch.net/test/read.cgi/credit/1654007031/",
    # "https://rio2016.5ch.net/test/read.cgi/credit/1651982574/",
    # "https://rio2016.5ch.net/test/read.cgi/credit/1608297176/",
    # "https://rio2016.5ch.net/test/read.cgi/credit/1641628742/",
    # "http://rio2016.5ch.net/test/read.cgi/credit/1600489984/",
    # "https://rio2016.5ch.net/test/read.cgi/credit/1575522076/",
    # "https://rio2016.5ch.net/test/read.cgi/credit/1614998091/"


]

of = open(path_output, "w+", encoding="utf-8")

maxLength = 200  # chars
filteredMsgs = []  # to store filtered messages

for page_root_url in urls:

    output = re.search("https://(.+)$", page_root_url)
    if not output:
        continue

    response = requests.get(page_root_url)
    soup = BeautifulSoup(response.text, "html.parser")
    all_msg = soup.findAll('div', 'message')

    # remove the first and last two entries when scrapping from 5channel

    all_msg.pop(0)
    all_msg.pop(len(all_msg)-1)
    all_msg.pop(len(all_msg)-1)

    for msg in all_msg:
        msg = str(msg)
        for tag in replaceTags:
            msg = re.sub(tag, '', msg)
        # if message is over 200 chars, ignore
        if (len(msg) > maxLength):
            continue
        filteredMsgs.append(msg)

    # to avoid being detected for webscraping
    time.sleep(1)

for msg in filteredMsgs:
    of.write(msg+'\n')
of.close()
