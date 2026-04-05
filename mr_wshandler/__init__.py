from fastapi import WebSocket, WebSocketDisconnect
from typing import Callable, Literal
from json.decoder import JSONDecodeError
from .manager import connectionManager

class WSHandler:
  """
**WSHandler Class**

Decorator-based WebSocket handler for FastAPI.

This class provides a clean, reusable way to define WebSocket endpoints. It automatically manages the connection lifecycle (accept, receive loop, disconnect) and delegates incoming messages to your callback. The callback receives both the decoded message and the `WebSocket` object.

The global `connectionManager` is used internally - you can access it directly from your callbacks to broadcast, send to rooms, etc.

**Example:**
```python
ws = WSHandler()

@ws.endpoint(mode="dict")
async def onMessage(data: dict, websocket: WebSocket):
    await connectionManager.broadcast(data)
```

**Attributes:**
  None (uses global `connectionManager` for state).
  """
  def __init__(self) -> None:
    """Initialise the handler. The global connectionManager must already exist."""
    pass

  def set_onopen(self, callback:Callable) -> None:
    """
Register a callback to be executed when a new WebSocket connection is established.

The callback should accept one argument: the Connection object.

**Args:**
callback: Async function that takes a Connection parameter.

**Example:**

```python
@ws.set_onopen
async def onopen(conn: Connection):
    print(f"New connection: {conn.clientId}")
```
    """
    connectionManager.onopen = callback

  def set_onclose(self, callback:Callable) -> None:
    """
Register a callback to be executed when a WebSocket connection is closed.

The callback should accept one argument: the Connection object.

**Args:**
- `callback:` Async function that takes a Connection parameter.
    """
    connectionManager.onclose = callback
  
  def endpoint(self, mode:Literal["bytes","dict","str"]="str") -> Callable:
    """
Decorator factory for a WebSocket endpoint.

This method returns a decorator that wraps your message-handling function. The decorated function must accept (data, websocket) as parameters.

**Args:**

`mode:` How to receive incoming messages.
- `"str"` : calls websocket.receive_text() (default)
- `"bytes"`: calls websocket.receive_bytes()
- `"dict"` : calls websocket.receive_json(). If JSON decoding fails, an empty dict {} is passed to the callback.

**Returns:**
A decorator that transforms your callback into a FastAPI WebSocket endpoint.

**Raises:**
- `NotImplementedError`: If the global connectionManager is None (should never happen).

**Example:**

```python
@app.websocket("/ws")
@ws.endpoint(mode="dict")
async def onMessage(data: dict, websocket: WebSocket):
    await connectionManager.broadcast(data)
```
    """
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
