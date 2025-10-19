# Деплой NoteHub Frontend на Vercel

Пошаговая инструкция по развертыванию React + Vite frontend на Vercel.

## 📋 Предварительные требования

- GitHub аккаунт
- Vercel аккаунт (бесплатная регистрация через GitHub)
- Frontend код в GitHub репозитории
- Backend уже задеплоен на Render (URL известен)

## 🚀 Способ 1: Автоматический деплой через Vercel CLI (Рекомендуется)

### Шаг 1: Установите Vercel CLI

```bash
npm install -g vercel
```

### Шаг 2: Войдите в Vercel

```bash
cd web_frontend
vercel login
```

Откроется браузер для авторизации через GitHub.

### Шаг 3: Настройте проект

```bash
vercel
```

Ответьте на вопросы:
```
? Set up and deploy "web_frontend"? [Y/n] Y
? Which scope? [Ваш username]
? Link to existing project? [N]
? What's your project's name? notehub-frontend
? In which directory is your code located? ./
? Want to override the settings? [N]
```

### Шаг 4: Настройте переменные окружения

В процессе деплоя или после в Vercel Dashboard:

```bash
VITE_API_URL=https://notehub-backend.onrender.com
```

### Шаг 5: Deploy в production

```bash
vercel --prod
```

Получите URL:
```
https://notehub-frontend.vercel.app
```

---

## 🛠️ Способ 2: Деплой через Vercel Dashboard (Проще)

### Шаг 1: Войдите в Vercel

