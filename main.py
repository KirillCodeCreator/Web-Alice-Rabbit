# импортируем библиотеки
import logging

from flask import Flask, request, jsonify

# создаём приложение
# мы передаём __name__, в нём содержится информация,
# в каком модуле мы находимся.
# В данном случае там содержится '__main__',
# так как мы обращаемся к переменной из запущенного модуля.
# если бы такое обращение, например, произошло внутри модуля logging,
# то мы бы получили 'logging'
app = Flask(__name__)

# Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)

# Создадим словарь, чтобы для каждой сессии общения
# с навыком хранились подсказки, которые видел пользователь.
# Это поможет нам немного разнообразить подсказки ответов
# (buttons в JSON ответа).
# Когда новый пользователь напишет нашему навыку,
# то мы сохраним в этот словарь запись формата
# sessionStorage[user_id] = {'suggests': ["Не хочу.", "Не буду.", "Отстань!" ]}
# Такая запись говорит, что мы показали пользователю эти три подсказки.
# Когда он откажется купить слона,
# то мы уберем одну подсказку. Как будто что-то меняется :)
sessionStorage = {}


@app.route('/post', methods=['POST'])
# Функция получает тело запроса и возвращает ответ.
# Внутри функции доступен request.json - это JSON,
# который отправила нам Алиса в запросе POST
def main():
    logging.info(f'Request: {request.json!r}')

    # Начинаем формировать ответ, согласно документации
    # мы собираем словарь, который потом отдадим Алисе
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    # Отправляем request.json и response в функцию handle_dialog.
    # Она сформирует оставшиеся поля JSON, которые отвечают
    # непосредственно за ведение диалога
    handle_dialog(request.json, response)
    logging.info(f'Response:  {response!r}')

    # Преобразовываем в JSON и возвращаем
    return jsonify(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if New_Session(req):
        Init_Elephant_Session(res, user_id)
    elif Has_Elephant(user_id) is False:
        handle_dialog_elephant(req, res, user_id)
    elif Has_Rabbit(user_id) is False:
        handle_dialog_rabbit(req, res, user_id)


def New_Session(req):
    return req['session']['new'] is True

def Init_Elephant_Session(res, user_id):
    sessionStorage[user_id] = {
        'suggests': [
            "Не хочу.",
            "Не буду.",
            "Отстань!",
        ],
        'elephant': False
    }

    res['response']['text'] = f'Привет! Купи слона!'
    # Получим подсказки
    res['response']['buttons'] = get_suggests_elephant(user_id)
    return

def Init_Rabbit_Session(res, user_id):
    sessionStorage[user_id]['suggests'] = [
            "Не хочу.",
            "Не буду.",
            "Отстань!"
        ]
    sessionStorage[user_id]['rabbit'] = False

    res['response']['text'] = 'А теперь купи кролика!'
    # Получим подсказки
    res['response']['buttons'] = get_suggests_rabbit(user_id)
    return

def handle_dialog_elephant(req, res, user_id):
    # Сюда дойдем только, если пользователь не новый,
    # и разговор с Алисой уже был начат
    # Обрабатываем ответ пользователя.
    # В req['request']['original_utterance'] лежит весь текст,
    # что нам прислал пользователь
    # Если в ответе содержится вхождение слов 'ладно', 'куплю', 'покупаю', 'хорошо',
    # то мы считаем, что пользователь согласился.
    words = req['request']['original_utterance'].lower().split()
    logging.debug(f'request words:  {words}')
    matchers = ['ладно', 'куплю', 'покупаю', 'хорошо']
    matching = [s for s in words if any(xs in s for xs in matchers)]
    logging.debug(f'matching:  {matching}')

    if len(matching) > 0:
        # Пользователь согласился.
        Buy_Elephant(user_id)
        Init_Rabbit_Session(res, user_id)
        return

    # Если нет, то убеждаем его купить слона!
    res['response']['text'] = \
        f"Все говорят '{req['request']['original_utterance']}', а ты купи слона!"
    res['response']['buttons'] = get_suggests_elephant(user_id)


def handle_dialog_rabbit(req, res, user_id):
    # Сюда дойдем только, если пользователь не новый и уже купил слона,
    # Обрабатываем ответ пользователя.
    # В req['request']['original_utterance'] лежит весь текст,
    # что нам прислал пользователь
    # Если в ответе содержится вхождение слов 'ладно', 'куплю', 'покупаю', 'хорошо',
    # то мы считаем, что пользователь согласился.
    words = req['request']['original_utterance'].lower().split()
    logging.debug(f'request words:  {words}')
    matchers = ['ладно', 'куплю', 'покупаю', 'хорошо']
    matching = [s for s in words if any(xs in s for xs in matchers)]
    logging.debug(f'matching:  {matching}')

    if len(matching) > 0:
        Buy_Rabbit(user_id)
        # Пользователь согласился, прощаемся.
        res['response']['text'] = 'Кролика можно найти на Яндекс.Маркете!'
        res['response']['end_session'] = True
        return

    # Если нет, то убеждаем его купить кролика!
    res['response']['text'] = \
        f"Все говорят '{req['request']['original_utterance']}', а ты купи кролика!"
    res['response']['buttons'] = get_suggests_rabbit(user_id)


# Функция возвращает две подсказки для ответа.
def get_suggests_elephant(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    # Если осталась только одна подсказка, предлагаем подсказку
    # со ссылкой на Яндекс.Маркет.
    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": f"https://market.yandex.ru/search?text=слон",
            "hide": True
        })

    return suggests

# Функция возвращает две подсказки для ответа.
def get_suggests_rabbit(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    # Если осталась только одна подсказка, предлагаем подсказку
    # со ссылкой на Яндекс.Маркет.
    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": f"https://market.yandex.ru/search?text=кролик",
            "hide": True
        })

    return suggests


def Buy_Elephant(user_id):
    sessionStorage[user_id]['elephant'] = True


def Buy_Rabbit(user_id):
    sessionStorage[user_id]['rabbit'] = True


def Has_Elephant(user_id):
    return sessionStorage[user_id]['elephant'] is True


def Has_Rabbit(user_id):
    return sessionStorage[user_id]['rabbit'] is True


if __name__ == '__main__':
    app.run()
