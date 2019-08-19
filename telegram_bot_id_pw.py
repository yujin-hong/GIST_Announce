import telegram
import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

my_token = '**********' # your telegram chatbot token
bot = telegram.Bot(token=my_token)
# updates = bot.getUpdates()
#
# for u in updates:
#     print(u.message)

# chat_id = bot.getUpdates()[-1].message.chat.id #가장 최근에 온 메세지의 chat id를 가져옵니다
# print(chat_id)
chat_id = '********' #your chat_id

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with requests.Session() as s:
    list_req = s.get('https://college.gist.ac.kr/prog/bbsArticle/BBSMSTR_000000005587/list.do')
    html = list_req.text
    soup = BeautifulSoup(html, 'html.parser')
    href = ""
    onclick = ""
    text = ""
    titles = []
    for title in soup.find_all("td", class_="subject"):
        titles.append(title.find("a").get_text())

    before = ''

    with open(os.path.join(BASE_DIR, 'latest.txt'), 'r') as f:
        before = f.readline()
    # print("before")
    # print(before)
    # print("title[5]")
    # print(titles[5])
    if before != titles[5]:
    # if 1:
        with open(os.path.join(BASE_DIR, 'latest.txt'), 'w') as f:
            f.write(titles[5])
            bot.sendMessage(chat_id=chat_id, parse_mode="Markdown", text='*'+titles[5]+'*')
            options = webdriver.ChromeOptions()

            options.add_argument('headless')
            options.add_argument('window-size=1920x1080')
            options.add_argument("disable-gpu")
            # options.add_argument("no-sandbox")
            # driver = webdriver.Chrome('/home/hyj2508/Downloads/chromedriver')

            driver = webdriver.Chrome('/home/hyj2508/Downloads/chromedriver', chrome_options=options)

            driver.get('https://college.gist.ac.kr/college/login.do')

            driver.find_element_by_name('id').send_keys('*****') # your id
            driver.find_element_by_name('password').send_keys('******') # your password

            driver.find_element_by_id('login_btn').click()

            driver.get('https://college.gist.ac.kr/prog/bbsArticle/BBSMSTR_000000005587/list.do')

            driver.find_elements_by_class_name("subject")[5].find_element_by_tag_name('a').click()

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            contents = soup.find("div", class_="ui bbs--view--content").get_text().strip()
            bot.sendMessage(chat_id=chat_id, text=contents)

            clips = ''
            for clip in soup.find_all("a", class_='btn-on-ico'):
                print(clip['href'])
                # print(clip['href'][29:49])
                # print(clip['href'][52:53])
                clip_url = 'https://college.gist.ac.kr/cmm/fms/FileDown.do?atchFileId='+\
                      clip['href'][29:49]+'&fileSn='+clip['href'][52:53]
                print(clip_url)
                clip_title = clip.get_text()
                clip_title = clip_title.replace('[', '|').replace(']', '|')
                print(clip_title)
                clips = clips + '['+ clip_title +']('+clip_url+'), '
            if clips=='':
                bot.sendMessage(chat_id=chat_id, text='첨부 없음')
            else:
                clips = '첨부: ' + clips
                bot.sendMessage(chat_id=chat_id, parse_mode="Markdown", text=clips)



    # print(titles[5])
        # print(title.find("a")['href'])
        # href = title.find("a")['href']
        # # print(title.find("a")['onclick'])
        # print(title.find("a")['onclick'][30:50])
        # onclick = title.find("a")['onclick'][30:50]
        # print(title.find("a").get_text().strip())
        # text = title.find("a").get_text().strip()