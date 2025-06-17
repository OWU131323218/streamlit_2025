import streamlit as st
from datetime import datetime

st.title("スケジュール管理アプリ")


# ToDoリストの初期化
if "todo_list" not in st.session_state:
    st.session_state.todo_list = []

# 予定追加機能
st.subheader("新しい予定を追加")
new_task = st.text_input("予定を入力してください", placeholder="例: ショッピング")
new_task_memo = st.text_area("予定のメモ（任意）", placeholder="例: 持ち物や集合場所など")

col_date, col_time = st.columns(2)
with col_date:
    task_date = st.date_input("日付を選択", value=datetime.now().date())
with col_time:
    task_time_str = st.text_input("時間を入力（例: 14:30）", value=datetime.now().strftime("%H:%M"))

if st.button("予定を追加"):
    if not new_task:
        st.error("予定を入力してください")
    else:
        try:
            datetime.strptime(task_time_str, "%H:%M")
            st.session_state.todo_list.append({
                "task": new_task,
                "memo": new_task_memo,
                "done": False,
                "date": task_date.strftime("%Y-%m-%d"),
                "time": task_time_str
            })
            st.success(f"「{new_task}」を追加しました！")
            st.rerun()
        except ValueError:
            st.error("時間は「HH:MM」形式で入力してください")

# 予定リスト表示
st.subheader("📝 予定一覧")

if not st.session_state.todo_list:
    st.info("まだ予定がありません。新しい予定を追加してみましょう！")
else:
    total_tasks = len(st.session_state.todo_list)
    completed_tasks = sum(1 for item in st.session_state.todo_list if item["done"])
    st.write(f"**予定数**: {total_tasks} 件 | **完了**: {completed_tasks} 件 | **残り**: {total_tasks - completed_tasks} 件")
    for i, item in enumerate(st.session_state.todo_list):
        col1, col2, col3 = st.columns([4, 2, 1])
        with col1:
            is_done = st.checkbox(
                item["task"], 
                value=item["done"], 
                key=f"checkbox_{i}"
            )
            if is_done != item["done"]:
                st.session_state.todo_list[i]["done"] = is_done
                st.rerun()
            # メモがあれば表示
            if item.get("memo"):
                st.markdown(f"<span style='color: #888;'>📝 {item['memo']}</span>", unsafe_allow_html=True)
        with col2:
            st.write(f"📅 {item.get('date', '')} ⏰ {item.get('time', '')}")
        with col3:
            if st.button("🗑️ 削除", key=f"delete_{i}"):
                st.session_state.todo_list.pop(i)
                st.success("予定を削除しました")
                st.rerun()

# 一括操作
if st.session_state.todo_list:
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("全て完了にする"):
            for item in st.session_state.todo_list:
                item["done"] = True
            st.success("全ての予定を完了にしました！")
            st.rerun()
    with col2:
        if st.button("完了済み予定を削除"):
            st.session_state.todo_list = [item for item in st.session_state.todo_list if not item["done"]]
            st.success("完了済み予定を削除しました")
            st.rerun()
