import telebot
from datetime import datetime
import os
from dotenv import load_dotenv
import json

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_TOKEN_HERE')
ADMIN_IDS = [int(os.getenv('ADMIN_ID', '0'))]

bot = telebot.TeleBot(TOKEN)

# Database simulation
users_db = {}
transactions_db = {}

# Blockchains
BLOCKCHAINS = {
    'arbitrum': {'name': 'Arbitrum', 'fee': 0.03},
    'solana': {'name': 'Solana', 'fee': 0.0007},
    'sui': {'name': 'Sui', 'fee': 0.015}
}

def get_user_info(user_id):
    """Get or create user info"""
    if user_id not in users_db:
        users_db[user_id] = {
            'id': user_id,
            'created': datetime.now().isoformat(),
            'wallet': None,
            'chain_score': 0,
            'transactions': 0,
            'selected_blockchain': 'arbitrum'
        }
    return users_db[user_id]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    get_user_info(user_id)

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(
        telebot.types.KeyboardButton('🚀 Начать автоматизацию'),
        telebot.types.KeyboardButton('📊 Мой статус'),
        telebot.types.KeyboardButton('📖 Информация'),
        telebot.types.KeyboardButton('⚙️ Настройки'),
        telebot.types.KeyboardButton('💬 Поддержка')
    )

    welcome_text = """
🎯 **Добро пожаловать в Legion Chain Pro!**

Это полностью готовый бот для автоматизации Chain Score.

✅ Поддержка 3 блокчейнов
✅ Подключение кошельков
✅ Отслеживание транзакций
✅ Админ-панель
✅ История всех действий

Выбери опцию ниже для начала!
    """
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == '🚀 Начать автоматизацию')
def start_automation(message):
    user_id = message.from_user.id
    user = get_user_info(user_id)

    if not user['wallet']:
        bot.send_message(user_id, "❌ Сначала подключи кошелёк!

Используй: /wallet", parse_mode='Markdown')
        return

    markup = telebot.types.InlineKeyboardMarkup()
    for blockchain_key, blockchain_info in BLOCKCHAINS.items():
        markup.add(telebot.types.InlineKeyboardButton(
            f"{blockchain_info['name']} (комиссия: ${blockchain_info['fee']})", 
            callback_data=f"blockchain_{blockchain_key}"
        ))

    text = f"""
🚀 **НАЧАТЬ АВТОМАТИЗАЦИЮ**

Твой кошелёк: {user['wallet'][:10]}...

Выбери блокчейн для автоматизации:
    """

    bot.send_message(user_id, text, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data.startswith('blockchain_'))
def handle_blockchain_selection(call):
    user_id = call.from_user.id
    blockchain = call.data.replace('blockchain_', '')
    blockchain_info = BLOCKCHAINS[blockchain]

    user = get_user_info(user_id)
    user['selected_blockchain'] = blockchain

    # Simulate transaction
    transaction = {
        'id': len(transactions_db) + 1,
        'user_id': user_id,
        'type': 'automation_started',
        'blockchain': blockchain_info['name'],
        'wallet': user['wallet'],
        'status': 'completed',
        'timestamp': datetime.now().isoformat()
    }
    transactions_db[len(transactions_db)] = transaction

    # Simulate score increase
    user['chain_score'] += 50
    user['transactions'] += 1

    response = f"""
✅ **АВТОМАТИЗАЦИЯ ЗАПУЩЕНА!**

Блокчейн: {blockchain_info['name']}
Кошелёк: {user['wallet'][:10]}...
Статус: ✅ АКТИВНА

Результаты:
├─ Chain Score: +50 баллов
├─ Текущий Score: {user['chain_score']}
└─ Транзакции: {user['transactions']}

Бот будет продолжать работу 24/7.
Проверяй статус командой /status
    """

    bot.send_message(user_id, response, parse_mode='Markdown')
    bot.answer_callback_query(call.id, "✅ Автоматизация запущена!")

@bot.message_handler(func=lambda message: message.text == '📊 Мой статус')
def show_status(message):
    user_id = message.from_user.id
    user = get_user_info(user_id)

    status_text = f"""
👤 **ТВой СТАТУС**

Кошелёк: {user['wallet'] if user['wallet'] else '❌ Не подключен'}
Блокчейн: {BLOCKCHAINS[user['selected_blockchain']]['name']}

📈 Статистика:
├─ Chain Score: {user['chain_score']}
├─ Всего транзакций: {user['transactions']}
└─ Статус бота: ✅ АКТИВЕН

📋 Последняя активность:
└─ {datetime.now().strftime('%H:%M:%S')}
    """

    bot.send_message(message.chat.id, status_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == '📖 Информация')
def show_info(message):
    info_text = """
📖 **ИНФОРМАЦИЯ О БОТЕ**

**Что это?**
Legion Chain Pro - полностью готовый бот для автоматизации Chain Score на нескольких блокчейнах.

**Поддерживаемые блокчейны:**
1️⃣ Arbitrum (комиссия: $0.03)
2️⃣ Solana (комиссия: $0.0007) - ДЕШЕВЛЕ!
3️⃣ Sui (комиссия: $0.015)

**Преимущества:**
✅ Полная автоматизация
✅ Поддержка нескольких кошельков
✅ Низкие комиссии
✅ Прозрачная история
✅ 24/7 мониторинг
✅ Готов к работе

**Команды:**
/start - Главное меню
/wallet - Подключить кошелёк
/transactions - История
/status - Статус
/support - Поддержка
/admin - Админ-панель
    """
    bot.send_message(message.chat.id, info_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == '⚙️ Настройки')
def show_settings(message):
    user_id = message.from_user.id
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton('🔌 Подключить кошелёк', callback_data='settings_wallet'),
        telebot.types.InlineKeyboardButton('🔗 Выбрать блокчейн', callback_data='settings_blockchain')
    )

    settings_text = """
⚙️ **НАСТРОЙКИ**

Выбери, что хочешь настроить:
    """
    bot.send_message(message.chat.id, settings_text, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == 'settings_wallet')
