from vector_stores import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import os
from dotenv import load_dotenv
import config_data as config
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableWithMessageHistory
from file_history_store import get_history



load_dotenv()
api_key = os.getenv("DASHSCOPE_API_KEY")
chat_api = os.getenv("Chat_API_Key")


class RagService(object):
    def __init__(self):
        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings(
                dashscope_api_key=api_key,
                model=config.embedding_model_name,
            )
        )

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system","以我提供的已知参考资料为主"
                 "简结和专业的回答用户的问题。参考资料:{context}。"
                 "并且我提供用户的对话的历史记录如下："),
                 MessagesPlaceholder("history"),
                 ("user","请回答用户的提问：{input}")
            ]
        )

        self.chat_model = ChatOpenAI(
            api_key=chat_api,
            base_url=config.base_url,
            model=config.chat_model_name
        )

        self.chain = self.__get_chain()

    def __get_chain(self):
        retriver =self.vector_service.get_retriever()

        def format_document(docs:list[Document]):
            if not docs:
                return "无相关参考资料"
            formatted_str = ""
            for doc in docs:
                formatted_str+= f"文档片段：{doc.page_content}\n文档元数据：{doc.metadata}\n\n"
            return formatted_str
        
        def format_for_retriever(value:dict) -> str:
            return value["input"]
        
        def format_for_prompt_template(value:dict) -> str:
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["context"]=value["context"]
            new_value["history"] = value["input"]["history"]
            return new_value

        chain = (
            {
                "input":RunnablePassthrough(),
                "context": RunnableLambda(format_for_retriever) | retriver | format_document
            } | RunnableLambda(format_for_prompt_template) | self.prompt_template | self.chat_model | StrOutputParser()
        )

        conversation_chain=RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )

        return conversation_chain


if __name__ == "__main__":                                                                   
    res=RagService().chain.invoke( {"input":"春天穿什么颜色"},config.session_config)
    print(res)                                                        