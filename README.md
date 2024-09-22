
# User Management API

Этот проект представляет собой API для управления пользователями с использованием FastAPI и PostgreSQL. Основные возможности включают:

- Создание пользователей
- Аутентификация пользователей с использованием токенов JWT
- Чтение информации о пользователях
- Обновление информации о пользователях
- Удаление пользователей

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/kojabu/test_task.git
   ```

2. Перейдите в каталог проекта:
   ```bash
   cd test_task
   ```

3. Создайте виртуальное окружение:
   ```bash
   python -m venv .venv
   ```

4. Активируйте виртуальное окружение:
   - На Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - На macOS и Linux:
     ```bash
     source .venv/bin/activate
     ```

5. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

6. Настройте базу данных PostgreSQL и добавьте данные для подключения в файл `database.py`:
   ```python
   SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost/db_name"
   ```

7. Запустите сервер разработки:
   ```bash
   uvicorn main:app --reload
   ```

## Эндпоинты

После запуска приложения можно просматривать документацию API на локальном сервере:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Основные эндпоинты:

- **POST** `/auth/` - Создать нового пользователя
- **POST** `/auth/token` - Получить JWT токен для авторизации
- **GET** `/users/all` - Получить всех пользователей
- **GET** `/users/{user_id}` - Получить информацию о пользователе по ID
- **PUT** `/update/{user_id}` - Обновить информацию пользователя
- **DELETE** `/delete/{user_id}` - Удалить пользователя
- **GET** `/` - Корневая точка
