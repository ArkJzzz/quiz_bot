# support-bot 

Бот-викторина для Telegram и группы ВКонтакте.


## Подготовка

- **Telegram**

    Напишите [Отцу ботов](https://telegram.me/BotFather):

    ```
    \start
    ```

    ```
    \newbot
    ```

    Получите токен для доступа к API Telegram.

- **ВКонтакте**

    Создайте группу во [ВКонтакте](https://vk.com/groups?tab=admin);

    Получите токен группы в настройках сообщества.

- **Redis**

    Зарегистрируйтесь на [redislabs](https://redislabs.com/)

    Получите адрес БД вида `redis-13965.f18.us-east-4-9.wc1.cloud.redislabs.com`, его порт вида: `16635` и его пароль.


## Установка

- Клонируйте репозиторий:
```
git clone https://github.com/ArkJzzz/quiz_bot.git
```

- Создайте файл ```.env``` и поместите в него токены Telegram и ВКонтакте, а так же данные для доступа к Redis:
```
TELEGRAM_TOKEN=<Ваш токен>
VK_TOKEN=<Ваш токен>
REDIS_HOST=<Адрес БД>
REDIS_PORT=<Порт>
REDIS_DB=<Номер БД, по умолчанию 0>
REDIS_PASSWORD=<Пароль>
```

- Установить зависимости:
```
pip3 install -r requirements.txt
```

## Запуск

- **Добавление в базу и обновление вопросов**
```
python3 init_quiz_db.py /Путь/к/директории/с/файлами/вопросов
```

- **Бот telegram**

```
python3 bot-tg.py
```
![](examination_tg.gif)

- **Бот VK**

```
python3 bot-vk.py
```
![](examination_tg.gif)


------
Примеры работающих ботов:

- [telegram](tg://resolve?domain=arkjzzz_quiz_bot)

- [vkontakte](https://vk.com/im?sel=-189341550)
