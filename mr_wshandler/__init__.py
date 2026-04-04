from fastapi import WebSocket, WebSocketDisconnect
from .manager import connectionManager
from typing import Callable

class WSHandler:
  def __init__(self) -> None:
    pass
  
  def endpoint(self, callback:Callable) -> Callable:
    async def wrapper(websocket:WebSocket):
      if not connectionManager: raise NotImplementedError("Connection Manager is not set.\nconnectionManager: {}".format(connectionManager))
      await connectionManager.connect(websocket)
      try:
        while True:
          data = await websocket.receive_text()
          await callback(data)
      except WebSocketDisconnect:
        await connectionManager.disconnect(websocket)
    return wrapper
