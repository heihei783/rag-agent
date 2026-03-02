import streamlit as st
from rag import RagService
import time
from config_data import session_config

st.title("智能客服")
st.divider()

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

if "message" not in st.session_state:
    st.session_state["message"]=[{"role":"assistant","content":"你好，有什么可以帮助你？"}]

for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])


prompt = st.chat_input()

if prompt:

    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role":"user","content":prompt})


    with st.spinner("正在思考中...."):                                                                                    
        res_stream=st.session_state["rag"].chain.stream({"input":prompt},session_config)
        full_response=st.chat_message("assistant").write_stream(res_stream)
        st.session_state["message"].append({"role":"assistant","content":full_response})