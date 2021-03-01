from urllib.parse import urljoin
import json
import os
import codecs
import arrow
import requests
import bs4

SOURCE_URL = 'https://tuoitre.vn/tin-moi-nhat.htm'
BASE_URL = 'https://tuoitre.vn/'


def get_content_article(url):
    raw_content = requests.get(url)
    if raw_content.ok:
        data = {}
        obj_content = bs4.BeautifulSoup(raw_content.content, 'lxml')
        title = obj_content.select_one('.article-title')
        data['title'] = title.text
        sub_title = obj_content.select_one('.main-content-body .sapo')
        data['sub_title'] = sub_title.text
        main_content = obj_content.select_one('.content .fck')
        data['main_content'] = main_content.text.replace('\n', '')
        pub_date = obj_content.select_one('.date-time')
        pub_date_format = arrow.get(pub_date.text.replace(' GMT+7', ''),  'DD/MM/YYYY HH:mm')
        created_path = './' + str(pub_date_format.date())
        if not os.path.isdir(created_path):
            os.makedirs(created_path)
        data['pub_date'] = pub_date_format.replace(tzinfo='Asia/Ho_Chi_Minh').format(locale='vi')
        f = codecs.open(created_path + '/' + data['pub_date'], mode='w', encoding='utf-8')
        json.dump(data, f, indent=4, ensure_ascii=False)
    else:
        print('Fail')


def get_link():
    r = requests.get(SOURCE_URL)
    if r.ok:
        obj_request = bs4.BeautifulSoup(r.content, 'lxml')
        links = obj_request.select('.name-news .title-news a')
        for tag_a in links:
            temp_url = urljoin(BASE_URL, tag_a.attrs['href'])
            get_content_article(temp_url)
    else:
        print('Fail')


if __name__ == '__main__':
    get_link()
