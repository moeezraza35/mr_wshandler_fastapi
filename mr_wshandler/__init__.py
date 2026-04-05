from fastapi import WebSocket, WebSocketDisconnect
from typing import Callable, Literal
from json.decoder import JSONDecodeError
from .manager import connectionManager

class WSHandler:
  def __init__(self) -> None:
    pass
  
  def endpoint(self, mode:Literal["bytes","dict","str"]="str") -> Callable:
    def decorator(callback:Callable):
      async def wrapper(websocket:WebSocket):
        if not connectionManager: raise NotImplementedError("Connection Manager is not set.\nconnectionManager: {}".format(connectionManager))
        await connectionManager.connect(websocket)
        try:
          while True:
            data:bytes|dict|str|None = None
            if mode == "str":
              data = await websocket.receive_text()
            elif mode == "bytes":
              data = await websocket.receive_bytes()
            elif mode == "dict":
              try:
                data = await websocket.receive_json()
              except JSONDecodeError:
                data = {}
            await callback(data, websocket)
        except WebSocketDisconnect:
          await connectionManager.disconnect(websocket)
      return wrapper
    return decorator
