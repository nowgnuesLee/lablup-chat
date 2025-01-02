import asyncio
import sys
import json
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from typing import cast
import logging
from aiohttp import web
import redis.asyncio as aioredis
from decouple import config

# 로깅 설정
logging.basicConfig(level=logging.INFO)

# Max processes
MAX_PROCESSES: int = config("MAX_PROCESSES", cast=int, default=5)

# Room name
ROOM_NAME: str = cast(str, config("ROOM_NAME", default="chat"))

# Redis 연결 정보
REDIS_HOST: str = cast(str, config("REDIS_HOST", default="localhost"))
REDIS_PORT: int = cast(int, config("REDIS_PORT", cast=int, default=6379))
REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}"

# Server config
HOST: str = cast(str, config("HOST", cast=str, default="127.0.0.1"))
PORT: int = cast(int, config("PORT", cast=int, default=8080))


# Redis Pub/Sub
async def redis_subscriber(
    room_name: str, ws: web.WebSocketResponse, redis: aioredis.Redis
) -> None:
    """Redis 채널 구독 및 메시지 수신"""
    try:
        async with redis.pubsub() as pubsub:
            await pubsub.subscribe(room_name)
            logging.info("Redis 구독: %s", room_name)

            # Redis 메시지 수신 및 WebSocket으로 전달
            async for message in pubsub.listen():
                if message["type"] == "message":
                    await ws.send_str(message["data"].decode("utf-8"))
    except asyncio.CancelledError:
        logging.error("Redis 구독 취소됨: %s", room_name)


async def rcv_msg(
    ws: web.WebSocketResponse,
    redis: aioredis.Redis,
    user_id: str,
    client_address: str,
) -> None:
    """웹 소켓에서 메시지를 수신하고 Redis 채널로 Publish"""
    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                # 메시지 Redis 채널로 Publish
                message_obj = {
                    "type": "message",
                    "userId": user_id,
                    "message": msg.data,
                }
                await redis.publish(ROOM_NAME, json.dumps(message_obj))
            elif msg.type == web.WSMsgType.CLOSE:
                logging.info(
                    "클라이언트 연결 종료, 주소: %s, 유저 아이디: %s",
                    client_address,
                    user_id,
                )
                break
            elif msg.type == web.WSMsgType.ERROR:
                logging.error(
                    "클라이언트 연결 종료, 주소: %s, 유저 아이디: %s",
                    client_address,
                    user_id,
                )
                break
    except Exception as e:
        logging.error("메시지 수신 중 에러 발생: %s", e)


# WebSocket 핸들러
async def websocket_handler(request):
    """웹 소켓 핸들러"""
    ws = web.WebSocketResponse()
    await ws.prepare(request)  # WebSocket 연결 준비

    try:
        async with aioredis.from_url(REDIS_URL) as redis:
            # 유저 카운트 증가 및 이름 할당
            user_count = await redis.incr("user_count")
            user_id = f"User{user_count}"
            client_address = request.remote
            logging.info(
                "클라이언트 연결됨, 주소: %s, 유저 아이디: %s",
                client_address,
                user_id,
            )

            # 클라이언트에 이름 전달
            await ws.send_json(
                {
                    "type": "info",
                    "userId": user_id,
                    "message": f"Welcome! Your name is: {user_id}",
                }
            )
            try:
                async with asyncio.TaskGroup() as tg:
                    tg.create_task(rcv_msg(ws, redis, user_id, client_address))
                    tg.create_task(redis_subscriber(ROOM_NAME, ws, redis))
            except asyncio.CancelledError:
                logging.info("비동기 작업이 취소되었습니다.")
    except Exception as e:
        logging.error("소켓 처리 중 에러 발생: %s", e)

    finally:
        await ws.close()
        logging.info("클라이언트 연결 종료")

    return ws


# HTTP 서버 초기화
async def init_app():
    """HTTP 서버 초기화"""
    app = web.Application()
    app.router.add_get("/chat", websocket_handler)  # WebSocket 경로
    return app


def start_server():
    """HTTP 서버 시작"""
    logging.info("서버 시작됨: %d", multiprocessing.current_process().pid)
    logging.info("서버 주소: %s:%d", HOST, PORT)
    try:
        web.run_app(init_app(), host=HOST, port=PORT, reuse_port=True)
    except Exception as e:
        logging.error("서버 실행 중 에러 발생: %s", e)
    finally:
        logging.info("서버 종료됨: %d", multiprocessing.current_process().pid)


# 서버 실행
if __name__ == "__main__":
    try:
        with ProcessPoolExecutor(max_workers=MAX_PROCESSES) as executor:
            futures = [executor.submit(start_server) for _ in range(MAX_PROCESSES)]
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    logging.error("서버 실행 중 에러 발생: %s", e)
    except KeyboardInterrupt:
        logging.error("종료됨")
    finally:
        sys.exit(0)
