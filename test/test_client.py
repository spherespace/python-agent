import sys
sys.path.append('/home/liam/python')
from pyagent.agent import Agent
import time
from pyagent.filter import Filter
from pyagent.key import PrivateKey

# 假设你的 private_key 是一个 32 字节的十六进制字符串
private_key_str = "928e7d737b02b4b875f5dfa5796226d09c334676c98a3ad7594b2129ec01e939"
private_key_bytes = bytes.fromhex(private_key_str)  # 转换为字节

# 创建 PrivateKey 对象
private_key = PrivateKey(private_key_bytes)

agent = Agent(
    agent_name="test_agent",
    agent_author="liam",
    agent_desc="A test agent",
    url="ws://127.0.0.1:6969",  # 替换为实际的 relay URL
    private_key=private_key,
    # filter=Filter(
    #     pubkey_refs=["e2d11a1ac40fb27556046c1ff47ee27f6e3ce580d5859c11e0edf43765678669"],  # 这里添加指定的 pubkey
    #     kinds=[4]  # 这里添加 kind=4，即 EncryptedDirectMessage
    # )
)

try:
    # 发送消息
    # recipient_key = "e2d11a1ac40fb27556046c1ff47ee27f6e3ce580d5859c11e0edf43765678669"
    # agent.send_message(recipient_key, "测试消息testnownewtestuser")
    
    # 持续检查新消息
    while True:
        if agent.has_message():
            print('have message')
            msg = agent.get_message()
            if msg:
                print(f"收到来自 {msg['sender']} 的消息: {msg['message']}")
        time.sleep(3)  # 避免过于频繁的检查
        
except KeyboardInterrupt:
    print("正在关闭连接...")
finally:
    agent.disconnect()