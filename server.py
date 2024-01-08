import websockets
import asyncio

all_clients = []

async def relay(socket):
	print("Client accepted")

	# Initial setup

	for client in all_clients:
		try:
			# Announce new client to other clients
			await client.send("A")
		except websockets.exceptions.ConnectionClosed:
			pass

	all_clients.append(socket)

	# Main loop - route all recieved messages

	while True:
		message = ""
		try:
			message = await socket.recv()
		except websockets.exceptions.ConnectionClosed:
			# This socket is closed - no need to continue
			all_clients.remove(socket)
			return

		# Echo the message to other clients
		for client in all_clients:
			if client == socket:
				continue	# Don't echo message back

			try:
				await client.send(message)
			except websockets.exceptions.ConnectionClosed:
				# Socket closed
				all_clients.remove(client)

async def main():
	print("Starting the server...")

	async with websockets.serve(relay, "0.0.0.0", 4174, max_size=2**26, read_limit=2**26, write_limit=2**26):
		await asyncio.Future()

asyncio.run(main())
