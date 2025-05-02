from fastapi import WebSocket
from typing import List
import json


class socketio:

    def __init__(self):
        self.__active_clients: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.__active_clients.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.__active_clients.remove(websocket)

    async def broadcast(self, data_type: str, data: str):
        send_data = json.dumps({
            "data_type": data_type,
            "data": data
        })

        for allclient in self.__active_clients:
            await allclient.send_text(send_data)

    def Getclinetsinfo(self):
        return len(self.__active_clients)
