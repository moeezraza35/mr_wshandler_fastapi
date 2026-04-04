from fastapi import FastAPI
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

# @connectionManager.set_onopen
# def onopen():
#   print("New connection established!")

@app.websocket("/ws")
@ws.endpoint
async def onMessage(data:str):
  print(data)
  print(connectionManager)
  await connectionManager.broadcast(data)

if __name__ == "__main__":
  uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
