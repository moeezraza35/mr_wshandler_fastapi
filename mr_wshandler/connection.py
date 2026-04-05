from fastapi import WebSocket

class Connection:
  def __init__(self, websocket:WebSocket, clientId:int|str) -> None:
    self.websocket = websocket
    self.clientId = clientId
    self.rooms:list[str] = []
  
  def __str__(self) -> str:
    return f"Connection: {self.websocket} | Client ID: {self.clientId}\nRooms: {self.rooms}"
  
  async def close(self):
    await self.websocket.close()
