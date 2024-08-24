import asyncio
import logging

from client import run_tcp_echo_client
from database import init_db
from server import run_server

logging.basicConfig(level=logging.INFO)


async def main():
    # Инициализация БД
    await init_db()

    # Запуск TCP-сервера
    server_task = asyncio.create_task(run_server())

    # Запуск 10 клиентов
    client_tasks = [
        asyncio.create_task(run_tcp_echo_client(i)) for i in range(10)
    ]

    # Ожидаем завершения всех клиентов
    await asyncio.gather(*client_tasks)

    # Останавливаем сервер после завершения всех клиентов
    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        logging.info("Server task cancelled")


if __name__ == "__main__":
    asyncio.run(main())
