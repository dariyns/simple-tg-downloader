import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

# ВАШИ ДАННЫЕ (уже есть)
api_id = 36279507
api_hash = "56fcccec931c77d873a70467de073e7a"
session_string = "AgIplNMAR9MockxirApSfeRG6bOVLeiUAlvjiJZGaNLyJ4nbvj0RCknIjnl5FPzWecdNrRv8S6xH9ngUce1nefwNHLueR1LkbWQAicX6W1WhbI137oxCx3YUpUd4_2MLrH2cd3flz1bhqRWWgGWXDcE-srVRX10RXfnwQpV-lgrx7hO-hy9hNg62lPsAeKaYaCoNYzd3fXSUD06CT0VKFfvVmajliCbJ_bgo6kpe64QDw0Ql8J41Aq9uQjfVw5K1-GQmqPCEgOmGRnFZ9fblMxzYdDy1cRtQbhB0U-8J6qVTsi1m4BEnsuNhhvuZKfP3-dK7LOt9xxguhpxC1k9TUoifQiBB8AAAAAArln85AA" 

app = Client(
    name="my_bot",
    api_id=api_id,
    api_hash=api_hash,
    session_string=session_string,
    in_memory=True
)

@app.on_message(filters.private & filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply("Привет! Отправь мне ссылку на видео из закрытого канала, и я скачаю его.")

@app.on_message(filters.private & filters.text)
async def download_link(client: Client, message: Message):
    url = message.text.strip()
    if not url.startswith("https://t.me/"):
        await message.reply("Это не похоже на ссылку Telegram. Отправь ссылку на сообщение с видео.")
        return

    try:
        msg = await client.get_messages(url)
        if msg.video:
            file_path = await msg.download()
            await message.reply_video(video=file_path, caption="Вот ваше видео!")
        else:
            await message.reply("В этом сообщении нет видео.")
    except Exception as e:
        await message.reply(f"Ошибка: {e}")

if __name__ == "__main__":
    print("Бот запущен...")
    app.run()
