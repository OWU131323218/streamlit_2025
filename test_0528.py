import streamlit as st
import streamlit_calendar as st_calendar
from datetime import datetime, date

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
    task_date = st.date_input("日付を選択", value=date.today())
with col_time:
    task_time = st.text_input("時間を入力（例: 14:30）", value=datetime.now().strftime("%H:%M"))

if st.button("タスクを追加"):
    if not new_task:
        st.error("タスクを入力してください")
    else:
        try:
            # 時間の形式チェック
            datetime.strptime(task_time, "%H:%M")
            st.session_state.todo_list.append({
                "task": new_task,
                "done": False,
                "date": task_date.strftime("%Y-%m-%d"),
                "time": task_time
            })
            st.success(f"「{new_task}」を追加しました！")
            st.rerun()
        except ValueError:
            st.error("時間は「HH:MM」形式で入力してください")

# カレンダー表示
st.subheader("📅 カレンダー表示 ToDoリスト")

# ToDoリストをカレンダーイベント形式に変換
events = []
for i, item in enumerate(st.session_state.todo_list):
    # 日付と時間を結合してISO形式に
    start_str = f"{item['date']}T{item['time']}:00"
    events.append({
        "id": str(i),
        "title": ("✅ " if item["done"] else "") + item["task"],
        "start": start_str,
        "end": start_str,
        "allDay": False,
        "color": "#95a5a6" if item["done"] else "#3498db"
    })

calendar_options = {
    "initialView": "dayGridMonth",
    "locale": "ja",
    "height": 600,
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay"
    }
}

calendar_events = {"events": events}

st_calendar.calendar(
    events=calendar_events,
    options=calendar_options,
    key="calendar"
)

# タスクの完了・削除操作
st.markdown("---")
st.write("### タスク操作")
for i, item in enumerate(st.session_state.todo_list):
    cols = st.columns([4, 2, 2, 1])
    with cols[0]:
        is_done = st.checkbox(
            f"{item['task']} ({item['date']} {item['time']})",
            value=item["done"],
            key=f"checkbox_{i}"
        )
        if is_done != item["done"]:
            st.session_state.todo_list[i]["done"] = is_done
            st.rerun()
    with cols[3]:
        if st.button("🗑️", key=f"delete_{i}"):
            st.session_state.todo_list.pop(i)
            st.success("タスクを削除しました")
            st.rerun()

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
