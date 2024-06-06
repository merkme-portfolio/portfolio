# API_KITTYGRAM

## 🔍 Описание:

**Проект KITTYGRAM** создан для ценителей своих котиков, которых
хозяин может опубликовать на платформе, чтобы похвастаться своим невероятно
красивым питомцем😊

**[API KITTYGRAM*](#api_kittygram)** - интерфейс для взаимодействия c пользователем, позволяющий получать, создавать, удалять и изменять объекты только своих котиков в базе данных [проекта](#описание).

![LOGOTYPE](https://sun9-46.userapi.com/impg/XFbDkOMrIg0MW-aq8SNvWlsKSFZeYiRfpDRd6Q/Qry-rwt_im8.jpg?size=540x440&quality=96&sign=e44c7ed46f95104b6525d2a725a64176&type=album "img.png")

---

## 💡 Как начать пользоваться проектом:
#### 1. Открыть проект в веб-браузере:
- Перейти по **[ссылке](https://www.kittygramm.shop)**, зарегистрироваться на сайте и разместить своего питомца.

#### 2. Запустить проект локально в контейнерах Docker:
**Рекомендуемые системные требования к компьютерам:**
- Ubuntu Linux 20.04 и выше;
- Windows 10 (2H20) и выше;
- macOS Monterey и выше.
  * Минимально необходимый объем ОЗУ компьютера — 4 Gb.

1. Установить Docker Desktop (версию, зависящую от Вашей ОС) на свой компьютер, с [официального сайта поставщика продукта.](https://www.docker.com/get-started/)

*Далее, если у Вас операционная система:*
- **Linux:**
  * можно пропустить этот шаг
- **Windows 8 или более ранние версии:**
  * нужно запускать проект при помощи виртуальной машины с ОС Linux Ubuntu
    через [программу Virtual Box](https://www.virtualbox.org/wiki/Downloads)
- **Windows 10 или 11:**
  * необходимо [установить утилиту Windows Subsystem for Linux ](https://learn.microsoft.com/ru-ru/windows/wsl/install)

> После выполнения шага, все сводится к дальнейшему использованию консоли для установки Docker:

2. Запустить Docker Desktop, установленную на шаге 1 данной инструкции;

3. Установить Docker (выполнение команд требуется выполнять последовательно):
```bash
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh

# Дополнительно к Docker установите утилиту Docker Compose:
sudo apt install docker-compose-plugin
# Проверить работу Docker'a:
sudo systemctl status docker
```
4. Склонировать репозиторий на свой компьютер и перейти в папку с ним:

```bash
git clone https://github.com/BIXBER/kittygram_final.git
cd kittygram_final/
```
5. ***Опционально:** создать, активировать и наполнить виртуальное окружение:*

    1. Создать и активировать виртуальное окружение:

    ```bash
    cd backend/
    python -m venv venv
    source venv/Scripts/activate
    ```

    2. Установить зависимости из файла requirements.txt, предварительно обновив пакетный менеджер pip:

    ```bash
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

6. Поднять контейнеры на основе уже созданных образов:
```bash
sudo docker compose up
```

7. Перейти в директорию с файлом docker-compose.yml и выполнить миграции:
```bash
cd ..
docker compose exec backend python manage.py migrate
# Проект запустится на 9000 порту
```

8. [Открыть локальное подключение](http://localhost:9000) через браузер и начать пользоваться проектом!

> Если возникнут некоторые трудности при установке Docker или непосредственно в его работе - вот 
  **[ссылка](https://code.s3.yandex.net/backend-developer/learning-materials/%D0%A3%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B1%D0%BB%D0%B5%D0%BC%20Docker%20for%20Windows.pdf)** с возможными решениями некоторых проблем.
---

## ▶️ Примеры запросов:
> Перед запуском ознакомьтесь с условиями, описанные в [примечании⬇️](#примечание)...
1. **Эндпоинт: https://www.kittygramm.shop/api/users/. Метод запроса: POST<br>Права доступа: Доступно без токена**

    При передаче следующих данных:

    * "username": "string" **(required)**,
    * "password": "string" **(required)**,
    * "email": "string"

    Вы получите ответ о создании нового пользователя:

    * "email": "string"
    * "username": "string",
    * "id": "integer"

<br>

2. **Эндпоинт: https://www.kittygramm.shop/api/token/login/. Метод запроса: POST<br>Права доступа: Доступно без токена**

    При передаче имени зарегистрированного пользователя и пароля:

    * "username": "string" **(required)**,
    * "password": "string" **(required)**
    
    Вам в ответе будет выдан ***JWT Token***, позволяющий авторизоваться:

    * "auth_token": "string"

  > ***JWT Token*** необходимо вставить в *header* вашего запроса под ключом `Authorization`: `Token <ваш_токен>`

<br>

3. **Эндпоинт: https://www.kittygramm.shop/api/cats/. Метод запроса: GET<br>Права доступа: Авторизованный пользователь**

    В ответ вы получите список всех котиков, которые имеются в базе данных проекта. Опционально, можно параметризировать запрос номером страницы с котиками: для этого необходимо дописать к запросу следующую строку: `?page=<номер_страницы>`.

<br>

4. **Эндпоинт: https://www.kittygramm.shop/api/cats/ Метод запроса: POST.<br> Права доступа: Авторизованный пользователь**

    При передаче следующих данных **в теле запроса**:

    * "name": "string" **(required)**,
    * "color": "string (hex-format)" **(required)**,
    * "birth_year": "integer" **(required)**,
    * "achievements": [{"achievement_name": "string"}, {"achievement_name": "string"}, etc...],
    * "image_url": "url"
    
    В базу будет добавлен новый котик и придет ответ в виде:

    * "id": "integer",
    * "name": "string",
    * "color": "string",
    * "birth_year": "integer",
    * "achievements": "list",
    * "owner": "integer",
    * "age": "integer",
    * "image": "url",
    * "image_url": "url"

  > В качестве примера, в параметре `color` запроса можно использовать значение `#000000`, которое отображает черный цвет

---

### Примечание:
> Проект **[API KITTYGRAM](#api_kittygram)** находится во временном доступе для пользователей сети. В связи с этим, в случае, если эндпоинт с доменным именем https://www.kittygramm.shop/ недоступен - Вы можете [использовать проект локально](#2-запустить-проект-локально-на-компьютере) на своем компьютере, соответственно отправляя запросы на эндпоинт http://127.0.0.1:9000/
> **В данном руководстве, в качестве примера приведена лишь часть запросов к эндпоинтам, имеющихся в проекте [API KITTYGRAM](#api_kittygram)**