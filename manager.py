import asyncio
import json
import websockets

SERVER_URL = "wss://archipelago.gg:38281"  # Replace with target port

async def connect_archipelago():
    async with websockets.connect(SERVER_URL) as websocket:
        # Step 1: Wait for RoomInfo
        room_info = await websocket.recv()
        print("Connected to server:", json.loads(room_info))

        # Step 2: Send Connect packet
        connect_packet = [{
            "cmd": "Connect",
            "password": "",
            "game": "Archipelago",  # Or specific game name
            "name": "PlayerName",
            "uuid": "unique-client-id",
            "tags": ["AP"],
            "version": {"major": 0, "minor": 4, "build": 4, "class": "Version"},
            "items_handling": 7  # Receive items from all sources
        }]
        await websocket.send(json.dumps(connect_packet))

        # Step 3: Listen for incoming messages
        while True:
            response = await websocket.recv()
            packets = json.loads(response)
            for packet in packets:
                cmd = packet.get("cmd")
                if cmd == "Connected":
                    print(f"Successfully joined! Slot ID: {packet['slot']}")
                elif cmd == "ReceivedItems":
                    print(f"Items received: {packet['items']}")
                elif cmd == "PrintJSON":
                    # Formatted chat/item messages
                    msg = "".join([part.get("text", "") for part in packet.get("data", [])])
                    print(f"[Log] {msg}")

asyncio.run(connect_archipelago())
