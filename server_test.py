import asyncio
import websockets
import json

async def handler(websocket, path):
    print(f"WebSocket connection from {websocket.remote_address}")
    try:
        await websocket.send(json.dumps({"type": "connected", "message": "Connected to JARVIS-X"}))
        async for message in websocket:
            print(f"Received: {message}")
            try:
                # Intentar parsear como JSON
                data = json.loads(message)
                if data.get("type") == "ping":
                    await websocket.send(json.dumps({"type": "pong"}))
                else:
                    await websocket.send(json.dumps({"type": "echo", "data": data}))
            except json.JSONDecodeError:
                # Si no es JSON, enviar como texto
                await websocket.send(f"Echo: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("WebSocket disconnected")

async def main():
    async with websockets.serve(handler, "127.0.0.1", 8001):
        print("WebSocket server running on ws://127.0.0.1:8001")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())