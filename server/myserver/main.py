from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from typing import List
import time
import json


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class connectionmanager:
    def __init__(self):
        self.activeconn: List[WebSocket] = []

    async def connect(self, websocket: WebSocket, clientid: int):
        await websocket.accept()
        print(f"{clientid} is connected")
        self.clietn_id = clientid
        self.activeconn.append(websocket)

    def disconnect(self, websocket: WebSocket):
        print(f"{self.clietn_id} is disconnected")
        self.activeconn.remove(websocket)

    async def broadcast(self, message_type: str, data: str):
        message = json.dumps({"type": message_type, "data": data})

        for connectedclient in self.activeconn:
            await connectedclient.send_text(message)


manager = connectionmanager()


@app.websocket("/ws/{clientid}")
async def mysock(websocket: WebSocket, clientid: int):
    await manager.connect(websocket=websocket, clientid=clientid)

    try:

        # sending notification with "system"
        await manager.broadcast(
            message_type="system",
            data={"message": f"client {clientid} joined the chat"},
        )


        # sendind time to client with "time"
        time_task = asyncio.create_task(send_periodic_updates())



        while True:
            # coming from client
            data = await websocket.receive_text()

            try:

                # sending message with type "chat"
                message_data = json.loads(data)
                if message_data["type"] == "chat":
                    await manager.broadcast('chat',{
                        "client_id":clientid,
                        "message": message_data["message"]
                    })

            except:
                await manager.broadcast("chat",{
                    "client_id":clientid,
                    "message":data
                })


    except:
        manager.disconnect(websocket=websocket)
        print(f"{clientid} is disconnected")


        await manager.broadcast("system",{
            "message":f"client {clientid} left the chat"
        })

        time_task.cancel()



# for time function
async def send_periodic_updates():
    while True:
        current_time = time.strftime("%H:%M:%S")

        await manager.broadcast("time",{
            "time":current_time
        })

        await asyncio.sleep(1)
