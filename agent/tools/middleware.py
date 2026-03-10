from langchain.agents.middleware import wrap_tool_call, before_model
from langchain.tools.tool_node import ToolCallRequest
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from typing import Callable
from utils.logger_handler import logger
from langgraph.runtime import Runtime

@wrap_tool_call
def monitor_tool(
    #请求的数据封装
    request: ToolCallRequest,
    #请求的处理函数
    handler: Callable[[ToolCallRequest], ToolMessage | Command ]
) -> ToolMessage | Command:
    logger.info(f"[tool monitor]执行工具：{request.tool_call['name']}")
    logger.info(f"[tool monitor]传入参数：{request.tool_call['args']}")

    try:
        result = handler(request)
        logger.info(f"[tool monitor],工具{request.tool_call['name']}执行成功")

        return result
    except Exception as e:
        logger.error(f"工具{request.tool_call['name']}执行失败，{e}")
        raise e
    

@before_model
def log_before_model(
    state,
    runtime: Runtime,
):
    logger.info(f"[log_before_model]即将调用模型，带有{len(state['messages'])}条消息")
    logger.debug(f"[log_before_model]{type(state['messages'][-1]).__name__}['messages{state['messages'][-1].content.strip()}")
    return None


