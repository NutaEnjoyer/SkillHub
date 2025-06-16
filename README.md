# 🐍 SkillHub is a Django REST Framework-based educational platform for instructors and students

## 📦 Стек
- Django REST Framework
- PostgreSQL
- Redis 
- Celery
- Docker + docker-compose

---

```
             /^\/^\
           _|__|  O|
  \/     /~     \_/ \
   \____|__________/  \
          \_______      \
                  `\     \                 \
                    |     |                  \
                   /      /                    \
                  /     /                       \\
                /      /                         \ \
               /     /                            \  \
             /     /             _----_            \   \
            /     /           _-~      ~-_         |   |
           (      (        _-~    _--_    ~-_     _/   |
            \      ~-____-~    _-~    ~-_    ~-_-~    /
              ~-_           _-~          ~-_       _-~
                 ~--______-~                ~-___-~
```

---

## 🚀 Быстрый старт

### 1. Клонируй репозиторий

```bash
git clone https://github.com/NutaEnjoyer/SkillHub.git

cd SkillHub
```

### 2. Создайте ./env/.env файл

Создай файл .env в папке env по аналогу с env.template/.env.template:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your.email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your.email@gmail.com

DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

MONGO_URI=mongo
MONGO_DB_NAME=mongo_db_name
```

### 3. Соберите и запустите контейнеры

```bash
docker-compose up --build
```

#### Приложение будет доступно по адресу: http://localhost:8000/

## License

[MIT licensed](https://github.com/nestjs/nest/blob/master/LICENSE).
