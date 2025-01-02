# Lablup Internship Onboarding Assignment - Web Chat
This assignment involves implementing a web-based chat application using asyncio, aiohttp, and redis.
## Contents in This Repository
This repository includes both the chat server and the chat web application
* `chat-server`: Chat server
* `chat-web`: Chat web application
* `backend.Dockerfile`: Dockerfile for the chat server
* `frontend.Dockerfile`: Dockerfile for the chat web application
* `docker-compose.yml`: Docker Compose configuration file
* `build.sh`: Script to run Docker Compose automatically
* `README.md`: This file
## Run Automatically
Since Docker Compose is used for automatic execution, Docker installation is required.
### 권한 부여
```bash
chmod +x ./build.sh
```
### Run build.sh
```bash
./build.sh
```
If executed successfully, you can access the chat web application at localhost:3001.
## Run Manually
For manual execution instructions, please refer to the README.md file in each project directory.