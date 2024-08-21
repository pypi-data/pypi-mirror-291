# python3.8
import os
import random

from paho.mqtt import client as mqtt_client

from ZRunAuto.config.logger import log


class MqttConfig:

    def __init__(self):
        self.broker = 'l728d872.ala.cn-hangzhou.emqxsl.cn'
        self.port = 8883
        self.topic = [("test/2", 0), ("test/1", 0)]
        # generate client ID with pub prefix randomly
        self.client_id = f'python-mqtt-{random.randint(0, 100)}'
        self.username = 'sun-client'
        self.password = 'qq123456'
        self.client = None  # type:mqtt_client

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            log.info("Connected to MQTT Broker!")
        else:
            log.info("Failed to connect, return code %d\n:{}", rc)

    @staticmethod
    def on_message(client, userdata, msg):
        log.info("Received {} from {} topic", msg.payload.decode(), msg.topic)

    def get_topics(self, topic):
        # 使用列表推导式提取所有元组的第一个元素
        return [topic[0] for topic in topic]

    def connect_mqtt(self, task_id: str) -> mqtt_client:
        try:
            client = mqtt_client.Client(self.client_id + task_id)
            # 获取当前文件的完整路径
            current_file_path = os.path.abspath(__file__)
            # 获取当前文件所在的目录
            current_directory = os.path.dirname(current_file_path)
            client.tls_set(ca_certs=current_directory + '/emqxsl-ca.crt')
            client.username_pw_set(self.username, self.password)
            client.on_connect = self.on_connect
            client.on_message = self.on_message
            client.connect(self.broker, self.port)
            task_topic = ('test/' + task_id, 0)
            self.topic.append(task_topic)
            client.subscribe(self.topic)
            log.info('当前订阅Topic：{}', self.get_topics(self.topic))
            self.client = client
            return client
        except Exception as e:
            print(f"Failed to connect to MQTT server: {e}")
            return None  # 或者抛出异常，取决于你的错误处理策略

    def run(self, task_id):
        pub_client = self.connect_mqtt(task_id)
        # client.loop_forever()
        pub_client.loop_start()

    def publish_msg(self, task_id, msg):
        msg_count = 0
        msg = f"messages: {str(msg)}"
        result = self.client.publish("test/" + task_id, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic test/`{task_id}`")
        else:
            print(f"Failed to send message to topic test/{task_id}")
        msg_count += 1

    def stop(self):
        self.client.loop_stop()
        log.info(str(self.client) + '已关闭连接')


MqttConfig = MqttConfig()
