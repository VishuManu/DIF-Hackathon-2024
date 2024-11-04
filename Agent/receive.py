'''import asyncio
import websockets

async def subscribe():
    uri = "ws://localhost:6969"  # Replace with your WebSocket URL
    
    async with websockets.connect(uri) as websocket:
        await websocket.send('{"type": "subscribe", "channel": "your_channel"}')
        
        while True:
            # Wait for a message from the WebSocket server
            message = await websocket.recv()
            print(f"Received message: {message}")

# Run the WebSocket client
asyncio.get_event_loop().run_until_complete(subscribe())
'''