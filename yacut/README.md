## Автор: [Антон Браун](https://github.com/merkme "Author's github")
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)


# Проект для генирации короткой ссылки.
Перед запуском проекта создайте в корневой директории проекта файл .env
```
# Измените настройки перед тем как запускать его в работу (если требуется)
# для локального запуска не требуется никаких изменений

FLASK_APP=yacut

# FLASK_ENV ставим на production, если планируем его деплоить.
FLASK_ENV=development

# База данных sqlite3, но вы можете подключить любую другую.
DATABASE_URI=sqlite:///db.sqlite3

# SECRET_KEY рекомендуется заменить на более сложный ключ
SECRET_KEY=YOUR_SECRET_KEY
```
### Для запуска проекта есть 2 пути:
#### Первый путь (у вас должен быть установлен Python):
Из корневой директории пишем в терминал:
```
chmod +x setup.sh
```
```
./setup.sh
```
После этого сервер будет доступен локально по адресу [127.0.0.1:5000](127.0.0.1:5000 "Адрес на локальной машине" )
#### Второй путь (для опытных пользователей):
```
git clone 
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
Запустить flash shell
```
flask shell
```
Импортировать базу данных db:
```
from yacut import db
```
Создать базу данных и таблицы:
```
db.create_all()
```
Запустить проект
```
flask run
```
После этого сервер будет доступен локально по адресу [127.0.0.1:5000](127.0.0.1:5000 "Адрес на локальной машине" )
