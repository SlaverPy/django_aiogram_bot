from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: list
    use_redis: bool
    bot_name: str
    chat_id: str


@dataclass
class Config:
    tg_bot: TgBot
    redis_host: str = None


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(tg_bot=TgBot(token=env.str("BOT_TOKEN"),
                               admin_ids=list(map(int, env.list("ADMINS"))),
                               use_redis=env.bool("USE_REDIS"),
                               bot_name=env.str("BOT_NAME"),
                               chat_id=env.str("CHAT_ID")))
