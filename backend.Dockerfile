# 베이스 이미지로 Python 3.12.6 사용
FROM python:3.12.6

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 필수 라이브러리 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/log/supervisor

# Python 패키지 의존성 파일 복사
COPY ./chat-server/requirements.txt .

# Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY ./chat-server/server.py .

# 환경 변수 설정 (기본값 제공)
ENV HOST=0.0.0.0
ENV PORT=8080
# local redis
ENV REDIS_HOST=localhost
ENV REDIS_PORT=6379
ENV ROOM_NAME=lablup
ENV MAX_PROCESSES=5

EXPOSE 8080

# 컨테이너에서 실행할 명령어 정의
ENTRYPOINT [ "python", "server.py" ]