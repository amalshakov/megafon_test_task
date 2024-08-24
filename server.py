import asyncio
import logging
from datetime import datetime

from database import save_message_to_db

logging.basicConfig(level=logging.INFO)


# TCP-сервер
async def handle_echo(reader, writer):
    addr = writer.get_extra_info("peername")
    logging.info(f"New connection from {addr}")

    while True:
        data = await reader.read(100)
        if not data:
            break
        message = data.decode()
        logging.info(f"Received {message} from {addr}")

        # Сохранение данных в БД
        await save_message_to_db(message, datetime.now())

        writer.write(data)
        await writer.drain()

    logging.info(f"Close the connection: {addr}")
    writer.close()
    await writer.wait_closed()


async def run_server(host="127.0.0.1", port=8888):
    server = await asyncio.start_server(handle_echo, host, port)
    addr = server.sockets[0].getsockname()
    logging.info(f"Serving on {addr}")

    async with server:
        await server.serve_forever()
