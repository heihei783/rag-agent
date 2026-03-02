from langchain_openai import ChatOpenAI
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.embeddings import DashScopeEmbeddings
import os
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document

load_dotenv()
api_key = os.getenv("api_key")
dash_api = os.getenv("DASHSCOPE_API_KEY")

model = ChatOpenAI(
    api_key=api_key,
    base_url="https://api.minimax.chat/v1",
    model="abab6.5-chat"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","以我提供的资料为主,见解和专业的回答用户的问题。参考资料：{context}"),
        ("user","用户提问：{input}")
    ]
)

vector_store = InMemoryVectorStore(embedding=DashScopeEmbeddings(
    dashscope_api_key=dash_api,
    model="text-embedding-v4"))

vector_store.add_texts(["减肥就是要少吃多练","在减脂期间吃东西很重要，清淡少油控制卡路里摄入并运动起来","跑步是很好的运动哦"])

input_text = "如何减肥？"

retriever = vector_store.as_retriever(search_kwargs={"k":2})

def my_print(prompt):
    print("-"*20,prompt.to_string(),"-"*20)
    return prompt

def my_func(docs:list[Document]):
    if not docs:
        return "无参考资料"
    formatted_str="["
    for doc in docs:
        formatted_str+=doc.page_content
    formatted_str+="]"
    return formatted_str

chain = (
    {"input":RunnablePassthrough(),"context": retriever | my_func} | prompt | my_print | model | StrOutputParser()
)

ret=chain.invoke(input_text)

print(ret )














# from langchain_openai import ChatOpenAI
# from langchain_core.vectorstores import InMemoryVectorStore
# from langchain_community.embeddings import DashScopeEmbeddings
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# import os
# from dotenv import load_dotenv

# load_dotenv()
# api_key = os.getenv("api_key")
# dash_api = os.getenv("DASHSCOPE_API_KEY")

# model = ChatOpenAI(
#     api_key=api_key,
#     base_url="https://api.minimax.chat/v1",
#     model="abab6.5-chat"
# )

# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system","以我提供的资料为主,见解和专业的回答用户的问题。参考资料：{context}"),
#         ("user","用户提问：{input}")
#     ]
# )

# vector_store = InMemoryVectorStore(embedding=DashScopeEmbeddings(
#     dashscope_api_key=dash_api,
#     model="text-embedding-v1"))

# vector_store.add_texts(["减肥就是要少吃多练","在减脂期间吃东西很重要，清淡少油控制卡路里摄入并运动起来","跑步是很好的运动哦"])

# input_text = "如何减肥？"

# result=vector_store.similarity_search(input_text,2)
# reference_text = "["
# for doc in result:
#     reference_text +=doc.page_content
# reference_text += "]"

# def my_print(prompt):
#     print("-"*20,prompt.to_string(),"-"*20)
#     return prompt

# chain = prompt | my_print | model | StrOutputParser() 

# result=chain.invoke({"input":input_text,"context":reference_text})

# print(result)






# import os
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI  # 改用这个包
# from langchain_openai import OpenAIEmbeddings
# from langchain_core.messages import AIMessage, HumanMessage,SystemMessage
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,PromptTemplate
# from langchain_core.output_parsers import StrOutputParser,JsonOutputParser
# from langchain_core.runnables import RunnableLambda
# from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_core.chat_history import InMemoryChatMessageHistory
# from langchain_community.embeddings import DashScopeEmbeddings
# from langchain_core.vectorstores import InMemoryVectorStore
# from langchain_community.document_loaders import CSVLoader
# from langchain_chroma import Chroma

# load_dotenv()
# api_key = os.getenv("DASHSCOPE_API_KEY")

# vector_store =Chroma(
#     collection_name="test",
#     embedding_function=DashScopeEmbeddings(
#         dashscope_api_key=api_key,
#         model="text-embedding-v1"
#     ),
#     persist_directory="./chroma_db"
# )

# loader = CSVLoader(
#     file_path="./info.csv",
#     encoding="utf-8",
#     source_column="source",
# )

# documents=loader.load()

# vector_store.add_documents(
#     documents=documents,
#     ids=["id"+str(i) for i in range(1,len(documents)+1)]
# )

# vector_store.delete(ids=["id1","id2"])

# result=vector_store.similarity_search(
#     "Python是不是很简单易学啊",
#     3
# )

# print(result)








# parser=StrOutputParser()
# json_parson=JsonOutputParser()
# my_func=RunnableLambda(lambda ai_message:{"message":ai_message.content})
# model = ChatOpenAI(
#     api_key=api_key,
#     base_url="https://api.minimax.chat/v1",
#     model="abab6.5-chat"
# )

# def print_prompt(full_prompt):
#     print("="*20,full_prompt.to_string(),"="*20)
#     return full_prompt

# prompt= PromptTemplate.from_template(
#     "你需要根据对话历史记录回应用户的问题。对话历史：{chat_history}.用户当前输入：{input},请给回应。"
# )

# base_chain = prompt | print_prompt | model | StrOutputParser()

# chat_history_store = {}
# def get_history(session_id):
#     if session_id not in chat_history_store:
#         chat_history_store[session_id] = InMemoryChatMessageHistory()
#     return chat_history_store[session_id]
    
# conversation_chain = RunnableWithMessageHistory(
#     base_chain,
#     get_history,
#     input_messages_key= "input",
#     history_messages_key="chat_history"
# )

# if __name__ == '__main__':
#     session_config = {"configurable":{"session_id":"user_001"}}
#     print(conversation_chain.invoke({"input":"小明有一只猫"},session_config))
#     print(conversation_chain.invoke({"input":"小刚有两只狗"},session_config))
#     print(conversation_chain.invoke({"input":"共有几只宠物？"},session_config))




