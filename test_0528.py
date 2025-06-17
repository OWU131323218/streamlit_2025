import streamlit as st
from datetime import datetime

st.title("第8回 演習: ToDoリストアプリ - 解答例")
st.caption("タスクの追加・完了チェック・削除ができるシンプルなToDoリストを作成しましょう。")

st.markdown("---")
st.subheader("演習: ToDoリスト")
st.write("**課題**: タスクの追加・完了チェック・削除ができるシンプルなToDoリストを作成する。")

# ToDoリストの初期化
if "todo_list" not in st.session_state:
    st.session_state.todo_list = []

# タスク追加機能
st.subheader("新しいタスクを追加")
new_task = st.text_input("タスクを入力してください", placeholder="例: レポートを書く")

col_date, col_time = st.columns(2)
with col_date:
    task_date = st.date_input("日付を選択", value=datetime.now().date())
with col_time:
    task_time_str = st.text_input("時間を入力（例: 14:30）", value=datetime.now().strftime("%H:%M"))

if st.button("タスクを追加"):
    if not new_task:
        st.error("タスクを入力してください")
    else:
        try:
            datetime.strptime(task_time_str, "%H:%M")
            st.session_state.todo_list.append({
                "task": new_task,
                "done": False,
                "date": task_date.strftime("%Y-%m-%d"),
                "time": task_time_str
            })
            st.success(f"「{new_task}」を追加しました！")
            st.rerun()
        except ValueError:
            st.error("時間は「HH:MM」形式で入力してください")

# カレンダー風ToDoリスト表示
st.subheader("📅 カレンダー風 ToDoリスト")

if not st.session_state.todo_list:
    st.info("まだタスクがありません。新しいタスクを追加してみましょう！")
else:
    # 日付ごとにタスクをまとめる
    from collections import defaultdict
    tasks_by_date = defaultdict(list)
    for i, item in enumerate(st.session_state.todo_list):
        tasks_by_date[item["date"]].append((i, item))

    # 日付順に表示
    for date in sorted(tasks_by_date.keys()):
        st.markdown(f"### <span style='color:#2c3e50'>📆 {date}</span>", unsafe_allow_html=True)
        for i, item in tasks_by_date[date]:
            cols = st.columns([1, 2, 4, 1])
            with cols[0]:
                is_done = st.checkbox(
                    "", 
                    value=item["done"], 
                    key=f"checkbox_{i}"
                )
                if is_done != item["done"]:
                    st.session_state.todo_list[i]["done"] = is_done
                    st.rerun()
            with cols[1]:
                st.markdown(f"<span style='color:#2980b9;font-weight:bold'>{item['time']}</span>", unsafe_allow_html=True)
            with cols[2]:
                task_style = "text-decoration: line-through; color: #888;" if item["done"] else ""
                st.markdown(f"<span style='{task_style}'>{item['task']}</span>", unsafe_allow_html=True)
            with cols[3]:
                if st.button("🗑️", key=f"delete_{i}"):
                    st.session_state.todo_list.pop(i)
                    st.success("タスクを削除しました")
                    st.rerun()
        st.markdown("---")

# 一括操作
if st.session_state.todo_list:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("全て完了にする"):
            for item in st.session_state.todo_list:
                item["done"] = True
            st.success("全てのタスクを完了にしました！")
            st.rerun()
    with col2:
        if st.button("完了済みタスクを削除"):
            st.session_state.todo_list = [item for item in st.session_state.todo_list if not item["done"]]
            st.success("完了済みタスクを削除しました")
            st.rerun()
