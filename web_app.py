import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="我的AI产品", page_icon="🤖")
st.title("🤖 我的第一个AI产品")
st.caption("基于 DeepSeek 大模型开发")

client = OpenAI(
    api_key=api_key=st.secrets["DEEPSEEK_API_KEY"],# ⚠️ 替换成真实的 Key
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
        with st.spinner("思考中..."):
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=st.session_state.messages
            )
            ai_reply = response.choices[0].message.content
            st.markdown(ai_reply)

    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
