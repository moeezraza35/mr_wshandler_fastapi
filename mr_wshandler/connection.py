from fastapi import WebSocket

class Connection:
  """
    **Connection Class**

    This class wraps a FastAPI `WebSocket` connection, adding a client ID and room tracking.

    **Attributes**

    - `websocket` : `WebSocket` - the actual connection.
    - `clientId` : `int | str` - unique identifier for this connection.
    - `rooms` : `list[str]` - room names this connection has joined.

    **Methods**

    - `close()` - asynchronously closes the WebSocket.
    """
  def __init__(self, websocket:WebSocket, clientId:int|str) -> None:
    self.websocket = websocket
    self.clientId = clientId
    self.rooms:list[str] = []
  
  def __str__(self) -> str:
    return f"Connection: {self.websocket} | Client ID: {self.clientId}\nRooms: {self.rooms}"
  
  async def close(self):
    await self.websocket.close()
