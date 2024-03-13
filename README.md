# Задача А теперь купи кролика
## Json для локального тестирования из Postman
```json
{
  "meta": {
    "locale": "ru-RU",
    "timezone": "UTC",
    "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
    "interfaces": {
      "screen": {},
      "payments": {},
      "account_linking": {}
    }
  },
  "session": {
    "message_id": 0,
    "session_id": "26ac22c5-66db-4f47-a466-74bf1efc2609",
    "skill_id": "8360d7f7-3f63-49a2-8b2e-89474a4d9087",
    "user": {
      "user_id": "509E1794C78925CB0722C32A63389952093D09E9CCB85735FD663EAFCF612C31"
    },
    "application": {
      "application_id": "D4AB8B932DA7656EBE6ACF3A82FCEA1372114380AD6F665C821A1EBBF2D25730"
    },
    "user_id": "D4AB8B932DA7656EBE6ACF3A82FCEA1372114380AD6F665C821A1EBBF2D25730",
    "new": true
  },
  "request": {
    "command": "",
    "original_utterance": "",
    "nlu": {
      "tokens": [],
      "entities": [],
      "intents": {}
    },
    "markup": {
      "dangerous_context": false
    },
    "type": "SimpleUtterance"
  },
  "version": "1.0"
}
```
## Локальное тестирование
Склонировать репозиторий, запустить файл main из PyCharm
### Адрес для Postman 
http://127.0.0.1:5000/post

## Тестирование из сети интернет
### Адрес для Postman
https://lucky-ruby-cartoon.glitch.me/post

## Тестирование навыка в Алисе
https://dialogs.yandex.ru/developer/skills/8360d7f7-3f63-49a2-8b2e-89474a4d9087/draft/test
