import os
import telebot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# تنظیمات مربوط به بات تلگرام
bot = telebot.TeleBot('7458519634:AAFlQ3wO8ZJyeRv8xPnMRl07HdHyLJEVrs0')

# تنظیمات وب‌اسکرپر
chromedriver_path = r"C:\Users\RayanPishro\Desktop\chromedriver-win64\chromedriver.exe"
if not os.path.exists(chromedriver_path):
    raise FileNotFoundError(f"Chromedriver not found at {chromedriver_path}")
os.environ['PATH'] += os.pathsep + os.path.dirname(chromedriver_path)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
    categories = ['Step Mom', 'Step Sister', 'Step Dad', 'Hard Fuck']
    for category in categories:
        keyboard.add(telebot.types.KeyboardButton(category))
    bot.send_message(
        message.chat.id, "لطفاً دسته‌بندی مورد نظر خود را انتخاب کنید:", reply_markup=keyboard)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global CATEGORY
    CATEGORY = message.text.lower()  # دریافت دسته‌بندی از پیام کاربر
    print(CATEGORY)
    try:
        driver = webdriver.Chrome()

        driver.get('https://www.pornhub.com/')

        age_verification_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@data-label="over18_enter"]'))
        )
        age_verification_button.click()

        accept_cookies_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@data-label="accept_all"]'))
        )
        accept_cookies_button.click()

        search_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'search'))
        )
        search_box.send_keys(CATEGORY)
        search_box.send_keys(Keys.RETURN)

        video_links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, '#videoSearchResult a'))
        )

        reply_message = f'لینک‌های جستجو برای دسته "{CATEGORY}":\n'
        for link in video_links[:3]:
            reply_message += link.get_attribute('href') + '\n'
            print(link)

        bot.send_message(message.chat.id, reply_message)

    except Exception as e:
        error_message = f'مشکلی در اجرای درخواست شما پیش آمده است:\n{str(e)}'
        bot.send_message(message.chat.id, error_message)

    finally:
        driver.quit()


# اجرای بات تلگرام
bot.polling()
