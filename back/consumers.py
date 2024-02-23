import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .utils.boss import run_crawl  # 假设这是您的爬虫程序


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crawl_running = False  # 控制爬虫运行的标志
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if message == "start":
            self.crawl_running = True
            await self.start_crawl()
        elif message == "stop":
            self.crawl_running = False

    async def start_crawl(self):
        try:
            # 确保 run_crawl 是一个生成器
            for output in run_crawl():
                if not self.crawl_running:
                    break  # 如果收到停止指令，退出循环
                send_msg = json.dumps({'message': output},ensure_ascii=False)
                # 解码 JSON 字符串中的 Unicode 转义字符
                print(f"向前端发送消息:{send_msg}")
                await self.send(text_data=send_msg)
                await asyncio.sleep(0.5)  # 控制消息发送的速度
        except Exception as e:
            await self.send(text_data=json.dumps({'error': str(e)}))
