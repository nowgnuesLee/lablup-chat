import asyncio
import redis.asyncio as aioredis
from aiohttp import web
import json
import multiprocessing

# Room name
ROOM_NAME = "lablup"

# Redis 연결 정보
REDIS_URL = "redis://localhost:6379"

# Redis Pub/Sub
async def redis_subscriber(room_name, ws):
    redis = await aioredis.from_url(REDIS_URL)
    try:
        pubsub = redis.pubsub()
        await pubsub.subscribe(room_name)
        print(f"Redis 채널 구독 시작: {room_name}")

        # Redis 메시지 수신 및 WebSocket으로 전달
        async for message in pubsub.listen():
            if message["type"] == "message":
                await ws.send_str(message["data"].decode("utf-8"))
    except asyncio.CancelledError:
        print(f"Redis 구독 취소됨: {room_name}")
    finally:
        await pubsub.unsubscribe(room_name)
        await redis.close()

async def rcv_msg(ws, redis, client_name, client_address):
    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                # 메시지 Redis 채널로 Publish
                message_obj = {
                    "type": "message",
                    "userId": client_name,
                    "message": msg.data,
                }
                await redis.publish(ROOM_NAME, json.dumps(message_obj))
            elif msg.type == web.WSMsgType.CLOSE:
                print(f"클라이언트 연결 종료: {client_address}, 이름: {client_name}")
                break
    except Exception as e:
        raise e


# WebSocket 핸들러
async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request) # WebSocket 연결 준비

    redis = None
    subscriber_task = None

    try:
        redis = await aioredis.from_url(REDIS_URL)

        # 유저 카운트 증가 및 이름 할당
        user_count = await redis.incr("user_count")
        client_name = f"User{user_count}"
        client_address = request.remote
        print(f"클라이언트 연결됨: {client_address}, 룸: {ROOM_NAME}, 이름: {client_name}")

        # 클라이언트에 이름 전달
        await ws.send_json({"type": "info", "userId": client_name, "message": f"Welcome! Your name is: {client_name}"})

        # Redis에서 메시지 구독 (비동기 작업 실행)
        subscriber_task = asyncio.create_task(redis_subscriber(ROOM_NAME, ws))
        receiver_task = asyncio.create_task(rcv_msg(ws, redis, client_name, client_address))
        
    except Exception as e:
        print(f"에러 발생: {e}")
    finally:
        # WebSocket 종료 시 Redis 구독 취소
        if subscriber_task:
            subscriber_task.cancel()
        if receiver_task:
            receiver_task.cancel()
        if redis:
            await redis.close()

    return ws

# HTTP 서버 초기화
async def init_app():
    app = web.Application()
    app.router.add_get('/chat', websocket_handler)  # WebSocket 경로
    return app


def start_server():
        web.run_app(init_app(), host='127.0.0.1', port=8080, reuse_port=True)

# 서버 실행
if __name__ == '__main__':
    num_processes = multiprocessing.cpu_count()
    print(f"서버 시작: CPU 코어 수 {num_processes}")
    processes = []
    try:
        for _ in range(num_processes):
            p = multiprocessing.Process(target=start_server)
            p.start()
            processes.append(p)

        for p in processes:
            p.join()
    except KeyboardInterrupt:
        print("서버 종료됨")
        for p in processes:
            p.terminate()
            p.join()