from langchain.agents import create_agent 
from model.factory import chat_model
from utils.prompt_loader import load_system_prompt
from agent.tools.agent_tools import rag_summarize, get_weather,get_user_location
from agent.tools.middleware import monitor_tool, log_before_model



class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model = chat_model,
            system_prompt = load_system_prompt(),
            tools = [rag_summarize,get_user_location,get_weather],
            middleware = [monitor_tool,log_before_model],
        )

    def execute_stream(self, query: str):
        input_dict = {
            "messages": [
                {"role":"user","content":query},
            ]
        }

        for chunk in self.agent.stream(input_dict,stream_mode = "values",context = {"report":False}):
            latest_message = chunk["messages"][-1]
            if latest_message.content:
                yield latest_message.content.strip() +  "\n"

if __name__ == "__main__":
    agent = ReactAgent()
    for chunk in agent.execute_stream("我感觉最近压力好大呀，在学agent，你就是我创造的agent，我好像没有坚持下去的动力了"):
        print(chunk, end="", flush = True)
