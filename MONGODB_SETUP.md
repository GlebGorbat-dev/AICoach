# Установка MongoDB на macOS

## Шаг 1: Обновление Command Line Tools

Перед установкой MongoDB необходимо обновить Command Line Tools:

```bash
# Удалите старые инструменты
sudo rm -rf /Library/Developer/CommandLineTools

# Установите новые инструменты
sudo xcode-select --install
```

Или обновите их через **Системные настройки → Обновление ПО**.

## Шаг 2: Установка MongoDB через Homebrew

```bash
# Добавьте официальный репозиторий MongoDB
brew tap mongodb/brew

# Установите MongoDB Community Edition (версия 7.0 или 8.0)
brew install mongodb-community@7.0
# или
brew install mongodb-community@8.0
```

## Шаг 3: Запуск MongoDB

```bash
# Запустите MongoDB как службу (будет запускаться автоматически при загрузке системы)
brew services start mongodb-community@7.0
# или для версии 8.0
brew services start mongodb-community@8.0

# Или запустите MongoDB вручную (без автозапуска)
mongod --config /opt/homebrew/etc/mongod.conf
```

## Шаг 4: Проверка установки

```bash
# Проверьте статус службы
brew services list | grep mongodb

# Подключитесь к MongoDB через mongosh
mongosh
```

## Шаг 5: Настройка переменных окружения

Создайте файл `.env` в корне проекта со следующим содержимым:

```env
# MongoDB Connection String
# Для локальной установки (обратите внимание: используется MONGO_DB_URL, а не MONGODB_URL):
MONGO_DB_URL=mongodb://localhost:27017/

# Или с указанием базы данных:
MONGO_DB_URL=mongodb://localhost:27017/Coach_deploy

# Если нужна аутентификация (опционально):
# MONGO_DB_URL=mongodb://username:password@localhost:27017/Coach_deploy?authSource=admin

# Идентификатор администратора
# Это ID пользователя-администратора в вашей системе
# Может быть UUID или любая строка, которая идентифицирует администратора
# Примеры:
ADMIN_ID=admin-12345
# или
# ADMIN_ID=550e8400-e29b-41d4-a716-446655440000

# ID векторного хранилища (Vector Store ID)
# ⚠️ ВАЖНО: Это должен быть РЕАЛЬНЫЙ ID векторного хранилища OpenAI, который начинается с 'vs_'
# Это НЕ имя коллекции MongoDB, а ID, который вы получаете при создании векторного хранилища в OpenAI
# 
# Как получить VS_ID:
# 1. Создайте векторное хранилище через OpenAI API или веб-интерфейс
# 2. Скопируйте ID хранилища (он будет выглядеть как: vs_xxxxxxxxxxxxx)
# 3. Укажите его здесь
#
# Пример:
# VS_ID=vs_abc123def456ghi789
#
# Если у вас еще нет векторного хранилища, создайте его через OpenAI API:
# https://platform.openai.com/docs/api-reference/vector-stores

# OpenAI API Key (обязательно для работы с LLM)
OPENAI_API_KEY=your-openai-api-key-here

# Секретный ключ для JWT токенов (обязательно для безопасности)
SECRET_KEY=your-secret-key-here-minimum-32-characters-long

# Конфигурация FastAPI (опционально, по умолчанию 'development')
FASTAPI_CONFIG=development
```

### Пояснения к переменным:

- **MONGO_DB_URL**: Строка подключения к MongoDB. База данных будет называться `Coach_deploy` (как указано в config.py)
- **ADMIN_ID**: Идентификатор администратора. Это может быть:
  - UUID пользователя из вашей базы данных
  - Произвольная строка, которая идентифицирует администратора
  - Пример: `admin-12345` или `550e8400-e29b-41d4-a716-446655440000`
- **VS_ID**: **РЕАЛЬНЫЙ ID векторного хранилища OpenAI** (начинается с `vs_`). Это НЕ имя коллекции MongoDB!
  - Это ID, который вы получаете при создании векторного хранилища в OpenAI
  - Пример: `vs_abc123def456ghi789`
  - Если у вас нет векторного хранилища, создайте его через OpenAI API или веб-интерфейс
  - Документация: https://platform.openai.com/docs/api-reference/vector-stores
- **OPENAI_API_KEY**: Ключ API от OpenAI (получите на https://platform.openai.com/api-keys)
- **SECRET_KEY**: Секретный ключ для подписи JWT токенов (минимум 32 символа, используйте случайную строку)

## Шаг 6: Настройка конфигурации MongoDB (опционально)

Конфигурационный файл находится по адресу:
- Apple Silicon (M1/M2/M3): `/opt/homebrew/etc/mongod.conf`
- Intel: `/usr/local/etc/mongod.conf`

Вы можете отредактировать его для изменения порта, пути к данным и других настроек.

## Полезные команды

```bash
# Остановить MongoDB
brew services stop mongodb-community@7.0

# Перезапустить MongoDB
brew services restart mongodb-community@7.0

# Просмотр логов
tail -f /opt/homebrew/var/log/mongodb/mongo.log

# Удаление MongoDB (если нужно)
brew services stop mongodb-community@7.0
brew uninstall mongodb-community@7.0
```

## Совместимость

Ваш проект использует:
- `pymongo==4.13.2` - поддерживает MongoDB 4.0+
- `motor==3.7.1` - асинхронный драйвер для MongoDB

MongoDB 7.0 и 8.0 полностью совместимы с этими версиями драйверов.

