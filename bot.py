import sys
import asyncio
import os

print("=== STARTING BOT ===", file=sys.stderr)
sys.stderr.flush()

try:
    from pyrogram import Client, filters
    from pyrogram.types import Message
    from pyrogram.errors import RPCError, Unauthorized, FloodWait
    print("✅ Pyrogram imported", file=sys.stderr)
except ImportError as e:
    print(f"❌ Import error: {e}", file=sys.stderr)
    sys.exit(1)

# Данные для пользовательской сессии
API_ID = 36279507
API_HASH = "56fcccec931c77d873a70467de073e7a"
SESSION_STRING = "AgIplNMAR9MockxirApSfeRG6bOVLeiUAlvjiJZGaNLyJ4nbvj0RCknIjnl5FPzWecdNrRv8S6xH9ngUce1nefwNHLueR1LkbWQAicX6W1WhbI137oxCx3YUpUd4_2MLrH2cd3flz1bhqRWWgGWXDcE-srVRX10RXfnwQpV-lgrx7hO-hy9hNg62lPsAeKaYaCoNYzd3fXSUD06CT0VKFfvVmajliCbJ_bgo6kpe64QDw0Ql8J41Aq9uQjfVw5K1-GQmqPCEgOmGRnFZ9fblMxzYdDy1cRtQbhB0U-8J6qVTsi1m4BEnsuNhhvuZKfP3-dK7LOt9xxguhpxC1k9TUoifQiBB8AAAAAArln85AA"  # ЗАМЕНИТЕ НА ВАШУ ПОЛНУЮ СТРОКУ!

# Токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    print("❌ BOT_TOKEN not set in environment variables!", file=sys.stderr)
    sys.exit(1)
else:
    print("✅ BOT_TOKEN found", file=sys.stderr)

print("Creating user client...", file=sys.stderr)
user_client = Client(
    "user_session",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING,
    in_memory=True
)

print("Creating bot client...", file=sys.stderr)
bot_client = Client(
    "bot_session",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True
)

@bot_client.on_message(filters.private & filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply("Привет! Отправь мне ссылку на видео из закрытого канала, и я скачаю его для тебя.")
    print(f"Received /start from {message.from_user.id}", file=sys.stderr)

@bot_client.on_message(filters.private & filters.text)
async def handle_link(client: Client, message: Message):
    url = message.text.strip()
    print(f"Received link: {url}", file=sys.stderr)
    if not url.startswith("https://t.me/"):
        await message.reply("Это не похоже на ссылку Telegram. Отправь ссылку на сообщение с видео.")
        return

    await message.reply("Скачиваю видео, подожди...")

    try:
        msg = await user_client.get_messages(url)
        if msg.video:
            file_path = await msg.download()
            await message.reply_video(video=file_path, caption="Вот твоё видео!")
            print(f"Video downloaded and sent: {file_path}", file=sys.stderr)
        else:
            await message.reply("В этом сообщении нет видео.")
    except Exception as e:
        await message.reply(f"Ошибка: {e}")
        print(f"Error: {e}", file=sys.stderr)

async def main():
    print("Starting user client...", file=sys.stderr)
    await user_client.start()
    print("✅ User client started", file=sys.stderr)

    print("Starting bot client...", file=sys.stderr)
    await bot_client.start()
    print("✅ Bot client started", file=sys.stderr)

    # Проверяем, что бот может связаться с Telegram
    try:
        me = await bot_client.get_me()
        print(f"✅ Bot connected as @{me.username}", file=sys.stderr)
    except Exception as e:
        print(f"❌ Bot failed to connect to Telegram: {e}", file=sys.stderr)
        # Если ошибка, завершаем работу
        return

    print("Бот запущен и готов к работе!", file=sys.stderr)
    # Бесконечно ждём, пока клиенты работают
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Fatal error: {e}", file=sys.stderr)
        sys.exit(1)
