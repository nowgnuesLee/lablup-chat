#!/bin/bash

# 변수 설정
IMAGE_NAME="chat-front:latest"
DOCKERFILE="frontend.Dockerfile"
DOCKER_COMPOSE_FILE="docker-compose.yml"
BUILD_CONTEXT="."
PORT=3001

# 이미지 빌드
echo "Building Docker image: $IMAGE_NAME"
docker build -t $IMAGE_NAME -f $DOCKERFILE $BUILD_CONTEXT

# 빌드 성공 여부 확인
if [ $? -eq 0 ]; then
  echo "Docker image $IMAGE_NAME built successfully!"
else
  echo "Failed to build Docker image $IMAGE_NAME."
  exit 1
fi

# 도커 컴포즈 기준으로 컨테이너 내리기
echo "Stopping and removing existing Docker container..."
docker compose -f $DOCKER_COMPOSE_FILE down || true

# 도커 컴포즈 기준으로 컨테이너 올리기
echo "Starting Docker container..."
docker compose -f $DOCKER_COMPOSE_FILE up -d

# 컨테이너 실행 여부 확인
if [ $? -eq 0 ]; then
  echo "Docker container started successfully! Access your app at http://localhost:$PORT"
else
  echo "Failed to start Docker container."
  exit 1
fi