#!/bin/bash

# 변수 설정
DOCKER_COMPOSE_FILE="docker-compose.yml"
BUILD_CONTEXT="."
PORT=3001

# 도커 컴포즈 기준으로 컨테이너 내리기
echo "Stopping and removing existing Docker container..."
docker compose -f $DOCKER_COMPOSE_FILE down --rmi all || true

# 도커 컴포즈 기준으로 컨테이너 올리기
echo "Starting Docker container..."
docker compose -f $DOCKER_COMPOSE_FILE up --build -d

# 컨테이너 실행 여부 확인
if [ $? -eq 0 ]; then
  echo "Docker container started successfully! Access your app at http://localhost:$PORT"
else
  echo "Failed to start Docker container."
  exit 1
fi