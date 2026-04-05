from fastapi import WebSocket
from .connection import Connection
from typing import Callable

class ConnectionManager:
  def __init__(self):
    self.active_connections: list[Connection] = []
    self._onopen:Callable|None = None
  
  def set_onopen(self, onopen:Callable|None):
    self._onopen = onopen

  async def connect(self, websocket:WebSocket):
    await websocket.accept()
    self.active_connections.append(Connection(websocket,0))
    if self._onopen:
      self._onopen()

  async def set_client_id(self, websocket:WebSocket, clientId:int|str):
    for connection in self.active_connections:
      if connection.websocket is websocket:
        connection.clientId = clientId
        break

  async def disconnect(self, websocket:WebSocket):
    for connection in self.active_connections:
      if connection.websocket is websocket:
        self.active_connections.remove(connection)
        break

  async def send_message(self, message:str|bytes|dict, websocket:WebSocket):
    if type(message) == str:
      await websocket.send_text(message)
    elif type(message) == bytes:
      await websocket.send_bytes(message)
    elif type(message) == dict:
      await websocket.send_json(message)   # fixed
    else:
      raise TypeError("Message must be str, bytes, or dict")

  async def send_message_to_connection(self, message:str|bytes|dict, websocket:WebSocket):
    await self.send_message(message, websocket)
  
  async def send_message_to_client_id(self, message:str|bytes|dict, clientId:int|str):
    for connection in self.active_connections:
      if connection.clientId == clientId:
        await self.send_message(message, connection.websocket)
        break

  def add_client_id_to_room(self, clientId:int|str, room:str):
    for connection in self.active_connections:
      if connection == clientId:
        if not room in connection.rooms:
          connection.rooms.append(room)
        break

  def remove_client_id_from_room(self, clientId:int|str, room:str):
    for connection in self.active_connections:
      if connection == clientId:
        connection.rooms.remove(room)
        break

  def add_connection_to_room(self, websocket:WebSocket, room:str):
    for connection in self.active_connections:
      if connection.websocket is websocket:
        if not room in connection.rooms:
          connection.rooms.append(room)
        break

  def remove_connection_from_room(self, websocket:WebSocket, room:str):
    for connection in self.active_connections:
      if connection.websocket is websocket:
        connection.rooms.remove(room)
        break

  async def send_message_to_room(self, message:str|bytes|dict, room:str):
    for connection in self.active_connections:
      if room in connection.rooms:
        await self.send_message(message, connection.websocket)

  async def broadcast(self, message:str|bytes|dict):
    for connection in self.active_connections:
      await self.send_message(message, connection.websocket)

connectionManager = ConnectionManager()
