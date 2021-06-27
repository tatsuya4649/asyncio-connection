#!/bin/env python
import asyncio

async def handle_echo(reader,writer):
	data = await reader.read(100)
	message = data.decode()
	addr = writer.get_extra_info('peername')

	print(f'Received: {message} from {addr}')
	print(f'Send: {message}')
	await writer.drain()

	print('Close connection')
	writer.close()

async def tcp_echo_server():
	server = await asyncio.start_server(
		handle_echo,'127.0.0.1',8888)
	
	addr = server.sockets[0].getsockname()
	print(f'Serving on {addr}')

	async with server:
		await server.serve_forever()

if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	loop.run_until_complete(tcp_echo_server())
