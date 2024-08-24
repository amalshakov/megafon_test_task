import asyncio
import logging
import random

logging.basicConfig(level=logging.INFO)


# TCP-клиенты
async def run_tcp_echo_client(client_id, host="127.0.0.1", port=8888):
    reader, writer = await asyncio.open_connection(host, port)

    for i in range(1, 6):
        await asyncio.sleep(random.uniform(5, 10))
        message = f"Hello from client {client_id}, message {i}"
        logging.info(f"Client {client_id} sending: '{message}'")
        writer.write(message.encode())
        await writer.drain()

        # Получаем эхо-ответ
        data = await reader.read(100)
        logging.info(f"Client {client_id} received: {data.decode()}")

    logging.info(f"Client {client_id} closing connection")
    writer.close()
    await writer.wait_closed()
