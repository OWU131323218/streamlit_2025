import streamlit as st
import pandas as pd

# タイトル
st.title("🗓️ スケジュール管理アプリ")

# タスクデータを保存するためのデータフレーム
if "tasks" not in st.session_state:
    st.session_state["tasks"] = pd.DataFrame(columns=["日付", "タスク"])

# タスク追加フォーム
st.header("➕ タスクを追加")
with st.form("task_form"):
    task_date = st.date_input("📅 日付を選択")
    task_name = st.text_input("✏️ タスク名を入力")
    submitted = st.form_submit_button("追加")

    if submitted:
        if task_name:
            new_task = pd.DataFrame({"日付": [task_date], "タスク": [task_name]})
            st.session_state["tasks"] = pd.concat([st.session_state["tasks"], new_task], ignore_index=True)
            st.success("✅ タスクが追加されました！")
        else:
            st.error("⚠️ タスク名を入力してください。")

# スケジュール表示と削除機能
st.header("📋 スケジュール一覧")
if not st.session_state["tasks"].empty:
    for index, row in st.session_state["tasks"].iterrows():
        with st.container():
            st.markdown(
                f"""
                <div style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; margin-bottom: 10px; background-color: #f9f9f9;">
                    <p><strong>📅 日付:</strong> {row["日付"]}</p>
                    <p><strong>✏️ タスク:</strong> {row["タスク"]}</p>
                    <form action="" method="post">
                        <button style="background-color: #ff4b4b; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;" onclick="window.location.reload()">削除</button>
                    </form>
                </div>
                """,
                unsafe_allow_html=True,
            )
else:
    st.write("現在、スケジュールはありません。")
