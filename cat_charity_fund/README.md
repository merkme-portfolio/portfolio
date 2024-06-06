### Автор: [Антон Браун](https://github.com/merkme "Author's github")
---
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white) ![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white) ![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
> Перечисление приведено в порядке приоритета использования.

# 😻 Кошачий благотворительный фонд.
__Сервис для поддержки котиков - каждому из нас иногда нужна помощь!__  

<dl> 
	<dt>©«То, как мы ведем себя по отношению к кошкам здесь, внизу, определяет наш статус на небесах».</dt>
	<dd>Автор: Роберт А. Хайнлайн.</dd> 
</dl>

![cats](https://img.freepik.com/premium-photo/cats-couple-love-with-hearts-valentine-s-day-card-3d-render-illustration_691560-7404.jpg)
---
Благодаря этому сервису вы можете:

|Навык|Получаете сразу|
|---|---|
|Спасти котика|😽|
|Сделать мир добрее|😽|
|Получить незабываемый опыт|😽|

Сделать всё это стало возможных не выходя из дома, сидя за компьютером, восторг! Не правда ли?

---

### 🔍 Возможности проекта:

- Создание благотворительных проектов и внесение пожертвований
- Реализован функционал, который гарантирует, что пока не закроется сбор на ранее созданный проект, средства не будут поступать в следующий
- Есть возможность ознакомиться со всеми проектами и пожертвованиями

## 💡 Как запустить проект?

Для того, чтобы запустить проект нам нужно выполнить несколько шагов:

1. **📁 Склонировать проект к себе на компьютер:**
    ```bash
    # HTTPS протокол
    git clone https://github.com/merkme/cat_charity_fund.git
    # SSH протокол
    git clone git@github.com:merkme/cat_charity_fund.git
    ```

2. **🔧 Создать и активировать виртуальное окружение:**

    ```bash
    python -m venv venv
    source venv/Scripts/activate
    ```

3. **⏳ Обновить пакетный менеджер *pip*:**
    ```bash
    python -m pip install --upgrade pip
    ```

4. **⏳Установить зависимости из файла requirements.txt:**
    ```bash
    pip install -r requirements.txt
    ```
5. **⚠️ Создать файл .env (его нельзя никому показывать , он хранит ваши __секреты__):**
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
    ```
6. **✔️ Запуск проекта:**

    ```bash
    # Ввести команду в терминал Bash при активированном виртуальном окружении и находясь в корневой папке проекта
    uvicorn app.main:app
    ```
---

## ▶️ <u>Пример использования:</u>
> Дополнительная информация описана ниже в [примечании⬇️](#примечание)...


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

    > При создании пожертвования и наличия незакрытых благотворительных проектов, такое пожертвование засчитывается в пользу первого по дате создания незакрытого благотворительного проекта. Если инвестируемая сумма больше необходимой цели закрытия инвестируемого благотворительного фонда — она засчитывается в пользу следующих за текущим открытых благотворительных проектов, если таковые существуют. После закрытия всех благотворительных проектов, избыточные инвестиции замораживаются и засчитываются в счет вновь открывшихся благотворительных проектов.

---

### Примечание:
>В данном руководстве, в качестве примера, приведена основная часть вариантов использования проекта.

*По умолчанию веб-сервер использует [8000 порт локального хоста](http://localhost:8000/).*

>Далее, есть возможность воспользоваться как веб-интерфейсом, [перейдя по ссылке в веб-браузере](http://localhost:8000/docs), так и программным интерфейсом, через любой HTTP-клиент.

