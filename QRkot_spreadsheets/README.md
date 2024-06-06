### Автор: [Антон Браун](https://github.com/merkme "Author's github")
---
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white) ![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white) ![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)![Google Cloud](https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white)
> Перечисление приведено в порядке приоритета использования.

#  Кошачий благотворительный фонд (updated: Google.API).
__Сервис для поддержки котиков - каждому из нас иногда нужна помощь!__  

<dl> 
	<dt>©«То, как мы ведем себя по отношению к кошкам здесь, внизу, определяет наш статус на небесах».</dt>
	<dd>Автор: Роберт А. Хайнлайн.</dd> 
</dl>

![cats](https://mir-s3-cdn-cf.behance.net/project_modules/max_1200/1f842f38789415.576f2d0d0383a.jpg)
---
Благодаря этому сервису вы можете:

|Навык|Получаете сразу|
|---|---|
|Спасти котика|V|
|Сделать мир добрее|V|
|Получить незабываемый опыт|V|


Сделать всё это стало возможных не выходя из дома, сидя за компьютером, восторг! Не правда ли?

---

### 🔍 Возможности проекта:

- Создание благотворительных проектов и внесение пожертвований
- Реализован функционал, который гарантирует, что пока не закроется сбор на ранее созданный проект, средства не будут поступать в следующий
- Есть возможность ознакомиться со всеми проектами и пожертвованиями
- Возможность сформировать отчёт в виде google таблицы, чтобы узнать какие проекты закрываются быстрее.

## Как запустить проект?

Для того, чтобы запустить проект нам нужно выполнить несколько шагов:

1. **Склонировать проект к себе на компьютер:**
    ```bash
    # HTTPS протокол
    git clone https://github.com/merkme/cat_charity_fund.git
    # SSH протокол
    git clone git@github.com:merkme/cat_charity_fund.git
    ```

2. ** Создать и активировать виртуальное окружение:**

    ```bash
    python -m venv venv
    source venv/Scripts/activate
    ```

3. **Обновить пакетный менеджер *pip*:**
    ```bash
    python -m pip install --upgrade pip
    ```

4. **Установить зависимости из файла requirements.txt:**
    ```bash
    # для Windows
    pip install -r requirements_win.txt

    # для MacOS
    pip install -r requirements_mac.txt
    ```
5. **Создать файл .env (его нельзя никому показывать , он хранит ваши __секреты__):**
    ```bash
    nano .env
    ```
    📃 В него надо внести данные, которых не хватает (`<>` не нужны):
    ```
    APP_TITLE=Кошачий благотворительный фонд
    APP_DESCRIPTION=Сервис для поддержки котиков!
    DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
    SECRET=<какая-то ваша секретная фраза>
    FIRST_SUPERUSER_EMAIL=<логин пользователя с правами superuser>
    FIRST_SUPERUSER_PASSWORD=<пароль пользователя с правами superuser>

    EMAIL=<тут указываем ваш личный e-mail, для доступа к отчётам.>

    # Ниже укажите данные из файла credentials.json 
    # https://console.cloud.google.com/apis/credentials
  
    TYPE=
    PROJECT_ID=
    PRIVATE_KEY_ID=
    PRIVATE_KEY=
    CLIENT_EMAIL=
    CLIENT_ID=
    AUTH_URI=
    TOKEN_URI=
    Auth_provider_x509_cert_url=
    CLIENT_X509_CERT_URL=
    UNIVERSE_DOMAIN=
    ```
6. **✔️ Запуск проекта:**

    ```bash
    # Ввести команду в терминал Bash при активированном виртуальном окружении и находясь в корневой папке проекта
    uvicorn app.main:app
    ```
7. **В случае возникнования ошибки `Could not deserialize key data. The data may be in an incorrect format` при запуске:**  
  Внести изменения в файле QRkot_spreadsheets\app\core\google_client.py
  ```python
  INFO = {
    'type': settings.type,
    'project_id': settings.project_id,
    'private_key_id': settings.private_key_id,
    'private_key': settings.private_key.replace('\\n', '\n'),
    'client_email': settings.client_email,
    'client_id': settings.client_id,
    'auth_uri': settings.auth_uri,
    'token_uri': settings.token_uri,
    'auth_provider_x509_cert_url': settings.auth_provider_x509_cert_url,
    'client_x509_cert_url': settings.client_x509_cert_url
  }
  ```
---

## <u>Пример использования:</u>
> Дополнительная информация описана ниже в [примечании](#примечание)...


### Программный интерфейс:

1. **Эндпоинт: http://localhost:8000/auth/register/. Метод запроса: `POST`<br>Права доступа: Без ограничений**

    При передаче идентифицирующей информации о новом пользователе:
    ```json
    {
      "email": "string",
      "password": "string"
    }
    ```

    В ответ Вы получите полную сгенерированную информацию о зарегистрированном пользователе:

    ```json
    {
      "id": "int",
      "email": "string",
      "is_active": "bool",
      "is_superuser": "bool",
      "is_verified": "bool"
    }
    ```

2. **Эндпоинт: http://localhost:8000/auth/jwt/login/. Метод запроса: `POST`<br>Права доступа: Любой зарегистрированный пользователь**

    При передаче идентифицирующей информации о зарегистрированном пользователе:
    ```json
    {
      "email": "string",
      "password": "string"
    }
    ```

    В ответ Вы получите токен доступа и его тип для аутентификации при выполнении запросов:

    ```json
    {
      "access_token": "string",
      "token_type": "string"
    }
    ```

3. **Эндпоинт: http://localhost:8000/users/me/. Метод запроса: `GET`<br>Права доступа: Любой авторизованный пользователь**

    В ответ Вы получите полную информацию об авторизованном пользователе:
    ```json
    {
      "id": "int",
      "email": "string",
      "is_active": "bool",
      "is_superuser": "bool",
      "is_verified": "bool"
    } 
    ```

4. **Эндпоинт: http://localhost:8000/charity_project/. Метод запроса: `GET`<br>Права доступа: Без ограничений**

    В ответ Вы получите все существующие актуальные и закрытые проекты благотворительного фонда в виде списка:
    ```json
    [
      {
        "name": "string",
        "description": "string",
        "full_amount": "int",
        "id": "int",
        "invested_amount": "int",
        "fully_invested": "bool",
        "create_date": "datetime",
        "close_date": "datetime"
      }
    ]  
    ```

    > Если значение поля `fully_invested` находится в значении "true", то такой благотворительный проект является закрытым.

5. **Эндпоинт: http://localhost:8000/charity_project/. Метод запроса: `POST`<br>Права доступа: Суперпользователь**
    При передаче информации о новом проекте благотворительного фонда:

    ```json
    {
      "name": "string",
      "description": "string",
      "full_amount": "int"
    }
    ```

    В ответ Вы получите полную сгенерированную информацию о созданном проекте благотворительного фонда:
    ```json
    {
      "name": "string",
      "description": "string",
      "full_amount": "int",
      "id": "int",
      "invested_amount": "int",
      "fully_invested": "bool",
      "create_date": "datetime",
      "close_date": "datetime"
    }
    ```

6. **Эндпоинт: http://localhost:8000/charity_project/{project_id:int}. Параметры: `{project_id:int}` - ID благотворительного проекта в БД. Метод запроса: `PATCH`<br>Права доступа: Суперпользователи**

    При передаче информации о новом проекте благотворительного фонда:

    ```json
    {
      "name": "string",
      "description": "string",
      "full_amount": "int"
    }
    ```

    > Если поле `full_amount` передано со значением, равным уже инвестированной сумме в этот проект (поле `invested_amount`) - благотворительный проект автоматически становится закрытым.

    > *Поля можно изменять как множественно, так и одиночно.*

    В ответ Вы получите полную сгенерированную информацию о созданном проекте благотворительного фонда:
    ```json
    {
      "name": "string",
      "description": "string",
      "full_amount": "int",
      "id": "int",
      "invested_amount": "int",
      "fully_invested": "bool",
      "create_date": "datetime",
      "close_date": "datetime"
    }
    ```

7. **Эндпоинт: http://localhost:8000/donations/. Метод запроса: `GET`<br>Права доступа: Суперпользователи**

    В ответ Вы получите все существующие инвестированные и неинвестированные пожертвования пользователей в виде списка:
    ```json
    [
      {
        "full_amount": "int",
        "comment": "string",
        "id": "int",
        "create_date": "datetime",
        "user_id": "int",
        "invested_amount": "int",
        "fully_invested": "bool",
        "close_date": "datetime"
      }
    ]
    ```


8. **Эндпоинт: http://localhost:8000/donations/. Метод запроса: `POST`<br>Права доступа: Любой авторизованный пользователь**

    При передаче краткой информации о пожертвовании:

    ```json
    {
      "full_amount": "int",
      "comment": "string"
    }
    ```

    В ответ Вы получите полную сгенерированную информацию о созданном пожертвовании в благотворительный фонд:
    ```json
    {
      "full_amount": "int",
      "comment": "string",
      "id": "int",
      "create_date": "datetime"
    }
    ```

8. **Эндпоинт: http://localhost:8000/google/. Метод запроса: `POST`<br>Права доступа: Суперпользователи**

    При отправке данного запроса, вы получите ссылку на файл с отчётом, который будет представлен в виде google sheets
    ```json
    {
      "https://docs.google.com/spreadsheets/d/spreadsheetsId"
    }
    ```

    > При создании пожертвования и наличия незакрытых благотворительных проектов, такое пожертвование засчитывается в пользу первого по дате создания незакрытого благотворительного проекта. Если инвестируемая сумма больше необходимой цели закрытия инвестируемого благотворительного фонда — она засчитывается в пользу следующих за текущим открытых благотворительных проектов, если таковые существуют. После закрытия всех благотворительных проектов, избыточные инвестиции замораживаются и засчитываются в счет вновь открывшихся благотворительных проектов.

---

### Примечание:
>В данном руководстве, в качестве примера, приведена основная часть вариантов использования проекта.

*По умолчанию веб-сервер использует [8000 порт локального хоста](http://localhost:8000/).*

>Далее, есть возможность воспользоваться как веб-интерфейсом, [перейдя по ссылке в веб-браузере](http://localhost:8000/docs), так и программным интерфейсом, через любой HTTP-клиент.

