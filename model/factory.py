from abc import ABC, abstractmethod
from typing import Optional
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.embeddings import Embeddings
from langchain_openai.chat_models.base import BaseChatOpenAI
from utils.config_handler import rag_conf
from os import getenv
from dotenv import load_dotenv

load_dotenv()
embedding_api = getenv("DASHSCOPE_API_KEY")
chat_model_api = getenv("Chat_API_Key")



class BaseModefactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatOpenAI]:
        pass


class ChatModelFactory(BaseModefactory):
    def generator(self) -> Optional[Embeddings | BaseChatOpenAI]:
        return ChatOpenAI(model=rag_conf["chat_model_name"],api_key=(rag_conf.get("chat_api_key") or chat_model_api),base_url=rag_conf.get("chat_base_url"))
    
class EmbeddingFactory(BaseModefactory):
    def generator(self) -> Optional[Embeddings | BaseChatOpenAI]:
        return DashScopeEmbeddings(model = rag_conf.get("embedding_model_name"),dashscope_api_key=(rag_conf.get("dashscope_api_key") or embedding_api))
    

chat_model = ChatModelFactory().generator()
embed_model = EmbeddingFactory().generator()