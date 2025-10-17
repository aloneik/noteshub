# CORS Configuration Guide

## Что такое CORS?

**CORS (Cross-Origin Resource Sharing)** — механизм безопасности браузера, который контролирует, какие веб-сайты могут обращаться к вашему API.

### Когда нужен CORS?

CORS требуется, когда фронтенд и бэкенд работают на разных:
- **Доменах**: `example.com` vs `api.example.com`
- **Портах**: `localhost:8000` vs `localhost:5173`
- **Протоколах**: `http://` vs `https://`

## Текущая конфигурация

### Development (по умолчанию)

CORS разрешен для локальных фронтендов:
```python
CORS_ORIGINS = [
    "http://localhost:3000",   # React (npm start)
    "http://localhost:5173",   # Vite (npm run dev)
    "http://localhost:5174",   # Vite alternative port
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]
```

### Production

Установите переменную окружения `CORS_ORIGINS`:

```bash
# .env файл или environment variables
CORS_ORIGINS=https://notehub.com,https://www.notehub.com,https://app.notehub.com
```

Или в Docker:
```yaml
environment:
  - CORS_ORIGINS=https://notehub.com,https://www.notehub.com
```

## Настройки CORS

### Текущие разрешения

| Настройка | Значение | Описание |
|-----------|----------|----------|
| `allow_origins` | См. выше | Список разрешенных источников |
| `allow_credentials` | `True` | Разрешить cookies и Authorization headers |
| `allow_methods` | `["*"]` | Все HTTP методы (GET, POST, PUT, DELETE, etc.) |
| `allow_headers` | `["*"]` | Все заголовки (Authorization, Content-Type, etc.) |

### Для production рекомендуется

Ограничить методы и заголовки:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept"],
)
```

## Тестирование CORS

### Из браузера (DevTools Console)

```javascript
// Проверка CORS с фронтенда
fetch('http://localhost:8000/health')
  .then(r => r.json())
  .then(data => console.log('✅ CORS работает!', data))
  .catch(err => console.error('❌ CORS ошибка:', err));
```

### С curl

```bash
# Проверка CORS headers
curl -H "Origin: http://localhost:5173" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: Authorization" \
     -X OPTIONS \
     -v http://localhost:8000/api/notes
```

Должны быть заголовки:
```
Access-Control-Allow-Origin: http://localhost:5173
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: *
Access-Control-Allow-Headers: *
```

## Безопасность

### ⚠️ Небезопасно

```python
# НЕ используйте в production!
allow_origins=["*"]  # Разрешает ВСЕ домены
```

### ✅ Безопасно

```python
# Явно указывайте разрешенные домены
allow_origins=[
    "https://notehub.com",
    "https://www.notehub.com",
]
```

## Troubleshooting

### Ошибка: "blocked by CORS policy"

**Причина**: Фронтенд не в списке разрешенных origins

**Решение**:
1. Проверьте, что фронтенд запущен на разрешенном порту
2. Добавьте URL фронтенда в `CORS_ORIGINS`
3. Перезапустите бэкенд

### Ошибка: "credentials mode is 'include'"

**Причина**: `allow_credentials=True` требует конкретные origins (не `*`)

**Решение**: Укажите точные домены вместо `*`

### Ошибка в production

**Проблема**: CORS работает локально, но не в production

**Решение**:
1. Убедитесь, что установлена переменная `CORS_ORIGINS`
2. Проверьте, что домены указаны с правильным протоколом (`https://`)
3. Проверьте логи: `docker compose logs backend`

## Примеры конфигурации

### Kubernetes

```yaml
env:
  - name: CORS_ORIGINS
    value: "https://notehub.com,https://www.notehub.com"
```

### Docker Compose

```yaml
services:
  backend:
    environment:
      - CORS_ORIGINS=https://notehub.com,https://www.notehub.com
```

### Railway / Heroku

```bash
# CLI
railway variables set CORS_ORIGINS="https://notehub.com,https://www.notehub.com"
heroku config:set CORS_ORIGINS="https://notehub.com,https://www.notehub.com"
```

## Дополнительные ресурсы

- [MDN CORS Documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [FastAPI CORS Middleware](https://fastapi.tiangolo.com/tutorial/cors/)
- [CORS Explained (web.dev)](https://web.dev/cross-origin-resource-sharing/)
