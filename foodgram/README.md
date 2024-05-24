### Автор: [Антон Браун](https://github.com/merkme "Author's github")
---
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)

# Foodgram - цифровой кулинарный помощник.
__FOODGRAM - это то, что вам нужно! Все рецепты в 1 месте!__  
_Устали звонить маме или бабушке, чтобы спросить рецепт вашего любимого блюда?_  

---
В это трудно поверить, но после регистрации вы сразу сможете:

|Навык|Получаете сразу|
|---|---|
|Приготовить свои любимые маринованные огурчики|&check;|
|Окунуться в детство, повторив любимые блюда|&check;|
|Узнать что-то новое и стать ещё круче!|&check;|

Foodgram сделает ваши дни вкуснее, острее и наполнит вашу жизнь вкусом.  
Foodgram это место, где вы научитесь ~~рыбачить~~ готовить себе еду и будете сыты всю жизнь.  


<dl> 
	<dt>©Дай человеку рыбу, и ты накормишь его на один день, научи его рыбачить, и он будет сыт всю жизнь</dt>
	<dd>Автор: Дзэнко Судзуки</dd> 
</dl>


---

### Возможности проекта:

- Добавление рецептов
- Подписка на авторов рецептов, а так же добавления рецептов в избранное и корзину.
- Получать полный список ингридиентов, которые нужно купить для приготовления рецептов из корзины.

## Как запустить проект?


Подключаемся к нашему серверу:
```
ssh <username>@<ipadress>
```
Скачайте и установите curl — консольную утилиту, которая умеет скачивать файлы по команде пользователя:
```
sudo apt update
sudo apt install curl
```
С помощью утилиты curl скачайте скрипт для установки докера с официального сайта. Этот скрипт хорош тем, что сам определит и настроит вашу операционную систему.
```
curl -fSL https://get.docker.com -o get-docker.sh
```
Запустите сохранённый скрипт с правами суперпользователя:
```
# sh — программа для выполнения скриптов с командами терминала
sudo sh ./get-docker.sh
```
Дополнительно к Docker установите утилиту Docker Compose:
```
sudo apt install docker-compose-plugin
```
Проверьте, что всё работает:
```
sudo systemctl status docker
```
![IMAGE](https://pictures.s3.yandex.net/resources/S16_07_1691838427.png)

Теперь нам потребуется установить git:
```
sudo apt install git
```
Настраиваем конфиг:
```
git config --global user.name "Ваше имя"
git config --global user.email "ваш@example.com"
```
Создаём ключ SSH:
```
ssh-keygen -t rsa -b 4096 -C "ваш@example.com"
```
Добавьте ключ SSH в ваш аккаунт на GitHub:
Скопируйте содержимое вашего открытого ключа SSH (обычно в файле `~/.ssh/id_rsa.pub`) и добавьте его в настройках вашего аккаунта на GitHub. Вы можете это сделать на странице "Settings" -> "SSH and GPG keys".  

Чтобы убедиться, что все настроено правильно, вы можете выполнить команду:
```
ssh -T git@github.com

# После вы должны увидеть приветственное сообщение
# Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

Если всё так, то скачаем проект (ниже приведена команда для скачивания через SSH):  
```
git clone git@github.com:merkme/foodgram-project-react.git
```
Далее создадим файл .env (этот файл хранится на сервере, его нельзя никому показывать, он хранит ваши __секреты__):
```
nano .env
```
В него надо внести данные, которых не хватает (`<>` не нужны):
```
POSTGRES_PASSWORD=<your_password>
SECRET_KEY=<your_secret_key (you can put a long string there)>
ALLOWED_HOSTS=<your_host_ip>|<your_domain_name>
CSRF_TRUSTED_ORIGINS = https://*.<your_domain_name>.ru
POSTGRES_USER=posgres
POSTGRES_DB=foodgram
DB_NAME=foodgram
DB_HOST=db
DB_PORT=5432
DEBUG=False
```

Переходим в папку `/infra` и пишем:
```
sudo docker compose up
sudo docker compose exec backend python manage.py collectstatic
sudo docker compose exec backend python manage.py migrate

# Так же вы можете создать администратора сайта, выполнив команду
sudo docker compose exec backend python manage.py createsuperuser
```
После этого, наш сайт уже доступен по [ссылке](http://localhost:8090), если ваш сервер находится в вашей локальной сети, то всё, сайт уже будет вам доступен, если нет, то вам необходимо выполнить следующие шаги:  

Установка nginx на ваш сервер:
```
sudo apt install nginx -y 
```
Теперь запускаем nginx командой:
```
sudo systemctl start nginx 
```
Ну и сразу для вашей безопасности установите firewall на сервер:
```
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH 
```
Теперь включите файрвол:
```
sudo ufw enable 
```
В терминале выведется запрос на подтверждение операции с предупреждением, что команда может оборвать SSH-соединение:
`Command may disrupt existing ssh connections. Proceed with operation (y|n)?`
Подтвердите операцию — введите y и нажмите Enter.  
Вот такое сообщение`Firewall is active and enabled on system startup` говорит о том, что файрвол активен и будет включаться при запуске системы.  

Теперь настроим nginx:
```
sudo nano /etc/nginx/sites-enabled/default 
```
И туда впишите следующее:
```
server {
    server_name your_server_ip;

    location / {
    proxy_pass http://127.0.0.1:8090;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```
После этого перезагрузите nginx:
```
sudo systemctl reload nginx
```
После этого foodgram станет доступен по адресу вашего сервера. Ура, Вы справились!  

## API проекта
С API проекта вы сможете ознакомиться по ссылке: `server_ip/docs/`  

Так же будет пример запросов и ответов на них.
