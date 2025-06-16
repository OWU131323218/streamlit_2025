import streamlit as st
import pandas as pd

# タイトル
st.title("スケジュール管理アプリ")

# タスクデータを保存するためのデータフレーム
if "tasks" not in st.session_state:
    st.session_state["tasks"] = pd.DataFrame(columns=["日付", "タスク"])

# タスク追加フォーム
st.header("タスクを追加")
with st.form("task_form"):
    task_date = st.date_input("日付を選択")
    task_name = st.text_input("タスク名を入力")
    submitted = st.form_submit_button("追加")

    if submitted:
        if task_name:
            new_task = pd.DataFrame({"日付": [task_date], "タスク": [task_name]})
            st.session_state["tasks"] = pd.concat([st.session_state["tasks"], new_task], ignore_index=True)
            st.success("タスクが追加されました！")
        else:
            st.error("タスク名を入力してください。")

# スケジュール表示
st.header("スケジュール一覧")
if not st.session_state["tasks"].empty:
    for index, row in st.session_state["tasks"].iterrows():
        with st.container():
            col1, col2, col3 = st.columns([2, 4, 1])
            col1.write(row["日付"])
            col2.write(row["タスク"])
            if col3.button("削除", key=f"delete_{index}"):
                st.session_state["tasks"] = st.session_state["tasks"].drop(index).reset_index(drop=True)
                st.success(f"タスク '{row['タスク']}' が削除されました！")
else:
    st.write("現在、スケジュールはありません。")
