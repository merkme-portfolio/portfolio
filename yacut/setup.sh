#!/bin/bash

# Создать виртуальное окружение
python -m venv venv

# Активировать виртуальное окружение
source venv/Scripts/activate

# Установить зависимости из файла requirements.txt
pip install -r requirements.txt

# Запустить Flask Shell и выполнить необходимые команды
echo "from yacut import db; db.create_all()" | flask shell

# Запустить проект
flask run