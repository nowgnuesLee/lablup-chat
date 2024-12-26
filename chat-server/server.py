import asyncio
import redis.asyncio as aioredis
from aiohttp import web

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

# WebSocket 핸들러
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    room_name = request.query.get("room", "default")
    client_address = request.remote
    print(f"클라이언트 연결됨: {client_address}, 룸: {room_name}")

    # Redis에서 메시지 구독 (비동기 작업 실행)
    subscriber_task = asyncio.create_task(redis_subscriber(room_name, ws))

    redis = await aioredis.from_url(REDIS_URL)
    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                # 메시지 Redis 채널로 Publish
                message = f"[{client_address}] {msg.data}"
                print(message)
                await redis.publish(room_name, message)
            elif msg.type == web.WSMsgType.CLOSE:
                print(f"클라이언트 연결 종료: {client_address}")
                break
    except Exception as e:
        print(f"에러 발생: {e}")
    finally:
        # WebSocket 종료 시 Redis 구독 취소
        subscriber_task.cancel()
        await redis.close()

    return ws

# HTTP 서버 초기화
async def init_app():
    app = web.Application()
    app.router.add_get('/ws', websocket_handler)  # WebSocket 경로
    return app

# 서버 실행
if __name__ == '__main__':
    try:
        web.run_app(init_app(), host='127.0.0.1', port=8080)
    except KeyboardInterrupt:
        print("서버 종료됨")
