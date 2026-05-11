# Технологии программирования

Репозиторий с выполненными заданиями по курсу **«Технологии программирования»**.

Курс был построен вокруг практических задач на работу с Linux/Bash, Git, Python, тестированием, FastAPI, C/C++-сборкой, PyBind11, Docker, Docker Compose и GitLab CI.  
Каждое задание выполнено в отдельной ветке.

## Навигация по репозиторию

| Ветка | Раздел курса | Краткое содержание |
|---|---|---|
| `task0` | Вводное задание | Создание приватного репозитория, настройка прав, исполняемый `run.sh`, первый Merge Request |
| `bash/logs` | Bash, Linux, обработка файлов | Скрипт фильтрации логов, разбор аргументов, регулярные выражения, сортировка и вывод |
| `bash/lu` | Bash, численные вычисления | LU-разложение матрицы из CSV-файла с выводом матриц `L` и `U` |
| `1` — `17`, `git/sub` | Git | Merge/rebase, конфликты, revert/reset/amend, cherry-pick, интерактивный rebase, submodules |
| `pybind` | PyBind11, CMake, C++/Python | Реализация Python-пакета `fastdict` с C++-структурой данных и биндингами через PyBind11 |
| `task-fastapi` | FastAPI, REST API | Микросервис для ветеринарной клиники с CRUD-операциями |
| `task-testing-python` | Pytest, тестирование | Покрытие тестами готового Python-проекта, моки, времнные файлы и директории, параметризация, проверка покрытия |
| `task-ci` | GitLab CI/CD | Настройка CI pipeline: установка зависимостей, запуск тестов |
| `task-docker` | Docker | Docker-образ для проекта с CMake и Flask-приложением |
| `task-docker-compose` | Docker Compose | Оркестрация backend, базы данных, init-контейнера и frontend |

## Как посмотреть конкретное задание

```bash
git clone https://github.com/Bred0id/Programming_technologies.git
cd Programming_technologies
git switch <branch-name>
```

Для каждого задания исходное условие сохранено в `README.md` соответствующей ветки.

---

# Затронутые технологии

## Linux и Bash

В рамках курса отрабатывалась работа с Linux-окружением и написание shell-скриптов для практических задач: обработки файлов, фильтрации логов и численных вычислений.

### Использованные инструменты и темы

- файловая система Linux;
- типы файлов и права доступа;
- `chmod`, `chown`, `chgrp`;
- shebang;
- переменные окружения;
- `PATH`, `PWD`, `OLDPWD`, `IFS`;
- `stdin`, `stdout`, `stderr`;
- перенаправления потоков;
- pipe;
- работа с аргументами скрипта;
- переменные Bash;
- индексированные и ассоциативные массивы;
- циклы, ветвления и функции;
- регулярные выражения;
- обработка CSV;
- `grep`, `cut`, `wc`, `rev`, `tr`;
- `sort`, `head`, `tail`;
- `find`, `xargs`, `tee`, `timeout`, `time`;
- `awk`, `sed`, `diff`;
- `bc` для вычислений с плавающей точкой;
- различие `LF` и `CRLF`.

---

## Git и командная разработка

Большой блок курса был посвящен Git: от базовых операций до исправления истории, конфликтов, интерактивного rebase и submodules.

### Использованные инструменты и темы

- локальный и удаленный репозиторий;
- `origin`;
- `git init`;
- `git clone`;
- `git add`;
- `git commit`;
- `git push`;
- `git pull`;
- `git fetch`;
- ветки и теги;
- `HEAD`;
- `git checkout`;
- `git switch`;
- `git restore`;
- `git merge`;
- `git rebase`;
- `git cherry-pick`;
- интерактивный rebase;
- squash;
- amend;
- merge conflicts;
- `git revert`;
- `git reset --soft`;
- `git reset --mixed`;
- `git reset --hard`;
- detached HEAD;
- `.gitignore`;
- `.gitkeep`;
- Git objects;
- file modes;
- executable bit;
- hooks;
- stash;
- submodules;
- `git diff`;
- `git log`;
- `git show`;
- `git status`.

### Практические результаты

В ветках `1` — `17` были отработаны различные сценарии Git:

- слияние веток;
- разрешение конфликтов;
- откат отдельных коммитов;
- откат ветки к прошлому состоянию;
- перенос коммитов между ветками;
- редактирование старых коммитов;
- исправление line endings;
- исправление прав исполняемых файлов;
- работа с историей проекта.
- git hooks

В ветке `git/sub` отдельно отработана работа с `git submodule`: подключение внешнего репозитория, инициализация после клонирования и взаимодействие с сервисом через именованные каналы `FIFO`.

---

## Python, FastAPI и REST API

В курсе затрагивалась разработка Python-сервисов и реализация REST API на FastAPI.

### Использованные инструменты и темы

