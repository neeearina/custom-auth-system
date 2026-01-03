# Custom Authentication & Authorization System

Backend-приложение на Django REST Framework с кастомной системой аутентификации и авторизации. Проект реализует собственную модель разграничения доступа, не полностью основанную на стандартных механизмах Django (Groups/Permissions).

## Описание проекта

Этот сервис представляет собой REST API для управления пользователями и контроля доступа к ресурсам. Основная особенность — кастомная система авторизации, которая позволяет гибко настраивать права доступа через роли, ресурсы и действия.

### Что решает проект

- **Аутентификация пользователей**: регистрация, вход, выход, управление профилем
- **Кастомная авторизация**: гибкая система прав доступа на основе ролей
- **Управление доступом**: административный API для настройки прав
- **Тестирование доступа**: mock endpoints для проверки работы системы

### Кастомная авторизация

Вместо стандартных Django Groups/Permissions используется собственная модель:
- **Role** (Роль) — определяет группу пользователей (admin, user и т.д.)
- **Resource** (Ресурс) — объект, к которому нужен доступ (projects, reports и т.д.)
- **Action** (Действие) — операция, которую можно выполнить (read, create, update, delete)
- **Permission** (Право) — правило: роль может выполнить действие над ресурсом

## Схема системы доступа

### Роли (Roles)

Роль определяет группу пользователей с определенными правами:

- **admin** — администратор с полным доступом ко всем ресурсам
- **user** — обычный пользователь с ограниченными правами

### Ресурсы (Resources)

Ресурс — это объект или группа объектов, к которым нужен доступ:

- **projects** — проекты
- **reports** — отчеты
- **access** — управление системой доступа (только для админов)

### Действия (Actions)

Действие — это операция, которую можно выполнить над ресурсом:

- **read** — просмотр/чтение
- **create** — создание
- **update** — обновление
- **delete** — удаление
- **admin** — административные действия

### Правила доступа (Permissions)

Правило связывает роль, ресурс и действие. Например:

- `admin` может `read` `projects` 
- `admin` может `create` `projects` 
- `user` может `read` `projects` 

### Проверка доступа

1. Пользователь должен быть аутентифицирован (иметь валидный токен)
2. Система проверяет роли пользователя
3. Для каждой роли проверяются права на ресурс и действие
4. Если право найдено — доступ разрешен (200 OK)
5. Если пользователь не аутентифицирован — 401 Unauthorized
6. Если пользователь аутентифицирован, но нет прав — 403 Forbidden

## Запуск проекта

### Локально

1. **Клонируйте репозиторий**:
```bash
git clone <repository-url>
cd custom-auth-system
```

2. **Создайте виртуальное окружение**:
```bash
python -m venv venv
source venv/bin/activate 
```

3. **Установите зависимости**:
```bash
pip install -r requirements.txt
```

4. **Создайте файл .env и отредактируйте его**:
```bash
cp .env-example .env
```

5. **Создайте миграции**:
```bash
python manage.py makemigrations
```

6. **Примените миграции** (создаст таблицы в базе данных):
```bash
python manage.py migrate
```

**Важно**: Миграции должны быть применены перед загрузкой фикстур, иначе возникнет ошибка `no such table`.

7. **Загрузите тестовые данные**:
```bash
python manage.py loaddata access/fixtures/initial_data.json
```

8. **Создайте суперпользователя** (опционально):
```bash
python manage.py createsuperuser
```

9. **Запустите сервер**:
```bash
python manage.py runserver
```

Сервер будет доступен по адресу: http://localhost:8000

### Через Docker

1. **Соберите образ**:
```bash
docker build -t auth-app .
```

2. **Запустите контейнер**:
```bash
docker run -p 8000:8000 --env-file .env auth-app
```

Или используйте переменные окружения напрямую:
```bash
docker run -p 8000:8000 \
  -e SECRET_KEY=your-secret-key \
  -e DEBUG=True \
  -e ALLOWED_HOSTS=localhost,127.0.0.1 \
  auth-app
```

## Примеры API-запросов

### Регистрация

```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
  }'
```

**Ответ**:
```json
{
  "message": "User registered successfully.",
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "date_joined": "2024-01-15T10:00:00Z",
    "last_login": null
  }
}
```

### Login

```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

**Ответ**:
```json
{
  "message": "Login successful.",
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "date_joined": "2024-01-15T10:00:00Z",
    "last_login": "2024-01-15T10:30:00Z"
  }
}
```

### Запрос к защищенному ресурсу (с токеном)

```bash
curl -X GET http://localhost:8000/api/mock/projects/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

**Ответ (если есть права)**:
```json
{
  "message": "Access granted to projects",
  "data": [
    {
      "id": 1,
      "name": "Project Alpha",
      "description": "First project",
      "status": "active",
      "created_at": "2024-01-15T10:00:00Z"
    }
  ],
  "count": 3
}
```

### Пример ошибки 401 (не аутентифицирован)

```bash
curl -X GET http://localhost:8000/api/mock/projects/
```

**Ответ**:
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Пример ошибки 403 (нет прав)

Если пользователь не имеет права на доступ к ресурсу:

**Ответ**:
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### Обновление профиля

```bash
curl -X PATCH http://localhost:8000/api/users/profile/update/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Updated Doe"
  }'
```

### Logout

```bash
curl -X POST http://localhost:8000/api/users/logout/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

### Удаление пользователя (soft delete)

```bash
curl -X DELETE http://localhost:8000/api/users/delete/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```
## Особенности реализации

### Soft Delete

При удалении пользователя:
- Токен удаляется (logout)
- Поле `is_active` устанавливается в `False`
- Пользователь не может войти снова
- Запись в БД сохраняется

### Кастомная проверка прав

Используется класс `HasResourcePermission`, который:
1. Проверяет аутентификацию пользователя
2. Получает роли пользователя из таблицы `UserRole`
3. Проверяет наличие права через связь `Role → Permission → Resource + Action`
4. Возвращает `True` если право найдено, иначе `False`

### Permission Classes

- `IsAuthenticated` — стандартная проверка аутентификации DRF
- `HasResourcePermission` — кастомная проверка прав доступа
- `IsAdminPermission` — проверка наличия роли admin для административных операций

### Middleware

Используются стандартные middleware Django:
- `AuthenticationMiddleware` — для работы с токенами
- `SessionMiddleware` — для сессий (опционально)

## Административный API

Все административные endpoints требуют роль `admin` и права `access:admin`.

### Получить список ролей

```bash
curl -X GET http://localhost:8000/api/access/roles/ \
  -H "Authorization: Token <admin-token>"
```

### Создать правило доступа

```bash
curl -X POST http://localhost:8000/api/access/permissions/ \
  -H "Authorization: Token <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "role_id": 2,
    "resource_id": 1,
    "action_id": 1
  }'
```

### Назначить роль пользователю

```bash
curl -X POST http://localhost:8000/api/access/user-roles/ \
  -H "Authorization: Token <admin-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "role_id": 2
  }'
```

### Получить обзор системы доступа

```bash
curl -X GET http://localhost:8000/api/access/overview/ \
  -H "Authorization: Token <admin-token>"
```
## Безопасность

- Пароли хранятся в хешированном виде (Django default)
- Токены используются для аутентификации
- Soft delete предотвращает потерю данных
- Проверка прав на уровне API endpoints