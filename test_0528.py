import streamlit as st
import random
import time

st.title("⌨️ タイピングゲーム")

# お題リスト
words = [
    "algorithm", "python", "streamlit", "computer", "keyboard",
    "university", "schedule", "visualization", "function", "variable"
]

if "current_word" not in st.session_state:
    st.session_state.current_word = random.choice(words)
    st.session_state.start_time = None
    st.session_state.input_text = ""
    st.session_state.result = ""
    st.session_state.finished = False

def reset_game():
    st.session_state.current_word = random.choice(words)
    st.session_state.start_time = None
    st.session_state.input_text = ""
    st.session_state.result = ""
    st.session_state.finished = False

if st.button("リセット"):
    reset_game()

st.subheader("次の英単語を入力してください：")
st.markdown(f"## {st.session_state.current_word}")

if not st.session_state.start_time:
    if st.button("スタート"):
        st.session_state.start_time = time.time()
else:
    st.session_state.input_text = st.text_input("ここに入力", value=st.session_state.input_text)
    if st.session_state.input_text == st.session_state.current_word and not st.session_state.finished:
        elapsed = time.time() - st.session_state.start_time
        st.session_state.result = f"クリア！タイム：{elapsed:.2f}秒"
        st.session_state.finished = True

if st.session_state.result:
    st.success(st.session_state.result)
    if st.button("もう一度挑戦"):
        reset_game()
