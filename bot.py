import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
import os

# Данные для пользовательской сессии (ваш аккаунт)
API_ID = 36279507
API_HASH = "56fcccec931c77d873a70467de073e7a"
SESSION_STRING = "AgIplNMAR9MockxirApSfeRG6bOVLeiUAlvjiJZGaNLyJ4nbvj0RCknIjnl5FPzWecdNrRv8S6xH9ngUce1nefwNHLueR1LkbWQAicX6W1WhbI137oxCx3YUpUd4_2MLrH2cd3flz1bhqRWWgGWXDcE-srVRX10RXfnwQpV-lgrx7hO-hy9hNg62lPsAeKaYaCoNYzd3fXSUD06CT0VKFfvVmajliCbJ_bgo6kpe64QDw0Ql8J41Aq9uQjfVw5K1-GQmqPCEgOmGRnFZ9fblMxzYdDy1cRtQbhB0U-8J6qVTsi1m4BEnsuNhhvuZKfP3-dK7LOt9xxguhpxC1k9TUoifQiBB8AAAAAArln85AA"

# Токен бота (будет взят из переменной окружения BOT_TOKEN, которую мы зададим на Bothost)
BOT_TOKEN = os.getenv("BOT_TOKEN")  # на Bothost мы добавим переменную BOT_TOKEN с вашим токеном

# Создаём двух клиентов:
# user_client – от вашего имени (для скачивания)
# bot_client – от имени бота (для ответов)
user_client = Client(
    "user_session",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
    in_memory=True
)

bot_client = Client(
    "bot_session",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True
)

# Обработчик команды /start (бот отвечает)
@bot_client.on_message(filters.private & filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply("Привет! Отправь мне ссылку на видео из закрытого канала, и я скачаю его для тебя.")

# Обработчик текстовых сообщений (бот принимает ссылку)
@bot_client.on_message(filters.private & filters.text)
async def handle_link(client: Client, message: Message):
    url = message.text.strip()
    if not url.startswith("https://t.me/"):
        await message.reply("Это не похоже на ссылку Telegram. Отправь ссылку на сообщение с видео.")
        return

    # Сообщаем, что начали скачивание
    await message.reply("Скачиваю видео, подожди...")

    try:
        # Используем user_client для получения сообщения по ссылке (от вашего имени)
        msg = await user_client.get_messages(url)
        if msg.video:
            file_path = await msg.download()
            # Отправляем видео через бота
            await message.reply_video(video=file_path, caption="Вот твоё видео!")
        else:
            await message.reply("В этом сообщении нет видео.")
    except Exception as e:
        await message.reply(f"Ошибка: {e}")

async def main():
    # Запускаем обоих клиентов
    await user_client.start()
    await bot_client.start()
    print("Бот запущен и готов к работе!")
    # Бесконечно ждём, пока клиенты работают
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
