# MR WS Handler for FastAPI

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://python.org)
[![FastAPI Version](https://img.shields.io/badge/fastapi-0.100%2B-green)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

**A lightweight, reusable WebSocket handler for FastAPI** – developed by Moeez Raza.

The goal of this project is to make using WebSockets in FastAPI **easier, simpler, and faster**. Stop copying connection‑management code between projects. Just install, import, and focus on your real‑time logic.

## ✨ Features

- ✅ **Simple connection manager** – handles accept, store, disconnect.
- ✅ **Broadcast to all connected clients** – one line to send a message to everyone.
- ✅ **Send to specific client ID** – direct messaging with integer or string IDs.
- ✅ **Room support** (optional) – group clients into rooms for targeted broadcasts.
- ✅ **Multiple message types** – `str`, `bytes`, `dict` (auto‑converted to JSON).
- ✅ **Ready‑to‑use HTML/JS test client** – no need to write frontend code for testing.
- ✅ **Fully async** – built for high‑performance FastAPI apps.
- ✅ **Reusable** – publish to PyPI and `pip install` in any project.

## 📦 Installation

```bash
pip install mr-fastapi-wshandler
```
Or install directly from GitHub:
```bash
pip install git+https://github.com/your-username/mr_fastapi_wshandler.git
```
## 🚀 Quick Start
### 1. Create a FastAPI app with WebSocket endpoint
```python
from fastapi import FastAPI
from mr_wshandler import WSHandler, connectionManager

app = FastAPI()
ws = WSHandler()

@app.websocket("/ws")
@ws.endpoint
async def handle_message(data: str):
    # Echo the message back to everyone
    await connectionManager.broadcast(data)
```
### 2. Run the server
```bash
uvicorn main:app --reload
```
### 3. Test with the included HTML client
Open terminal and try to run the demo/main.py and access it on http://localhost:8000.

## 📚 API Reference
### `WSHandler`
`WSHandler()` – creates a new handler (uses the global connection manager).

`@WSHandler.endpoint` – decorator for your WebSocket route. Takes a callback that receives each incoming message.

### `ConnectionManager` (global `connectionManager`)
`async connect(websocket)` – accepts and stores a new connection.

`async disconnect(websocket)` – closes and removes a connection (server‑initiated).

`async remove_connection(websocket)` – removes a connection without closing (client‑initiated).

`async broadcast(message)` – sends message to all active connections.

`async send_to_client_id(message, client_id)` – sends to a specific client.

`async set_client_id(websocket, client_id)` – assigns an ID to a connection.

## 🧪 Testing
A full HTML/JS test client is included in the repository. Open it in your browser to interact with your WebSocket server.

## 🤝 Contributing
Contributions are welcome! Feel free to open issues or pull requests.

## 📄 License
This project is licensed under the MIT License – see the LICENSE.md file for details.

## 🔗 References
- [FastAPI WebSocket Documentation](https://fastapi.tiangolo.com/advanced/websockets/)
- [Python WebSockets](https://websockets.readthedocs.io/)

Made with ❤️ by Moeez Raza

Tags: `python` `fastapi` `websocket` `socket-server` `real-time`

## What to change

- Replace `your-username` with your actual GitHub username.
- If you haven't added a `LICENSE` file yet, do so (MIT suggested).
- The badge URLs assume your repository is public – they'll work automatically.

This README is informative, encourages adoption, and highlights the reusability you wanted. Just copy‑paste it into your repository's `README.md`.