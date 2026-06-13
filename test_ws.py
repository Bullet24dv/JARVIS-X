import asyncio
import websockets

async def test():
    try:
        async with websockets.connect("ws://127.0.0.1:8000/ws-test") as ws:
            await ws.send("test")
            response = await ws.recv()
            print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(test()) 