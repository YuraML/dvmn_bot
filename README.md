# dvmn_bot
 
Бот для публикации сообщений в телеграм боте пользователя о статусе проверок уроков на образовательной платформе [dvmn.org](https://dvmn.org/). Бот упакован в Docker контейнер и для его работы требуются только переменные окружения.

### Установка

Для запуска этого бота вам потребуется Docker. Вы можете скачать и установить его с [официального сайта](https://www.docker.com/get-started).

Откройте терминал и клонируйте этот репозиторий, а затем перейдите в его директорию:

```bash
git clone https://github.com/YuraML/dvmn_bot.git
cd dvmn_bot
```

Для работы программы необходимо создать файл `.env` в этой же директории, заполненный следующим образом:

```
DVMN_TOKEN={ваш API токен от платформы dvmn}
TG_TOKEN={токен вашего телеграм бота}
TG_LOGS_TOKEN={токен вашего бота, отвечающего за логи}
TG_CHAT_ID={id вашего телеграм чата}
```

Затем соберите Docker образ:

```bash
docker build -t dvmn_bot .
```

### Запуск

Для запуска бота введите в командную строку:

```bash
docker run -d --name dvmn_bot-instance --env-file=.env dvmn_bot
```

После этого бот начнет работу. Он работает непрерывно: в случае, если ваша работа будет проверена преподавателем, телеграм бот сразу же отправит соотвеетсвующее сообщение со статусом проверки работы.


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
