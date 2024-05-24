## Автор: [Антон Браун](https://github.com/merkme "Author's github")
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)


# Проект для парсинга информации о PEP Python.

### Описание:
Асинхронный парсер, который собирает информацию по PEP Python. 

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=100&size=17&duration=4998&pause=1000&color=27F72F&random=false&width=435&lines=Don't+waste+your+time%2C+let+parser+helps)](https://git.io/typing-svg)
### Функционал:
При запуске парсера создаётся 2 файла:  
Файл в названии которого присутствует *PEP*, содержит следующую информацию: номер PEP, его название, а так же статус.  
 
Файл в названии которого присутствует *status_summary*, содержит следующую информацию: статус, а так же количество PEP с одинаковыми статусами, дополнительно выводится общее количество PEP.

### Как запустить парсер

Для начала скачаем проект:
```
# Пример для загрузки используя SSH-key
git clone git@github.com:merkme/scrapy_parser_pep.git
```
Создадим вирутальное окружение (делаем это в корневой папке проекта) и активируем:
```
python -m venv venv
. venv/Scripts/activate
# после этого вы должны увидеть надпись (venv) в консоли
```
Установим зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Запустить парсинг информации о PEP:
```
scrapy crawl pep
```
