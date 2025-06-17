import streamlit as st
import datetime

st.title("📅 スケジュール管理アプリ")

# セッションステートで予定リストを管理
if "schedules" not in st.session_state:
    st.session_state.schedules = []

# 予定の追加フォーム
with st.form("add_schedule"):
    date = st.date_input("日付", datetime.date.today())
    time = st.time_input("時間", datetime.time(9, 0))
    title = st.text_input("タイトル")
    submitted = st.form_submit_button("追加")
    if submitted and title:
        st.session_state.schedules.append({
            "date": date,
            "time": time,
            "title": title
        })
        st.success("予定を追加しました！")

# 予定の表示と削除
st.subheader("予定一覧")
if st.session_state.schedules:
    # 日付・時間順にソート
    schedules = sorted(
        enumerate(st.session_state.schedules),
        key=lambda x: (x[1]["date"], x[1]["time"])
    )
    for idx, schedule in schedules:
        col1, col2 = st.columns([5, 1])
        with col1:
            st.write(f'{schedule["date"]} {schedule["time"].strftime("%H:%M")} - {schedule["title"]}')
        with col2:
            if st.button("削除", key=f"delete_{idx}"):
                st.session_state.schedules.pop(idx)
                st.experimental_rerun()
else:
    st.write("予定はありません。")