1. Перейдите на [vercel.com](https://vercel.com)
2. Нажмите **"Sign Up"** → **"Continue with GitHub"**
3. Авторизуйтесь через GitHub

### Шаг 2: Импортируйте проект

1. В Dashboard нажмите **"Add New..."** → **"Project"**
2. Выберите свой GitHub репозиторий: `aloneik/noteshub`
3. Нажмите **"Import"**

### Шаг 3: Настройте проект

На странице конфигурации заполните:

#### Framework Preset
- Автоматически определится: **Vite**

#### Root Directory
- Укажите: `web_frontend` (нажмите Edit)
- Выберите папку `web_frontend` из списка

#### Build Settings (автоматически заполнены)
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`

#### Environment Variables
Добавьте переменную:
```
Name: VITE_API_URL
Value: https://notehub-backend.onrender.com
```

**Важно**: Замените URL на ваш актуальный URL backend из Render!

### Шаг 4: Deploy

1. Нажмите **"Deploy"**
2. Дождитесь завершения (2-5 минут)
3. Получите URL вида: `https://notehub-frontend.vercel.app`

---

## ✅ Проверка работы

### 1. Откройте сайт
```
https://notehub-frontend.vercel.app
```

### 2. Проверьте страницы
- `/login` - Страница входа
- `/register` - Страница регистрации
- `/dashboard` - Дашборд (после входа)

### 3. Тестирование
1. Зарегистрируйте нового пользователя
2. Войдите в систему
3. Создайте заметку
4. Создайте план в заметке

---

## 🔧 Обновление CORS в Backend

**Критически важно!** После деплоя frontend обновите CORS в backend:

### В Render Dashboard:

1. Откройте ваш Web Service (backend)
2. Перейдите в **"Environment"**
3. Найдите переменную `CORS_ORIGINS`
4. Обновите значение:
```
CORS_ORIGINS=https://notehub-frontend.vercel.app,http://localhost:5173
```
5. Нажмите **"Save Changes"** (автоматически редеплоится)

**Важно**: 
- Используйте точный URL (с `https://`)
- Без слэша в конце
- Можно добавить несколько через запятую

---

## 🔄 Автоматический деплой

После первого деплоя Vercel автоматически:
- ✅ Деплоит при каждом push в `master`
- ✅ Создает preview для Pull Requests
- ✅ Показывает статус деплоя в GitHub

### Отключить auto-deploy:
В Vercel Dashboard → Settings → Git → Auto Deploy

---

## ⚙️ Дополнительные настройки

### Custom Domain (опционально)

1. В Vercel Dashboard → Settings → Domains
2. Добавьте свой домен
3. Настройте DNS записи
4. Обновите CORS_ORIGINS в backend

### Environment Variables

Добавить дополнительные переменные:
1. Settings → Environment Variables
2. Add New
3. Введите Name и Value
4. Выберите окружение (Production/Preview/Development)

### Build Settings

Изменить команды сборки:
1. Settings → General → Build & Development Settings
2. Измените команды
3. Save

---

## 🐛 Troubleshooting

### Проблема: Build fails

**Решение**: Проверьте логи сборки
```
Deployments → Latest Deployment → Building → View Function Logs
```

Частые причины:
- Отсутствие зависимостей в `package.json`
- Ошибки TypeScript
- Неправильный Root Directory

### Проблема: CORS errors

**Решение**: 
1. Проверьте CORS_ORIGINS в backend
2. Убедитесь, что URL точный (с https://)
3. Проверьте, что backend редеплоился после изменений

### Проблема: API calls fail

**Решение**: Проверьте `VITE_API_URL`
1. Settings → Environment Variables
2. Убедитесь, что URL правильный
3. Redeploy после изменений

### Проблема: 404 on refresh

**Решение**: Vercel автоматически обрабатывает SPA роутинг, но если проблема есть:

Создайте `vercel.json` в корне `web_frontend/`:
```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### Проблема: Env variables не работают

**Причина**: Vite требует префикс `VITE_`

**Решение**: 
- ✅ `VITE_API_URL` - работает
- ❌ `API_URL` - не работает

---

## 📊 Мониторинг и аналитика

### Vercel Analytics (опционально)

1. Settings → Analytics → Enable
2. Бесплатно до 100k событий/месяц
3. Просмотр в Dashboard → Analytics

### Speed Insights

1. Settings → Speed Insights → Enable
2. Мониторинг производительности
3. Core Web Vitals

---

## 💰 Ценообразование Vercel

### Free Tier (Hobby)
- ✅ Неограниченные деплои
- ✅ 100GB bandwidth/месяц
- ✅ Автоматический SSL
- ✅ Preview deployments
- ✅ Serverless Functions (100GB-Hrs)
- ✅ Один член команды

### Ограничения Free Tier
- 100GB bandwidth (достаточно для ~1M посетителей/месяц)
- Commercial use разрешено
- No custom redirects limit

### Pro Tier ($20/месяц)
- 1TB bandwidth
- Больше build minutes
- Команды
- Приоритетная поддержка

Для нашего проекта **Free tier более чем достаточно!**

---

## 🔐 Security Best Practices

### Environment Variables
- ✅ Используйте `VITE_API_URL` для публичных данных
- ❌ НЕ храните секреты в frontend
- ✅ Секреты только в backend

### HTTPS
- ✅ Автоматически включен Vercel
- ✅ Автоматическое обновление сертификатов

### Headers
Vercel автоматически устанавливает:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`

---

## 📝 Конфигурация проекта

### Создайте `vercel.json` (опционально)

В `web_frontend/vercel.json`:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        }
      ]
    }
  ]
}
```

---

## 🚀 Quick Deploy Command

Одна команда для деплоя:

```bash
cd web_frontend
vercel --prod
```

---

## ✅ Deployment Checklist

### Pre-Deploy
- [ ] Frontend код в GitHub
- [ ] Backend задеплоен на Render
- [ ] Backend URL известен
- [ ] Все тесты проходят локально

### Deploy
- [ ] Vercel аккаунт создан
- [ ] Проект импортирован
- [ ] Root Directory установлен: `web_frontend`
- [ ] VITE_API_URL настроен
- [ ] Deploy завершен успешно

### Post-Deploy
- [ ] Сайт открывается
- [ ] CORS обновлен в backend
- [ ] Регистрация работает
- [ ] Логин работает
- [ ] CRUD операции работают
- [ ] URL сохранен

---

## 🔗 Полезные ссылки

- **Vercel Dashboard**: https://vercel.com/dashboard
- **Documentation**: https://vercel.com/docs
- **Vite Guide**: https://vitejs.dev/guide/
- **React Docs**: https://react.dev/

---

## 📞 Следующие шаги

1. ✅ **Deploy frontend на Vercel** (вы здесь)
2. 🔄 **Обновите CORS** в backend
3. ✅ **Протестируйте** production version
4. 📊 **Настройте мониторинг** (опционально)
5. 🌐 **Custom domain** (опционально)
6. 🚀 **Готово!**

---

## 🎉 Готово!

После деплоя у вас будет:
- 🌐 Frontend: `https://notehub-frontend.vercel.app`
- 🔧 Backend: `https://notehub-backend.onrender.com`
- 📚 API Docs: `https://notehub-backend.onrender.com/docs`

**Total deployment time**: ~5 минут
**Cost**: $0 (free tier)
**Maintenance**: Auto-deploy on git push

---

**Успешного деплоя! 🚀**
