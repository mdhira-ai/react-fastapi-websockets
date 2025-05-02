from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from typing import List
import time
import json
from soc import socketio
import uvicorn


app = FastAPI()
manager = socketio()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/ws/{clientid}")
async def mysock(websocket: WebSocket, clientid: int):
    await manager.connect(websocket=websocket)

    try:

        # sending notification with "system"
        await manager.broadcast(
            data_type="system",
            data={"message": f"client {clientid} joined the chat"},
        )

        # sendind time to client with "time"
        time_task = asyncio.create_task(send_periodic_updates())

        await sendclientinfo()

        while True:
            # coming from client
            data = await websocket.receive_text()

            try:

                # sending message with type "chat"
                message_data = json.loads(data)
                if message_data["data_type"] == "chat":
                    await manager.broadcast(
                        data_type="chat",
                        data={
                            "client_id": clientid,
                            "message": message_data["message"],
                        },
                    )

            except:
                await manager.broadcast(
                    data_type="chat", data={"client_id": clientid, "message": data}
                )

    except:
        manager.disconnect(websocket=websocket)
        await sendclientinfo()

        await manager.broadcast(
            data_type="system", data={"message": f"client {clientid} left the chat"}
        )

        time_task.cancel()


# for time function
async def send_periodic_updates():
    while True:
        current_time = time.strftime("%H:%M:%S")

        await manager.broadcast(data_type="time", data={"time": current_time})

        await asyncio.sleep(1)


async def sendclientinfo():
    await manager.broadcast(
        data_type="clientinfo", data={"message": manager.Getclinetsinfo()}
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
