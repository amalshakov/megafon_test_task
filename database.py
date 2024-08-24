import aiosqlite

DATABASE_FILE = "megafon_test_task.db"


async def init_db():
    async with aiosqlite.connect(DATABASE_FILE) as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS megafon_test_task (
                message TEXT,
                timestamp TEXT
            )"""
        )
        await db.commit()


async def save_message_to_db(message, timestamp):
    async with aiosqlite.connect(DATABASE_FILE) as db:
        await db.execute(
            "INSERT INTO megafon_test_task (message, timestamp) VALUES (?, ?)",
            (message, timestamp.strftime("%Y-%m-%d %H:%M:%S")),
        )
        await db.commit()