- Python project layout;
- зависимости проекта;
- виртуальное окружение;
- FastAPI;
- Pydantic;
- REST API;
- HTTP/HTTPS;
- CRUD;
- route decorators;
- query parameters;
- path parameters;
- request/response models;
- HTTP status codes;
- обработка ошибок;
- OpenAPI/Swagger;
- ASGI;
- `uvicorn`;
- асинхронная модель выполнения;
- `async`/`await`;
- сравнение Flask и FastAPI.

---

## Тестирование Python-кода

Отдельная часть курса была посвящена тестированию: от базовых unit-тестов до моков, фикстур и проверки внешнего API.

### Использованные инструменты и темы

- `pytest`;
- `assert`;
- `pytest.raises`;
- `pytest.warns`;
- fixtures;
- `pytest.mark`;
- `parameterize`;
- `skip`;
- `skipif`;
- `monkeypatch`;
- mock testing;
- coverage;
- тестирование исключений;
- тестирование файловой системы;
- тестирование внешнего API через заглушки;
- unit-тесты;
- интеграционные сценарии;
- white box / black box / gray box;
- mutation testing;
- static analysis;
- linters;
- E2E testing.

---

## GitLab CI/CD

CI/CD-блок был связан с автоматизацией проверок для Python-проекта.

### Использованные инструменты и темы

- GitLab CI;
- `.gitlab-ci.yml`;
- stages;
- jobs;
- runner tags;
- установка зависимостей в pipeline;
- запуск тестов в CI;
- публикация результатов тестов;
- linting;
- проверка Merge Request;
- различие локального запуска и запуска внутри CI.

---

## C++, CMake и PyBind11

Курс затрагивал интеграцию C++ и Python: сборку C++-кода, создание Python extension module и экспорт C++-классов в Python.

### Использованные инструменты и темы

- C++;
- CMake;
- Make;
- этапы сборки C/C++;
- препроцессинг;
- компиляция;
- линковка;
- `add_executable`;
- `add_library`;
- `target_link_libraries`;
- `PUBLIC`;
- `PRIVATE`;
- `INTERFACE`;
- статические библиотеки;
- динамические библиотеки;
- `find_package`;
- header guards;
- `#pragma once`;
- Python C API;
- PyBind11;
- `py::class_`;
- `py::object`;
- `py::self`;
- `py::dynamic_attr`;
- `def_property`;
- `def_readwrite`;
- GIL;
- `py::gil_scoped_acquire`;
- `py::gil_scoped_release`;
- обработка исключений;
- сборка `.so`-модуля.

### Практические результаты

В ветке `pybind` реализован Python-пакет `fastdict` с C++-реализацией структуры данных и биндингами через PyBind11.

Поддержанный интерфейс:

```python
from fastdict import FastDict

d = FastDict()

d[key] = value
value = d[key]

key in d
len(d)

d.keys()
d.values()
d.items()

del d[key]
```

Дополнительно выполнено сравнение с обычным Python `dict` по времени и памяти на операциях вставки, поиска и удаления.

---

## Docker

Docker-блок был посвящен упаковке приложения в контейнер и настройке окружения внутри Docker-образа.

### Использованные инструменты и темы

- виртуализация и контейнеризация;
- Docker image;
- Docker container;
- Dockerfile;
- layers;
- build cache;
- cache miss;
- `FROM`;
- `RUN`;
- `COPY`;
- `ADD`;
- `ENV`;
- `ARG`;
- `CMD`;
- `ENTRYPOINT`;
- `WORKDIR`;
- `USER`;
- `EXPOSE`;
- `VOLUME`;
- bind mounts;
- volumes;
- tmpfs;
- `.dockerignore`;
- Docker registry;
- tags;
- `latest`;
- `alpine`;
- `busybox`;
- multi-stage build;
- управление контейнерами;
- `docker build`;
- `docker run`;
- `docker ps`;
- `docker images`;
- `docker rm`;
- `docker rmi`;
- `docker inspect`;
- `docker logs`.

---

## Docker Compose и оркестрация контейнеров

Docker Compose-блок был посвящен запуску многоконтейнерного приложения: backend, база данных, init-контейнер и frontend.

### Использованные инструменты и темы

- YAML;
- Docker Compose;
- services;
- networks;
- volumes;
- environment variables;
- `.env`;
- `depends_on`;
- healthcheck;
- restart policies;
- logs;
- replicas;
- secrets;
- init containers;
- backend/frontend interaction;
- постоянное хранение данных в volume.

---

# Общий результат

В рамках курса был собран репозиторий, который покрывает полный путь от базовой работы с системой и Git до запуска контейнеризированного backend-приложения с CI/CD:

1. организация репозитория и Merge Request workflow;
2. Bash-скрипты для обработки данных;
3. практическое владение Git;
4. Python API на FastAPI;
5. тестирование Python-кода;
6. настройка CI/CD;
7. C++/Python integration через PyBind11;
8. Docker-сборка приложения;
9. Docker Compose для многоконтейнерного запуска.

Репозиторий можно использовать как портфолио по курсу: в нем отражены не только итоговые решения, но и набор технологий, которые применялись и защищались устно.
