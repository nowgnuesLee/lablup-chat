# Chat Server
A chat server developed using aiohttp, asyncio, and Redis.
## Getting Started
We are currently using Python version 3.12.6. Since Redis is being used, Redis installation is required.
### Installation With pip
``` bash
pip install -r requirements.txt
```
### Run Server
``` bash
python server.py
```
## Env
```
HOST=SERVER_HOST
PORT=SERVER_PORT
REDIS_HOST=REDIS_HOST
REDIS_PORT=REDIS_PORT

MAX_PROCESSES=NUMBER_OF_PROCESSES

ROOM_NAME=ROOM_NAME
```
## Simulation
You can interact with the running chat server through client.py. You can run multiple clients to simulate a scenario with multiple clients.
### Run Client
```bash
python client.py
```