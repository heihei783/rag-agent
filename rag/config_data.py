md5_path = "./md5.text"

#Chroma
collection_name="rag"
persist_directory="./chroma_db"


#spliter
chunk_size=1000
chunk_overlap=100
separators=["\m\n","\n",",",".","!","?"," 。","、"]
max_split_char_number = 1000


similarity_threshold=2

embedding_model_name = "text-embedding-v4"
chat_model_name = "abab6.5-chat"
base_url="https://api.minimax.chat/v1"

session_config = {
        "configurable":{
            "session_id":"user_001",
        }
    } 