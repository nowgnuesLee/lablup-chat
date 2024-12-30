import asyncio
from typing import cast
from aioconsole import ainput  # 비동기 입력 처리
from decouple import config
import websockets

HOST = cast(str, config("HOST", default="127.0.0.1", cast=str))
PORT = cast(int, config("PORT", default=8080, cast=int))
SERVER_URL = f"ws://{HOST}:{PORT}/chat"


async def send_messages(websocket):
    """사용자 입력을 처리하여 메시지를 서버로 전송"""
    while True:
        message = await ainput("메시지 입력: ")  # 비동기 입력 처리
        await websocket.send(message)
        print(f"서버로 보낸 메시지: {message}")


async def receive_messages(websocket):
    """서버로부터 메시지를 수신하여 출력"""
    while True:
        try:
            print("메시지 수신 대기중")
            response = await websocket.recv()
            print(f"브로드캐스트 메시지: {response}")
        except websockets.ConnectionClosed:
            print("서버와의 연결이 종료되었습니다.")
            break


async def client():
    """웹소켓 클라이언트"""
    uri = SERVER_URL
    async with websockets.connect(uri) as websocket:
        print("룸에 연결됨")

        # 송신 및 수신을 각각 비동기 태스크로 실행
        send_task = asyncio.create_task(send_messages(websocket))
        receive_task = asyncio.create_task(receive_messages(websocket))

        # 두 태스크 중 하나가 종료될 때까지 대기
        _, pending = await asyncio.wait(
            [send_task, receive_task],
            return_when=asyncio.FIRST_COMPLETED,
        )

        # 종료되지 않은 태스크를 취소
        for task in pending:
            task.cancel()


if __name__ == "__main__":
    asyncio.run(client())
