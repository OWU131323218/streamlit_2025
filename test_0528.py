import streamlit as st

st.title("🧠 性格診断アプリ")

questions = [
    "1. 新しいことに挑戦するのが好きだ",
    "2. 友達と過ごすのが好きだ",
    "3. 計画を立てて行動する方だ",
    "4. 落ち着いて物事を考えることが多い",
    "5. 人の気持ちに敏感だ",
    "6. 物事を最後までやり遂げるタイプだ",
    "7. 失敗してもすぐに立ち直る方だ",
    "8. 細かいことに気がつく方だ",
    "9. みんなをまとめるのが得意だ",
    "10. 一人の時間も大切にしたい"
]

choices = ["あてはまる", "ややあてはまる", "どちらともいえない", "あまりあてはまらない", "あてはまらない"]

if "answers" not in st.session_state:
    st.session_state.answers = [2] * 10  # デフォルトは真ん中

with st.form("personality_test"):
    st.write("各設問に答えてください。")
    for i, q in enumerate(questions):
        st.session_state.answers[i] = choices.index(
            st.radio(q, choices, index=st.session_state.answers[i], key=f"q{i}")
        )
    submitted = st.form_submit_button("診断する")

if submitted:
    score = sum(st.session_state.answers)
    # 診断結果
    if score <= 10:
        result = "【チャレンジャータイプ】\n新しいことに積極的に挑戦する行動派です！"
    elif score <= 17:
        result = "【ムードメーカータイプ】\n周囲を明るくする人気者タイプです！"
    elif score <= 24:
        result = "【バランスタイプ】\n冷静さと積極性のバランスが取れています。"
    elif score <= 32:
        result = "【サポータータイプ】\n人の気持ちに寄り添い、支えるのが得意です。"
    else:
        result = "【マイペースタイプ】\n自分のペースを大切にする落ち着いた性格です。"
    st.header("診断結果
