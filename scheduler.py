from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime


def create_scheduler(bot):
    scheduler = AsyncIOScheduler(timezone="UTC")

    # Daily at 20:00 UTC
    scheduler.add_job(
        lambda: bot.send_message(chat_id=bot.owner_id,
                                 text="Опишите главное событие дня, эмоцию и оцените ее от 1 до 10"),
        'cron', hour=20, minute=0
    )

    # Weekly on Sunday at 20:00 UTC
    scheduler.add_job(
        lambda: bot.send_message(chat_id=bot.owner_id,
                                 text="Какая из эмоций недели была самой яркой?"),
        'cron', day_of_week='sun', hour=20, minute=0
    )

    # Monthly on the 1st at 20:00 UTC
    scheduler.add_job(
        lambda: bot.send_message(chat_id=bot.owner_id,
                                 text="Какая из эмоций месяца была самой запоминающейся?"),
        'cron', day=1, hour=20, minute=0
    )

    return scheduler
