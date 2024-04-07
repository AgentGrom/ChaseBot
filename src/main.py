import asyncio
import telegram

from src.config import TOKEN

async def main():
    bot:telegram.Bot = telegram.Bot(TOKEN)
    async with bot:
        updates = (await bot.get_updates())[0].message.chat
        print(updates)


if __name__ == '__main__':
    asyncio.run(main())