import streamlit as st
import pandas as pd

# タイトル
st.title("スケジュール管理アプリ")

# タスクデータを保存するためのデータフレーム
if "tasks" not in st.session_state:
    st.session_state["tasks"] = pd.DataFrame(columns=["日付", "時間", "タスク"])

# タスク追加フォーム
st.header("タスクを追加")
with st.form("task_form"):
    task_date = st.date_input("日付を選択")
    task_time = st.time_input("時間を選択")
    task_name = st.text_input("タスク名を入力")
    submitted = st.form_submit_button("追加")

    if submitted:
        if task_name:
            new_task = pd.DataFrame({"日付": [task_date], "時間": [task_time], "タスク": [task_name]})
            st.session_state["tasks"] = pd.concat([st.session_state["tasks"], new_task], ignore_index=True)
            st.success("タスクが追加されました！")
        else:
            st.error("タスク名を入力してください。")

# スケジュール表示と削除機能
st.header("スケジュール一覧と削除")
if not st.session_state["tasks"].empty:
    # スケジュール一覧を表示
    st.dataframe(st.session_state["tasks"])

    # 削除機能
    task_to_delete = st.selectbox("削除するタスクを選択", st.session_state["tasks"]["タスク"])
    if st.button("削除"):
        st.session_state["tasks"] = st.session_state["tasks"][st.session_state["tasks"]["タスク"] != task_to_delete]
        st.success(f"タスク '{task_to_delete}' が削除されました！")
else:
    st.write("現在、スケジュールはありません。")
