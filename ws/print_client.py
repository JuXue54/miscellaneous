import socketio

# 创建 Socket.IO 客户端
sio = socketio.Client()

# 连接事件
@sio.event
def connect():
    print("成功连接到服务端")
    msg = input("输入内容")
    sio.emit('message',
                {
                    "event": "START_PRINT_TASK",
                    "taskId": "",
                    "meta": {"msg": msg }
                })


# 断开事件
@sio.event
def disconnect():
    print("已断开连接")


# 自定义事件处理
@sio.on('message')
def on_message(data):
    print("收到消息:", data)

if __name__ == '__main__':
    # 连接到 Socket.IO 服务端
    sio.connect('http://localhost:9999')  # 根据你的服务端地址修改
    sio.wait()