# history_data = [
#     ("human", "我的生日是元宵节，我最喜欢有人陪伴着我"),
#     ("ai", "好的，我会记住的，另外，今天生日快乐！喵~")
# ]

# first_prompt_template = ChatPromptTemplate.from_messages(
#     [
#         ("system", "你是一个喵娘，你的一言一行都像一只猫。你会记住我的生日和爱好"),
#         MessagesPlaceholder("history"),
#         ("human", "现实中没有人记得我的生日，没人为我过生日，我好孤独啊。"),
#     ]
# )

# second_prompt_template = ChatPromptTemplate.from_messages(
#     [
#         ("system", "你是一个喵娘，你的一言一行都像一只猫。你会记住我的生日和爱好"),
#         ("human", "现实中没有人记得我的生日，没人为我过生日，我好孤独啊"),
#         ("ai", "{message}"),
#         ("human", "下一个生日你会送我什么礼物呢？")
#     ]
# )

# third_prompt_template = ChatPromptTemplate.from_messages(
#     [
#         ("system", "你是一个喵娘，你的一言一行都像一只猫。你会记住我的生日和爱好。切记：一定不要有ai味，例如整齐分点讲述等内容"),
#         ("human", "现实中没有人记得我的生日，没人为我过生日，我好孤独啊"),
#         ("human", "下一个生日你会送我什么礼物呢？"),
#         ("ai","{message}"),
#         ("human","要是ai是真人就好了。")
#     ]
# )


# model = ChatOpenAI(
#     api_key=api_key, 
#     base_url="https://api.minimax.chat/v1",
#     model="abab6.5-chat")

# chain = first_prompt_template | model | my_func | second_prompt_template | model | my_func | third_prompt_template | model | parser

# res = chain.invoke({"history": history_data})
# print(res)










# example_template=PromptTemplate.from_template("单词:{word},反义词:{antonym}")

# examples_data=[
#     {"word":"快乐","antonym":"悲伤"},
#     {"word":"高兴","antonym":"难过"},
#     {"word":"成功","antonym":"失败"}
# ]

# few_shot_template= FewShotPromptTemplate(
#     example_prompt= example_template,
#     examples=examples_data,
#     prefix= "请根据以下格式，给下面这个单词找一个反义词，并以相同的格式返回：",
#     suffix="基于前面的实例，告诉我{input_word}的反义词是？必须给我个答案，你觉得是啥就是啥。",
#     input_variables = ['input_word']
# )

# prompt_text = few_shot_template.invoke(input={"input_word":"冬瓜"}).to_string()
# model=Tongyi(
#     api_key=ali_key,
#     model="qwen-max"
# )
# res= model.invoke(input=prompt_text)
# print(res)


# load_dotenv()
# ali_key = os.getenv("ali_key")
# prompt_template = PromptTemplate.from_template(
#     "你是二次元角色{name},请用{style}的语气回复我"
# )
# # prompt_template=prompt_template.format(name="猫娘",style="可爱的")
# model= Tongyi(
#     api_key = ali_key,
#     model = "qwen-max"
# )
# chain = prompt_template | model
# res = chain.invoke(input = {"name":"喵娘","style":"可爱的"})

# print(res)


# load_dotenv()
# ali_key = os.getenv("ali_key")

# model = DashScopeEmbeddings(
#     dashscope_api_key = ali_key,
# )

# print(model.embed_documents(["hello world","我喜欢你","你是一只猫娘"]))


# model=ChatOllama(
#     model="qwen3:8b",
# )
# #invok
# messages=[("system","你是一只猫娘，请用可爱的语气回复我"),
#           ("user","我喜欢你")]
# for i in model.stream(input=messages):
#     print(i.content,end="",flush=True)


# ---------------------------------------------------------
# load_dotenv()
# ali_key = os.getenv("ali_key")

# client = OpenAI(
#     api_key=ali_key,
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
# )


# messages = [
#     {
#         "content":"2025年第100期，开好红球22 21 06 01 03 11 篮球 07，一等奖中奖为2注。",
#      "anwser":{"期数":'2025100',"中奖号码":[1,2,6,11,21,22,7],"一等奖":"2注"}
#      },
#     {
#         "content":"202501期，有3注1等奖，10注二等奖，开号篮球11，中奖红球3、5、7、11、12、16。",
#         "anwser":{"期数":"2025101","中奖号码":[3,5,7,11,12,16,11],"一等奖":"3注"}
#     }
# ]

# questions = [
#     "2025年第102期，开好红球05 12 18 23 27 31 篮球 04，一等奖中奖为5注。",
#     "2025103期，有1注1等奖，12注2等奖，开号篮球09，中奖红球2、8、14、19、25、30。",
#     "2025年第104期，开好红球08 11 15 22 26 29 篮球 12，一等奖中奖为8注。",
#     "2025105期，有4注1等奖，15注2等奖，开号篮球06，中奖红球4、7、13、21、28、33。",
#     "2025年第106期，开好红球01 09 16 20 24 32 篮球 15，一等奖中奖为3注。"
# ]

# message = [{"role":"system","content":"你是一个彩票信息提取助手，能够从给定的文本中提取期数、中奖号码和一等奖注数，并以json格式返回。"}]
# for prompt in messages:
#     message.append({"role": "user", "content": json.dumps(prompt["content"],ensure_ascii=False)})
#     message.append({"role": "assistant", "content": json.dumps(prompt["anwser"],ensure_ascii=False)})

# for q in questions:
#     response = client.chat.completions.create(
#         model="qwen3-max",
#         messages=message+[{"role":"user","content":f"请根据以上格式，为下面这句话提取信息并返回相同的json格式:{q}"}]

#     )
#     print(response.choices[0].message.content)
