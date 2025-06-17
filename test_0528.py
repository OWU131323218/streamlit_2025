import streamlit as st

st.title("📝 クイズゲーム")

questions = [
    {
        "q": "日本の首都はどこ？",
        "a": ["大阪", "東京", "名古屋", "札幌"],
        "correct": 1
    },
    {
        "q": "地球は何番目の惑星？（太陽から数えて）",
        "a": ["2番目", "3番目", "4番目", "5番目"],
        "correct": 1
    },
    {
        "q": "パイ（π）の値に最も近いのは？",
        "a": ["2.14", "3.14", "4.13", "1.34"],
        "correct": 1
    },
    {
        "q": "イギリスの公用語は？",
        "a": ["英語", "フランス語", "ドイツ語", "スペイン語"],
        "correct": 0
    },
    {
        "q": "富士山の標高は約？",
        "a": ["2,776m", "3,776m", "4,776m", "1,776m"],
        "correct": 1
    }
]

if "answers" not in st.session_state:
    st.session_state.answers = [None] * len(questions)
if "submitted" not in st.session_state:
    st.session_state.submitted = False

with st.form("quiz_form"):
    for i, q in enumerate(questions):
        st.session_state.answers[i] = st.radio(q["q"], q["a"], index=st.session_state.answers[i] if st.session_state.answers[i] is not None else 0, key=f"q{i}")
    submitted = st.form_submit_button("採点する")
    if submitted:
        st.session_state.submitted = True

if st.session_state.submitted:
    score = 0
    for i, q in enumerate(questions):
        if q["a"].index(st.session_state.answers[i]) == q["correct"]:
            score += 1
    st.header(f"あなたのスコア: {score} / {len(questions)}")
    if score == len(questions):
        st.success("全問正解！すごい！")
    elif score >= len(questions) // 2:
        st.info("なかなか良い成績です！")
    else:
        st.warning("もう一度チャレンジしてみよう！")
