import json

import websocket
import threading

def on_message(ws, message):
    try:
        data = json.loads(message)
        if data.get('event', '') == 'STARTED':
            ws.send('{"page": 1}', opcode=websocket.ABNF.OPCODE_TEXT)
            ws.send('apple', opcode=websocket.ABNF.OPCODE_BINARY)
            ws.send('{"page": 2}', opcode=websocket.ABNF.OPCODE_TEXT)
            ws.send('orange', opcode=websocket.ABNF.OPCODE_BINARY)
        elif data.get('event', '') == 'SUCCESS':
            print(f'SUCCESS: {data.get("fileSize")}')
    except Exception as e:
        print(f"📩 收到消息: {message}")


def on_error(ws, error):
    print(f"❌ 错误: {error}")

def on_close(ws, close_status_code, close_msg):
    print("🔒 连接关闭")

def on_open(ws):
    print("连接打开")
    # def run():
    #     while True:
    #         msg = input("你说：")
    #         ws.send(f"""
    #         {{
    #             "event": "START_PRINT_TASK",
    #             "taskId": "",
    #             "meta": {{ "msg": "{msg}" }}
    #         }}
    #         """)
    # threading.Thread(target=run).start()

# 替换为你的 WebSocket 服务器地址

if __name__ == "__main__":
    ws_url = "ws://127.0.0.1:8080/speech"

    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(
        ws_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    ws.run_forever()
