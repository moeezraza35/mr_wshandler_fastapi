from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from pathlib import Path
import uvicorn
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from mr_wshandler import WSHandler, connectionManager

app = FastAPI()
ws = WSHandler()

@app.get("/")
async def index():
  file = open("demo/index.html", "rb")
  return HTMLResponse(file.read())

@ws.set_onopen
async def onopen(connection):
  print("New connection established!", connection)

@ws.set_onclose
async def onclose(connection):
  print("Connection closed!", connection)

@app.websocket("/ws")
@ws.endpoint(mode="dict")
async def onMessage(data:dict, websocket:WebSocket):
  if "room" in data:
    if "action" in data:
      if data["action"] == "join":
        connectionManager.add_connection_to_room(websocket, data["room"])
      elif data["action"] == "leave":
        connectionManager.remove_connection_from_room(websocket, data["room"])
    await connectionManager.send_message_to_room(data, data["room"])
  elif "clientId" in data:
    if "action" in data:
      if data["action"] == "set":
        await connectionManager.set_client_id(websocket, data["clientId"])
    await connectionManager.send_message_to_client_id(data, data["clientId"])
  else:
    await connectionManager.broadcast(data)
  print(data)

if __name__ == "__main__":
  uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
