## Автор: [Антон Браун](https://github.com/merkme "Author's github")
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

# Проект парсинга pep

### Описание:
Парсер собирает информацию по Python, полезный инструмент, который позволяет всегда оставаться вкурсе всех самых последних новостей.  

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=100&size=17&duration=4998&pause=1000&color=27F72F&random=false&width=435&lines=Don't+waste+your+time%2C+let+parser+helps)](https://git.io/typing-svg)
### Функционал:
Данный парсер имеет 4 режима работы: __whats_new__ | __latest-versions__ | __download__ | __pep__

### Дополнительные фичи:
Есть возможность запускать парсер с очисткой кеша, так же можно выводить результат работы парсера используя __PrettyTable__ или же получить __.csv file__

### Как запустить парсер

Запуск парсера о нововведениях в Python и их авторов
```
python main.py whats-new
```
Запуск парсера версий Python и их статусов
```
python main.py latest-versions
```
Запуск парсера, который скачивает архив документации Python
```
python main.py download
```
Запустить парсинг документации PEP
```
python main.py pep
```

### Дополнительные аргументы:
Получить полный список аргументов:
```
python main.py -h
```
