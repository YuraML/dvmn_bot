import logging
import os
import requests
import telegram

from dotenv import load_dotenv
from time import sleep


class TelegramLogsHandler(logging.Handler):
    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


logger = logging.getLogger("TelegramLogger")


def send_message(review_description, bot, chat_id):
    lesson_title = review_description['lesson_title']
    lesson_url = review_description['lesson_url']
    lesson_is_negative = review_description['is_negative']

    if lesson_is_negative:
        bot.send_message(chat_id=chat_id,
                         text=f'У вас проверили работу "{lesson_title}". '
                              f'Работа не сдана, есть недочеты. Ссылка на урок: {lesson_url}')
    else:
        bot.send_message(chat_id=chat_id,
                         text=f'У вас проверили работу "{lesson_title}".'
                              f' Работа сдана! Ссылка на урок: {lesson_url}')


def main():
    load_dotenv()
    url = 'https://dvmn.org/api/long_polling/'
    dvmn_token = os.environ['DVMN_TOKEN']
    tg_token = os.environ['TG_TOKEN']
    tg_logs_token = os.environ['TG_LOGS_TOKEN']
    chat_id = os.environ['TG_CHAT_ID']
    headers = {"Authorization": f"Token {dvmn_token}"}
    timestamp = None

    bot = telegram.Bot(token=tg_token)
    logs_bot = telegram.Bot(token=tg_logs_token)

    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(logs_bot, chat_id))
    logger.info("Бот запущен")

    while True:
        try:
            params = {'timestamp': timestamp} if timestamp else None
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            full_review = response.json()
            timestamp = full_review.get('timestamp') or full_review.get('timestamp_to_request')
            new_attempts = full_review.get('new_attempts')

            if new_attempts:
                for review_description in new_attempts:
                    send_message(review_description, bot, chat_id)

        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            logger.error("Ошибка соединения. Проверьте подключение к интернету и повторите запрос через 5 секунд.")
            sleep(5)
            continue
        except Exception as err:
            logger.exception(f"Произошла ошибка: {err}")
            sleep(5)
            continue


if __name__ == '__main__':
    main()
