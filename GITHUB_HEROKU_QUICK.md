# ⚡ БЫСТРЫЙ ГАЙД: GITHUB + HEROKU (10 МИНУТ)

**Для тех, кто спешит**

---

## 📦 ВСЕ ФАЙЛЫ УЖЕ ГОТОВЫ

Я создал для тебя:

```
✓ requirements.txt        (зависимости)
✓ Procfile                (для Heroku)
✓ runtime.txt             (Python 3.11)
✓ .gitignore              (игнорируемые файлы)
✓ .env.example            (пример переменных)
✓ legion_chain_pro_bot_heroku.py (бот для облака)
```

**Просто скопируй их в папку проекта!**

---

## 🚀 БЫСТРАЯ ИНСТРУКЦИЯ

### Шаг 1: Создай репозиторий на GitHub (2 мин)

```
1. Перейди: https://github.com/new
2. Имя: legion-chain-pro
3. Public ✓
4. Create repository
```

### Шаг 2: Подготовь папку (1 мин)

```
1. Создай папку: legion-chain-pro
2. Положи туда все файлы (те, что я создал)
3. Скопируй .env.example → .env
4. Открой .env и вставь токен/ID
```

### Шаг 3: Git push (2 мин)

```bash
cd Desktop/legion-chain-pro
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/legion-chain-pro.git
git push -u origin main
```

### Шаг 4: Heroku Deploy (3 мин)

```bash
heroku login
heroku create legion-chain-pro
heroku config:set TELEGRAM_BOT_TOKEN=ВАШ_ТОКЕН
heroku config:set ADMIN_ID=ВАШ_ID
git push heroku main
```

### Шаг 5: Проверка (2 мин)

```bash
heroku logs --tail
```

Ищи: "Listening for messages..." ✅ ГОТОВО!

---

## 📋 НУЖНО УСТАНОВИТЬ

1. **Git**: https://git-scm.com/download
2. **Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli

---

## 🎯 ФАЙЛЫ ДЛЯ КОПИРОВАНИЯ

Скопируй эти файлы в папку `legion-chain-pro`:

```
requirements.txt
Procfile
runtime.txt
.gitignore
.env.example
legion_chain_pro_bot_heroku.py
README.md (создай самостоятельно)
```

---

## 💻 КОМАНДЫ

### GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin [ссылка]
git push -u origin main
```

### Heroku

```bash
heroku login
heroku create [имя]
heroku config:set KEY=VALUE
git push heroku main
heroku logs --tail
```

---

## ✅ ГОТОВО!

Бот теперь работает на облаке и **работает 24/7** без остановки!

Версия: Quick Guide | 2025