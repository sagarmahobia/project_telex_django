import requests
import re
from bs4 import BeautifulSoup


def get_info_by_id(entity_id, entity_type):
    url = "https://t.me/" + str(entity_id)

    page = requests.get(url)
    soup = BeautifulSoup(page.content)

    title = soup.find("meta", property='og:title')["content"]
    description = soup.find("meta", property='og:description')["content"]
    image = soup.find("meta", property='og:image')["content"]

    subscribers = soup.select_one(".tgme_page_extra")

    if entity_type == "channels" or entity_type == "groups":
        subscribers = re.compile("^([1-9])[\s\d]+").match(subscribers.string).group().replace(" ", "")
    else:
        subscribers = 0
    return title, description, image, subscribers
