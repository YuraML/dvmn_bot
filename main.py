import os
import requests
import telegram

from dotenv import load_dotenv
from time import sleep


def main():
    load_dotenv()
    url = 'https://dvmn.org/api/long_polling/'
    dvmn_token = os.environ['DVMN_TOKEN']
    tg_token = os.environ['TG_TOKEN']
    chat_id = os.environ['TG_CHANNEL_ID']

    headers = {"Authorization": f"Token {dvmn_token}"}
    timestamp = None
    bot = telegram.Bot(token=tg_token)

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
                    lesson_title = review_description['lesson_title']
                    lesson_url = review_description['lesson_url']
                    lesson_is_negative = review_description['is_negative']

                    if lesson_is_negative:
                        bot.send_message(chat_id=chat_id,
                                         text=f'У вас проверили работу "{lesson_title}".'
                                              f' Работа не сдана, есть недочеты. Ссылка на урок: {lesson_url}')
                    else:
                        bot.send_message(chat_id=chat_id,
                                         text=f'У вас проверили работу "{lesson_title}".'
                                              f' Работа сдана! Ссылка на урок: {lesson_url}')

        except requests.exceptions.ReadTimeout:
            print("Превышено время ожидания запроса. Повторная попытка через 5 секунд.")
            sleep(5)
            continue
        except requests.exceptions.ConnectionError:
            print("Ошибка соединения. Проверьте подключение к интернету и повторите запрос через 5 секунд.")
            sleep(5)
            continue


if __name__ == '__main__':
    main()
