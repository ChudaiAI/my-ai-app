import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="我的AI产品", page_icon="🤖")
st.title("🤖 我的第一个AI产品")
st.caption("基于 DeepSeek 大模型开发")

client = OpenAI(
    api_key=st.secrets["DEEPSEEK_API_KEY"],# ⚠️ 替换成真实的 Key
    base_url="https://api.deepseek.com"
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你是一个有用的AI助手"}
    ]

with st.sidebar:
    st.header("设置")
    if st.button("清空对话"):
        st.session_state.messages = [
            {"role": "system", "content": "你是一个有用的AI助手"}
        ]
        st.rerun()

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if prompt := st.chat_input("请输入你的问题..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
     # 1. 开启流式输出 (stream=True)
     stream = client.chat.completions.create(
         model="deepseek-chat",
         messages=st.session_state.messages,
         stream=True
     )
     
     # 2. 定义一个提取器，把流式内容逐个字拿出来
     def stream_generator():
         for chunk in stream:
             if chunk.choices[0].delta.content is not None:
                 yield chunk.choices[0].delta.content
     
     # 3. st.write_stream 会边接收边在网页上渲染，并返回完整文本
     ai_reply = st.write_stream(stream_generator())
 
 # 4. 流式输出结束后，把完整的回复存入历史记录
 st.session_state.messages.append({"role": "assistant", "content": ai_reply})
