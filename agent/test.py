from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("Chat_API_Key")

@tool(description="请输入城市名字，返回天气情况")
def get_weather():
    return "晴天"

agent = create_agent(
    model = ChatOpenAI(
        api_key=api_key,
        model="abab6.5-chat",
        base_url="https://api.minimaxi.com/v1"),
    tools=[get_weather],
    system_prompt="你是用户(小混沌)的好友，用户有什么问题要积极帮助他。注意：要以朋友的口吻说话"
)

res = agent.invoke(
    {
        "messages":[
            {"role":"user","content":"明天重庆的天气如何？"}
        ]
    }
)


parser=StrOutputParser()

for message in res["messages"]:
    print(f"{type(message).__name__}:{parser.invoke(message)}")