#!/bin/env python
import asyncio

_READ_DATA_LENGTH=1024

async def tcp_echo_client(message,port,loop):
	print("Open Connection...")
	reader,writer = await asyncio.open_connection("127.0.0.1",port,loop=loop)

	print(f'Send: {message}')
	writer.write(message.encode())

	data = await reader.read(_READ_DATA_LENGTH)
	print(f'Received: {data.decode()}')

	print('Close the Socket')
	writer.close()


if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.run_until_complete(tcp_echo_client('helloworld',8888,loop))
	loop.close()
