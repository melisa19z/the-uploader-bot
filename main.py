import telebot
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlparse
import json
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

bot = telebot.TeleBot('7458519634:AAFlQ3wO8ZJyeRv8xPnMRl07HdHyLJEVrs0')


def ph_to_url(link):
    url_data = urlparse(link)
    if not (url_data.netloc in ["www.pornhub.com", "pornhub.com"] and url_data.path == "/view_video.php" and url_data.query.startswith('viewkey=')):
        exit("This link is incorrect.")

    id = url_data.query.replace("viewkey=", '')

    response = urlopen(f"https://www.pornhub.com/embed/{id}")
    html_text = response.read()

    soup = BeautifulSoup(html_text, 'html.parser')

    script = soup.find_all(
        name='script',
        string=lambda text: text and "var flashvars" in text
    )[0]

    json_data = re.findall(r'\{.*?\}', str(script))
    json_video_url = json.loads(
        [item for item in json_data if "get_media" in item][0])['videoUrl']

    json_video_response = urlopen(json_video_url)
    json_video_data = json_video_response.read()
    json_video = json.loads(json_video_data)

    return json_video[0]['videoUrl']


@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    categories = ['Step Mom', 'Step Sister', 'Step Dad', 'Hard Fuck']
    for category in categories:
        keyboard.add(telebot.types.KeyboardButton(category))
    bot.send_message(
        message.chat.id, "لطفاً دسته‌بندی مورد نظر خود را انتخاب کنید:", reply_markup=keyboard)


@bot.message_handler(chat_types=['private'])
def handle_message(message):

    global CATEGORY

    CATEGORY = message.text.lower()
    print(CATEGORY)

    try:
        options = Options()
        options.add_argument("--headless")

        driver = webdriver.Chrome(options=options)

        driver.get('https://www.pornhub.com/')

        sleep(5)
        age_verification_button = driver.find_element(
            By.XPATH, '/html/body/div[4]/div/div/button')
        age_verification_button.click()

        sleep(5)
        accept_cookies_button = driver.find_element(
            By.XPATH, '/html/body/div[4]/div/button[1]')
        accept_cookies_button.click()

        sleep(5)
        search_box = driver.find_element(By.NAME, 'search')
        search_box.send_keys(CATEGORY)
        search_box.send_keys(Keys.RETURN)

        sleep(5)
        video_links = driver.find_elements(
            By.CSS_SELECTOR, '#videoSearchResult a')

        reply_message = f'لینک‌های جستجو برای دسته "{CATEGORY}":\n'
        # در اینجا فقط اولین لینک را می‌گیریم، می‌توانید تعداد بیشتری را انتخاب کنید.
        for link in video_links[:1]:
            theLinks = link.get_attribute('href') + '\n'
            the_final_link = ph_to_url(theLinks)
            print(ph_to_url(theLinks))
            bot.send_video(message.chat.id, the_final_link)

    except Exception as e:
        print(e)
        error_message = f'مشکلی در اجرای درخواست شما پیش آمده است:\n{str(e)}'
        bot.send_message(message.chat.id, error_message)

    finally:
        driver.quit()


bot.polling(none_stop=True)
