import yaml

import logging
import asyncio

from .classes.bot import SupportBot

def load_config(config_file):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

def main():
    config = load_config("config.yaml")
    bot = SupportBot(config)

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("nio").setLevel(logging.WARNING)

    asyncio.get_event_loop().run_until_complete(bot.login())
    asyncio.get_event_loop().run_until_complete(bot.start())

if __name__ == "__main__":
    main()