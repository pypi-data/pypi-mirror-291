import json
import logging
import threading
from enum import Enum
from typing import Callable

from zyjj_client_sdk.base.base import Base
from zyjj_client_sdk.base.api import ApiService
import paho.mqtt.client as mqtt


class MqttEventType(Enum):
    Start = 1  # 开始任务
    Progress = 2  # 进度事件
    Success = 3  # 成功
    Fail = 4  # 失败
    DetailAppend = 5  # 详情追加
    DetailSet = 6  # 详情覆盖


class MqttServer:
    def __init__(self, base: Base, api: ApiService):
        self.__close = False
        self.__subscribe = {}
        # 获取客户端信息
        info = api.cloud_get_mqtt()
        host, client_id, username, password = (info['host'], info['client_id'], info['username'], info['password'])
        logging.info(f"mqtt info host {host} client_id {client_id} username {username} password {password}")
        # 如果设置了代理，那么就连接代理域名
        if base.mqtt_proxy is not None:
            logging.info(f"use proxy {base.mqtt_proxy}")
            self.__client = mqtt.Client(client_id=client_id, protocol=mqtt.MQTTv311, transport='websockets')
            self.__client.connect(base.mqtt_proxy, 80, 30)
        else:
            self.__client = mqtt.Client(client_id=client_id, protocol=mqtt.MQTTv311)
            self.__client.connect(host, 1883, 30)
        self.__client.username_pw_set(username, password)
        self.__client.on_connect = lambda client, userdata, flags, rc: self.__on_connect()
        self.__client.on_message = lambda client, userdata, msg: self.__on_message(msg)

    def __on_connect(self):
        logging.info(f'[mqtt] connect success')
        # 启动后自动订阅topic
        for topic, handle in self.__subscribe.items():
            logging.info(f'[mqtt] subscribe {topic}')
            self.__client.subscribe(topic, qos=2)
        if self.__close:
            self.close()

    def __run(self):
        self.__client.loop_forever()

    def __on_message(self, msg: mqtt.MQTTMessage):
        logging.info(f'[mqtt] from {msg.topic} get message {msg.payload}')
        event = json.loads(msg.payload)
        for topic, handle in self.__subscribe.items():
            if topic.endswith('/+'):
                if msg.topic.startswith(topic[:topic.index('/+')] + '/'):
                    handle(msg.topic, event)
            elif msg.topic == topic:
                handle(topic, event)

    def start_backend(self):
        threading.Thread(target=self.__run).start()

    def start(self):
        self.__run()

    def close(self):
        self.__close = True
        self.__client.disconnect()

    # 发送event事件
    def send_task_event(self, uid: str, task_id: str, event_type: MqttEventType, data=None):
        logging.info(f'[mqtt] task_event/{uid} send message {event_type} data {data}')
        self.__client.publish(
            f"task_event/{uid}",
            json.dumps({
                'task_id': task_id,
                'event_type': event_type.value,
                'data': data
            }, ensure_ascii=False),
            qos=1,
            retain=True
        )

    # 监听topic
    def add_subscribe(self, topic: str, handle: Callable[[str, dict], None]):
        self.__subscribe[topic] = handle
