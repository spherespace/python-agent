from langchain.llms.base import LLM
from langchain.prompts import PromptTemplate
from typing import Any, List, Optional, Dict
import cohere
from pydantic import Field, BaseModel

class CohereCustomLLM(LLM, BaseModel):
    """自定义的 Cohere LLM 类，继承自 LangChain 的 LLM 基类"""
    
    api_key: str = Field(..., description="Cohere API 密钥")
    client: Any = None

    def __init__(self, api_key: str, **kwargs):
        """初始化 Cohere LLM
        
        Args:
            api_key (str): Cohere API 密钥
        """
        super().__init__(api_key=api_key, **kwargs)
        self.client = cohere.Client(self.api_key)
    
    @property
    def _llm_type(self) -> str:
        """返回 LLM 类型"""
        return "cohere_custom"

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """获取标识参数"""
        return {"model": "command"}
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs: Any) -> str:
        """调用 Cohere API 生成回复
        
        Args:
            prompt (str): 输入提示
            stop (Optional[List[str]]): 停止词列表
            
        Returns:
            str: 生成的文本回复
        """
        try:
            response = self.client.generate(
                prompt=prompt,
                model='command',
                max_tokens=300,
                temperature=0.7,
                num_generations=1
            )
            return response.generations[0].text
        except Exception as e:
            print(f"调用 Cohere API 时发生错误: {str(e)}")
            return ""

class CohereAgent:
    """Cohere 问答代理类"""
    
    def __init__(self, api_key: str):
        """初始化 Cohere 代理
        
        Args:
            api_key (str): Cohere API 密钥
        """
        self.llm = CohereCustomLLM(api_key=api_key)
        
        # 创建提示模板
        self.prompt = PromptTemplate(
            input_variables=["question"],
            template="请回答下面的问题：{question}"
        )
        
        # 创建新的 Runnable 链
        self.chain = self.prompt | self.llm
    
    def ask(self, question: str) -> str:
        """向代理提问并获取回答
        
        Args:
            question (str): 输入的问题
            
        Returns:
            str: 代理的回答
        """
        try:
            # 使用同步的 invoke 方法
            response = self.chain.invoke({"question": question})
            return response.strip()
        except Exception as e:
            print(f"获取回答时发生错误: {str(e)}")
            return ""

def get_ai_response(question: str) -> str:
    """获取 AI 回答的外部接口函数
    
    Args:
        question (str): 输入的问题
        
    Returns:
        str: AI 的回答
    """
    try:
        agent = CohereAgent(api_key="你的_COHERE_API_KEY")
        return agent.ask(question)
    except Exception as e:
        return f"发生错误: {str(e)}"

if __name__ == "__main__":
    # 测试代码
    API_KEY = "你的_COHERE_API_KEY"
    
    # 创建代理实例
    agent = CohereAgent(api_key=API_KEY)
    
    # 测试提问
    question = "苹果的英文是什么？"
    answer = agent.ask(question)
    print(f"问题: {question}")
    print(f"回答: {answer}")