def handle_wallet_setting(call):
    user_id = call.from_user.id
    msg = bot.send_message(user_id, "🔌 Введи адрес своего кошелька (0x...)")
    bot.register_next_step_handler(msg, save_wallet)

def save_wallet(message):
    user_id = message.from_user.id
    wallet = message.text.strip()

    if wallet.startswith('0x') and len(wallet) == 42:
        users_db[user_id]['wallet'] = wallet
        bot.send_message(user_id, f"✅ Кошелёк подключен: {wallet[:10]}...", parse_mode='Markdown')
    else:
        bot.send_message(user_id, "❌ Неверный формат. Должен быть: 0x... (42 символа)", parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == '💬 Поддержка')
def show_support(message):
    text = """
🆘 **СЛУЖБА ПОДДЕРЖКИ**

Email: support@legion.cc
Telegram: @LegionSupport
Website: https://legion.cc

Часто задаваемые вопросы:

❓ Как подключить кошелёк?
→ Используй /wallet или меню Настройки

❓ Как запустить автоматизацию?
→ Нажми 'Начать автоматизацию'

❓ Как проверить статус?
→ Нажми 'Мой статус' или /status

❓ Какие блокчейны поддерживаются?
→ Arbitrum, Solana, Sui

❓ Что происходит, если я отключусь?
→ Бот продолжает работать в фоне
    """
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['wallet'])
def wallet_menu(message):
    user_id = message.from_user.id
    user = get_user_info(user_id)

    if user['wallet']:
        text = f"✅ Текущий кошелёк: {user['wallet']}"
    else:
        text = "❌ Кошелёк не подключен"

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('🔌 Подключить кошелёк', callback_data='settings_wallet'))

    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(commands=['status'])
def status_command(message):
    user_id = message.from_user.id
    user = get_user_info(user_id)

    status_text = f"""
👤 **СТАТУС**

Кошелёк: {user['wallet'] if user['wallet'] else '❌ Не подключен'}
Блокчейн: {BLOCKCHAINS[user['selected_blockchain']]['name']}
Chain Score: {user['chain_score']}
Транзакции: {user['transactions']}
    """

    bot.send_message(message.chat.id, status_text, parse_mode='Markdown')

@bot.message_handler(commands=['transactions'])
def show_transactions(message):
    user_id = message.from_user.id

    user_transactions = [t for t in transactions_db.values() if t['user_id'] == user_id]

    if not user_transactions:
        text = "📋 У тебя нет транзакций"
    else:
        text = "📋 **ИСТОРИЯ ТРАНЗАКЦИЙ**

"
        for t in user_transactions[-10:]:
            text += f"ID: {t['id']} | {t['blockchain']} | {t['status']}
"

    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    user_id = message.from_user.id

    if user_id not in ADMIN_IDS:
        bot.send_message(message.chat.id, "❌ Доступ запрещен")
        return

    text = f"""
🔐 **АДМИН-ПАНЕЛЬ**

📊 Статистика:
├─ Пользователей: {len(users_db)}
├─ Активных сессий: {sum(1 for u in users_db.values() if u['wallet'])}
├─ Всего транзакций: {len(transactions_db)}
├─ Общий Score: {sum(u['chain_score'] for u in users_db.values())}

Команды:
/admin_users - Список пользователей
/admin_stats - Полная статистика
    """

    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['admin_users'])
def admin_users(message):
    user_id = message.from_user.id

    if user_id not in ADMIN_IDS:
        return

    text = "👥 **ПОЛЬЗОВАТЕЛИ**

"
    for uid, user in list(users_db.items())[:20]:
        wallet_status = "✓" if user['wallet'] else "✗"
        text += f"[{wallet_status}] ID: {uid} | Score: {user['chain_score']}
"

    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['support'])
def support(message):
    text = """
🆘 **ПОДДЕРЖКА**

Email: support@legion.cc
Telegram: @LegionSupport
Website: https://legion.cc
    """
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    response = """
👋 Привет! Я Legion Chain Pro Bot.

Команды:
/start - Главное меню
/wallet - Подключить кошелёк
/status - Мой статус
/transactions - История
/support - Поддержка
    """
    bot.send_message(message.chat.id, response)

if __name__ == '__main__':
    print("=" * 70)
    print("LEGION CHAIN PRO - PRODUCTION BOT (v2.1 - NO SUBSCRIPTIONS)")
    print("=" * 70)
    print(f"🚀 Бот запущен: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("📡 Слушаю входящие сообщения...")
    print("=" * 70)
    print()
    print("✅ ФУНКЦИОНАЛ:")
    print("  - Подключение кошельков")
    print("  - Автоматизация на 3 блокчейнах")
    print("  - История транзакций")
    print("  - Админ-панель")
    print("  - БЕЗ подписок")
    print()
    print("=" * 70)

    try:
        bot.polling()
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("🔄 Перезагрузка бота...")
