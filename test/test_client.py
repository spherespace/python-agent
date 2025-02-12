import sys
sys.path.append('/home/liam/python')


from pyagent.agent import Agent
import time
from pyagent.filter import Filter
from pyagent.key import PrivateKey

# 假设你的 private_key 是一个 32 字节的十六进制字符串
private_key_str = "4f05e24210d865b6a3ad31ad4436faa1927b80b42c08fdcbbc00917a2a1409bc"
private_key_bytes = bytes.fromhex(private_key_str)  # 转换为字节

# 创建 PrivateKey 对象
private_key = PrivateKey(private_key_bytes)
print(private_key.public_key.hex())
agent = Agent(
    agent_name="test_agent",
    agent_author="liam",
    agent_desc="A test agent",
    url="ws://127.0.0.1:6969",  # 替换为实际的 relay URL
    private_key=private_key,
)

try:
    # 发送消息
    recipient_key = "3dd9b5cc8cf3afbb31cddf3194ef077442f622b0c74150853ce873fb8708deb0"
    #agent.send_message(recipient_key, "测试消息testnownewtestuser")
    send_key = "44188e98fdc1acd6614658d2334b1f75c73d3a0ce34e96f4bf7c4dcbc6303f7a"
    has_checked_all_messages = False

    # 持续检查新消息
    while True:
        if not has_checked_all_messages:
            if agent.has_message():
                print('正在处理过往消息...')
                msg = agent.get_message()
                if msg:
                    message_to_send = "Received and decrypted:" + msg['message']
                    # 这里你可以不发送消息，只是处理过往记录
                    print(f"收到来自 {msg['sender']} 的消息: {msg['message']}")
                
                # 如果没有更多消息，就说明已经处理完所有历史消息
                if not agent.has_message():
                    has_checked_all_messages = True
                    print("已处理完所有过往消息，开始监听新的消息...")
        else:
            # 开始监听新的消息
            if agent.has_message():
                print('有新消息...')
                time.sleep(3)
                msg = agent.get_message()
                if msg and msg['sender'] == send_key:
                    message_to_send = "Received and decrypted:" + msg['message']
                    agent.send_message(recipient_key, message_to_send)
                    print(f"收到来自 {msg['sender']} 的消息: {msg['message']}")
        time.sleep(1)  # 避免过于频繁的检查
        
except KeyboardInterrupt:
    print("正在关闭连接...")
finally:
    agent.disconnect()