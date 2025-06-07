# Система Турниров

Мини-система турниров, созданная с использованием FastAPI для управления турнирами и регистрации игроков.

## Функции

- Создание турниров с ограничением по количеству игроков и датой начала
- Регистрация игроков в турнирах с валидацией email
- Предотвращение дублирования регистраций и переполнения турниров
- Получение списка зарегистрированных игроков для каждого турнира
- Полностью асинхронная реализация с FastAPI и SQLAlchemy 2.0

## Технологический стек

- **Python 3.11+**
- **FastAPI** - Современный веб-фреймворк для создания API
- **SQLAlchemy 2.0** - Асинхронная ORM
- **PostgreSQL** - База данных
- **Alembic** - Миграции базы данных
- **Pydantic** - Валидация данных
- **Docker & Docker Compose** - Контейнеризация
- **Pytest** - Фреймворк тестирования
- **MyPy** - Проверка типов
- **Ruff** - Линтер
- **Black** - Форматирование кода

## Структура проекта

```
project/
├── app/
│   ├── main.py              # Точка входа FastAPI приложения
│   ├── config.py            # Настройки конфигурации
│   ├── db.py                # Подключение к базе данных и сессии
│   ├── models/
│   │   └── tournament.py    # SQLAlchemy модели
│   ├── schemas/
│   │   └── tournament.py    # Pydantic схемы
│   ├── repositories/
│   │   └── tournament.py    # Слой доступа к данным
│   ├── services/
│   │   └── tournament.py    # Слой бизнес-логики
│   └── api/
│       └── tournament.py    # API маршруты
├── alembic/                 # Миграции базы данных
├── tests/
│   └── test_registration.py # Тестовые случаи
├── docker-compose.yml       # Конфигурация Docker сервисов
├── Dockerfile              # Контейнер приложения
├── pyproject.toml          # Конфигурация проекта и зависимости
├── Makefile                # Команды разработки
└── README.md               # Этот файл
```

## API Endpoints

### Создание турнира
```http
POST /api/v1/tournaments
Content-Type: application/json

{
  "name": "Weekend Cup",
  "max_players": 8,
  "start_at": "2025-06-01T15:00:00Z"
}
```

### Регистрация игрока
```http
POST /api/v1/tournaments/{tournament_id}/register
Content-Type: application/json

{
  "name": "Иван Иванов",
  "email": "ivan@example.com"
}
```

### Получение игроков турнира
```http
GET /api/v1/tournaments/{tournament_id}/players
```

## Быстрый старт

### Требования
- Docker и Docker Compose
- Python 3.11+ (для локальной разработки)

### Запуск с Docker (Рекомендуется)

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd tournament-system
```

2. Скопируйте файл окружения:
```bash
cp .env.example .env
```

3. Запустите приложение:
```bash
make dev
# или
docker compose up --build
```

API будет доступно по адресу `http://localhost:8000`

Документация API доступна по адресу `http://localhost:8000/docs`

### Локальная разработка

1. Установите зависимости:
```bash
make install
# или
pip install -e .[dev]
```

2. Запустите базу данных PostgreSQL:
```bash
docker compose up db
```

3. Выполните миграции:
```bash
make migrate-docker
# или
docker compose exec app alembic upgrade head
```

4. Запустите сервер разработки:
```bash
uvicorn app.main:app --reload
```

## Команды разработки

### 🚀 Разработка
```bash
# Запуск сервера разработки
make dev

# Запуск в фоновом режиме
make dev-d

# Остановка всех контейнеров
make stop

# Просмотр логов
make logs
```

### 🧪 Тестирование
```bash
# Запуск тестов в Docker (рекомендуется)
make test-docker

# Запуск тестов с чистой базой данных
make test-clean

# Локальные тесты
make test
```

### 🔍 Качество кода
```bash
# Проверка линтером в Docker
make lint-docker

# Форматирование кода в Docker
make format-docker

# Проверка типов в Docker
make type-check-docker

# Локальные проверки
make lint
make format
make type-check
```

### 🗄️ База данных
```bash
# Выполнение миграций в Docker
make migrate-docker

# Локальные миграции
make migrate
```

### 🛠️ Утилиты
```bash
# Полная очистка
make clean

# Помощь по командам
make help
```

## Миграции базы данных

Для создания новой миграции после изменения моделей:

```bash
# В Docker контейнере
docker compose exec app alembic revision --autogenerate -m "Описание изменений"
docker compose exec app alembic upgrade head
```

## Тестирование

Запуск набора тестов:

```bash
# В Docker (рекомендуется)
make test-docker

# Локально
make test
```

Тесты включают:
- Создание турниров
- Валидацию регистрации игроков
- Предотвращение дублирования email
- Ограничения вместимости турниров
- Обработку ошибок

## Качество кода

Проект использует несколько инструментов для поддержания качества кода:

- **MyPy** для статической проверки типов
- **Ruff** для линтинга
- **Black** для форматирования кода
- **Pytest** для тестирования

Запуск всех проверок качества:

```bash
make lint-docker
make type-check-docker
make format-docker
make test-docker
```

## Переменные окружения

Создайте файл `.env` на основе `.env.example`:

```bash
DATABASE_URL=postgresql+asyncpg://tournament_user:tournament_pass@localhost:5432/tournament_db
DEBUG=true
```

## Архитектура

Приложение следует шаблону многослойной архитектуры:

- **API слой** (`app/api/`): FastAPI маршруты и обработка запросов/ответов
- **Сервисный слой** (`app/services/`): Бизнес-логика и валидация
- **Репозиторий слой** (`app/repositories/`): Доступ к данным и операции с базой данных
- **Модельный слой** (`app/models/`): SQLAlchemy модели базы данных
- **Схемы слой** (`app/schemas/`): Pydantic модели для валидации

## Бизнес-правила

1. **Создание турниров**: Турниры должны иметь название, максимальное количество игроков и дату начала
2. **Регистрация игроков**: 
   - Игроки должны предоставить корректное имя и email
   - Один email может зарегистрироваться в турнире только один раз
   - Нельзя превышать максимальное количество игроков в турнире
3. **Валидация данных**: Все входящие данные валидируются с помощью Pydantic схем
4. **Обработка ошибок**: Правильные HTTP статус-коды и сообщения об ошибках для всех сценариев

## Рекомендуемый рабочий процесс

**Первый запуск:**
```bash
# Запуск приложения
make dev
```

**Ежедневная разработка:**
```bash
make dev-d      # Запуск в фоне
make logs       # Просмотр логов при необходимости
make test-docker # Запуск тестов
make stop       # Остановка в конце дня
```

**Перед коммитом:**
```bash
make format-docker
make lint-docker
make type-check-docker
make test-docker
```

## Примеры использования

### Создание турнира
```bash
curl -X POST "http://localhost:8000/api/v1/tournaments" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Кубок выходного дня",
    "max_players": 16,
    "start_at": "2025-06-15T14:00:00Z"
  }'
```

### Регистрация игрока
```bash
curl -X POST "http://localhost:8000/api/v1/tournaments/1/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Алексей Петров",
    "email": "alexey@example.com"
  }'
```

### Получение списка игроков
```bash
curl -X GET "http://localhost:8000/api/v1/tournaments/1/players"
```

## Устранение неполадок

### Проблемы с Docker
```bash
# Очистка и перезапуск
make clean
make dev
```

### Проблемы с базой данных
```bash
# Пересоздание базы данных
docker compose down -v
docker compose up -d
make migrate-docker
```




## Лицензия

Этот проект создан в демонстрационных целях как часть технического задания.