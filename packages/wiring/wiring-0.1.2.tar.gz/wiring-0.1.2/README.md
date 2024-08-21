![logo with a label 'one bot codebase - multiple platforms'](https://i.ibb.co/1QGmCQx/343200157-4b987f42-1718-4a83-83b1-dc5556da28af.png)

seamless api for developing bots that run on multiple platforms.
**discord**, **telegram** and **twitch** are supported

works with asyncio

learn more in the sections below or **[docs](https://github.com/crucials/wiring/wiki)**

## install

install the base library:

```sh
pip install wiring
```

then choose extra dependencies for platforms that you want your bot to run on

```sh
pip install wiring[discord] wiring[telegram]
```

## usage example

```python
import asyncio

from wiring import (Bot, MultiPlatformMessage, MultiPlatformBot, MultiPlatformUser,
                    Command)
from wiring.platforms.discord import DiscordBot
from wiring.platforms.telegram import TelegramBot


DISCORD_TOKEN = 'place your token here or better load it from enviroment variables'
TELEGRAM_TOKEN = 'place your token here or better load it from enviroment variables'

async def send_commands_list(bot: Bot, message: MultiPlatformMessage,
                             args: list[str]):
    commands_list = '\n'.join(['/' + str(command.name) for command
                               in bot.commands])

    await bot.send_message(
        message.chat.id,
        'available commands:\n' + commands_list,
        reply_message_id=message.id
    )


async def start_bots():
    bot = MultiPlatformBot()

    bot.platform_bots = [
        DiscordBot(DISCORD_TOKEN),
        TelegramBot(TELEGRAM_TOKEN)
    ]

    async with bot:
        await bot.setup_commands([
            Command('help', send_commands_list)
        ])

        # blocks the execution
        await bot.listen_to_events()


asyncio.run(start_bots())
```
