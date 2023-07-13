import hashlib
import uvicorn
from typing import List

from fastapi import FastAPI
from fastapi import Response
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from message import MessageBody
import base64
import json
import logging
import requests

gunicorn_logger = logging.getLogger('gunicorn.error')

app = FastAPI()

encoding = 'utf-8'


@app.get("/")
def home():
    sha1 = hashlib.sha1()
    sha1.update("41cd274dace59708".encode(encoding))
    return Response(sha1.hexdigest())


@app.post("/")
async def home_post(body: MessageBody):
    await manager.broadcast(body.Msg.Content)
    content = base64.b64decode(body.Msg.Content).decode(encoding)
    aiui = json.loads(content)
    gunicorn_logger.info(f"aiui：{content}")
    uuid = aiui.get('uuid', 'unknown')
    text = aiui.get('text', 'unknown')
    data = {"sid": "44", "uuid": uuid, "text": text}
    rsp = requests.post("http://47.106.32.164:8091/system/webSocket/sendAudioFile", data).text
    gunicorn_logger.info(f"推送结果：{rsp}")
    return aiui


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(client_id: str, websocket: WebSocket):
    # 1、客户端、服务端建立 ws 连接
    await manager.connect(websocket)
    # 2、广播某个客户端进入聊天室
    await manager.broadcast(f"{client_id} 进入了聊天室")
    try:
        while True:
            # 3、服务端接收客户端发送的内容
            data = await websocket.receive_text()
            # 4、广播某个客户端发送的消息
            await manager.broadcast(f"{client_id} 发送消息：{data}")
            # 5、服务端回复客户端
            await manager.send_personal_message(f"服务端回复{client_id}：你发送的信息是：{data}", websocket)
    except WebSocketDisconnect:
        # 6、若有客户端断开连接，广播某个客户端离开了
        manager.disconnect(websocket)
        await manager.broadcast(f"{client_id} 离开了聊天室")


# 处理和广播消息到多个 WebSocket 连接
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        gunicorn_logger.info(f"broadcast live {len(self.active_connections)} message = {message}")
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()

if __name__ == "__main__":
    uvicorn.run("main:app")
