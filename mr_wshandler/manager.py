from fastapi import WebSocket
from .connection import Connection
from typing import Callable

class ConnectionManager:
  """
**ConnectionManager Class**

Manages multiple WebSocket connections, client IDs, and rooms.

This class is the core of the library. It keeps track of all active `Connection` objects, handles sending messages (text, bytes, JSON), supports client-specific addressing via `clientId`, and provides room-based messaging. It also offers `onopen` and `onclose` callbacks.

**Attributes:**
- `active_connections` (list[Connection]): List of currently connected clients.
- `onopen` (Callable | None): Callback invoked when a new connection is added.
- `onclose` (Callable | None): Callback invoked before a connection is removed.

**Methods:**
- `connect`: Accept a WebSocket and store it.
- `set_client_id`: Assign an ID to a connection.
- `disconnect`: Close and remove a connection (server-initiated).
- `send_message`: Core method to send a message (type-aware).
- `send_message_to_connection`: Alias for send_message.
- `send_message_to_client_id`: Send a message to a specific client by ID.
- `add_client_id_to_room`: Add a client (by ID) to a room.
- `remove_client_id_from_room`: Remove a client from a room.
- `add_connection_to_room`: Add a connection (by WebSocket) to a room.
- `remove_connection_from_room`: Remove a connection from a room.
- `send_message_to_room`: Send a message to all clients in a room.
- `broadcast`: Send a message to every active connection.

**Note:**
The room methods currently compare `connection == clientId` directly (in `add_client_id_to_room` and `remove_client_id_from_room`). This should be `connection.clientId == clientId` for correct behaviour.
  """
  def __init__(self):
    self.active_connections: list[Connection] = []
    self.onopen:Callable|None = None
    self.onclose:Callable|None = None

  async def connect(self, websocket:WebSocket):
    """Accept a WebSocket, wrap it in a Connection, add to the list, and call onopen."""
    await websocket.accept()
    newConnection = Connection(websocket,0)
    self.active_connections.append(newConnection)
    if self.onopen:
      await self.onopen(newConnection)

  async def set_client_id(self, websocket:WebSocket, clientId:int|str):
    """Assign a client ID to the connection identified by the WebSocket object."""
    for connection in self.active_connections:
      if connection.websocket is websocket:
        connection.clientId = clientId
        break

  async def disconnect(self, websocket:WebSocket):
    """Close the WebSocket, call onclose, and remove the connection."""
    for connection in self.active_connections:
      if connection.websocket is websocket:
        if self.onclose:
          await self.onclose(connection)
        self.active_connections.remove(connection)
        break

  async def send_message(self, message:str|bytes|dict, websocket:WebSocket):
    """
Send a message to a single connection.

Automatically picks the correct WebSocket method:
- str → `send_text`
- bytes → `send_bytes`
- dict → `send_json`

**Raises:**
  TypeError: If message type is not str, bytes, or dict.
    """
    if type(message) == str:
      await websocket.send_text(message)
    elif type(message) == bytes:
      await websocket.send_bytes(message)
    elif type(message) == dict:
      await websocket.send_json(message)   # fixed
    else:
      raise TypeError("Message must be str, bytes, or dict")

  async def send_message_to_connection(self, message:str|bytes|dict, websocket:WebSocket):
    """Alias for send_message - sends a message to a specific connection."""
    await self.send_message(message, websocket)
  
  async def send_message_to_client_id(self, message:str|bytes|dict, clientId:int|str):
    """Send a message to the connection that has the given clientId."""
    for connection in self.active_connections:
      if connection.clientId == clientId:
        await self.send_message(message, connection.websocket)
        break

  def add_client_id_to_room(self, clientId:int|str, room:str):
    """Add a client (by ID) to a room. (Note: currently compares `connection == clientId`.)"""
    for connection in self.active_connections:
      if connection == clientId:
        if not room in connection.rooms:
          connection.rooms.append(room)
        break

  def remove_client_id_from_room(self, clientId:int|str, room:str):
    """Remove a client from a room. (Note: currently compares `connection == clientId`.)"""
    for connection in self.active_connections:
      if connection == clientId:
        connection.rooms.remove(room)
        break

  def add_connection_to_room(self, websocket:WebSocket, room:str):
    """Add a connection (by WebSocket object) to a room."""
    for connection in self.active_connections:
      if connection.websocket is websocket:
        if not room in connection.rooms:
          connection.rooms.append(room)
        break

  def remove_connection_from_room(self, websocket:WebSocket, room:str):
    """Remove a connection (by WebSocket) from a room."""
    for connection in self.active_connections:
      if connection.websocket is websocket:
        connection.rooms.remove(room)
        break

  async def send_message_to_room(self, message:str|bytes|dict, room:str):
    """Send a message to all connections that are members of the given room."""
    for connection in self.active_connections:
      if room in connection.rooms:
        await self.send_message(message, connection.websocket)

  async def broadcast(self, message:str|bytes|dict):
    """Send a message to every active connection (no filtering)."""
    for connection in self.active_connections:
      await self.send_message(message, connection.websocket)

connectionManager = ConnectionManager()
"""**connectionManager** is global variable initializes on the first import and can be used anywhere in the program."""