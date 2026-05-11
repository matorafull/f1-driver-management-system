# 🏎️ F1 Driver Management System

Веб-приложение для управления данными чемпионата Формулы-1. Система позволяет отслеживать информацию о пилотах и командах, а также визуализировать текущее положение в личном зачете и Кубке конструкторов в реальном времени.

## 🚀 Основные функции

* **Live Dashboard**: Автоматический расчет очков и отображение таблиц WDC (World Drivers' Championship).
* **Driver Management**: Управление списком пилотов (добавление, просмотр, удаление).
* **Team Management**: Система регистрации команд.
* **Relational Database**

## 🛠 Технологический стек

* **Backend**: Python 3.12, FastAPI
* **Database**: PostgreSQL + SQLAlchemy (ORM)
* **Frontend**: Bootstrap 5, JavaScript

---

## ⚙️ Инструкция по запуску

### 1. Предварительные требования
Убедитесь, что у вас установлены:
* Python 3.12
* PostgreSQL

### 2. Клонирование и настройка окружения
```bash
# Клонируйте репозиторий
git clone "https://github.com/matorafull/f1-driver-management-system"
cd f1-driver-management-system

# Создайте и активируйте виртуальное окружение
python -m venv venv

# Для Windows (PowerShell):
.\venv\Scripts\activate

# Установите зависимости
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv jinja2 python-multipart

### 3. Настройка базы данных
1.  Создайте базу данных в PostgreSQL (например, `f1_db`).
2.  Создайте в корне проекта файл `.env` и добавьте туда строку подключения:
    ```env
    DATABASE_URL=postgresql://user:password@localhost:5432/f1_db
    ```

3.  При первом запуске SQLAlchemy автоматически создаст все необходимые таблицы на основе описанных моделей.

### 4. Запуск приложения
Выполните следующую команду из корня проекта:
```bash
python -m uvicorn src.main:app --reload

После запуска приложение будет доступно по адресу: http://127.0.0.1:8000

---

## 📂 Структура проекта

* `src/main.py` — Точка входа, API-эндпоинты и маршрутизация.
* `src/models.py` — Описание схем таблиц базы данных (SQLAlchemy).
* `src/database.py` — Конфигурация подключения к PostgreSQL.
* `templates/` — HTML-шаблоны страниц.
* `static/` — Статические файлы (CSS стили, JS скрипты).

---
**Разработчик:** Eldiiar Sadykov 
**Проект в рамках курса Databases**
