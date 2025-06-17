import streamlit as st
from datetime import datetime, timedelta
from collections import defaultdict

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
st.subheader("📅 カレンダー表示 ToDoリスト")

if not st.session_state.todo_list:
    st.info("まだタスクがありません。新しいタスクを追加してみましょう！")
else:
    # タスクを日付ごとにまとめる
    tasks_by_date = defaultdict(list)
    for i, item in enumerate(st.session_state.todo_list):
        tasks_by_date[item["date"]].append((i, item))

    # 今月のカレンダーを作成
    today = datetime.now().date()
    first_day = today.replace(day=1)
    last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    start_weekday = first_day.weekday()  # 月曜=0
    days_in_month = last_day.day

    # カレンダーのヘッダー
    st.markdown(
        "<style>th,td{padding:4px 8px;text-align:center;} .done{color:#aaa;text-decoration:line-through;}</style>",
        unsafe_allow_html=True
    )
    st.markdown(f"#### {today.strftime('%Y年%m月')}")
    calendar_html = "<table><tr>"
    for wd in ["月", "火", "水", "木", "金", "土", "日"]:
        calendar_html += f"<th>{wd}</th>"
    calendar_html += "</tr><tr>"

    # 空白セル
    for _ in range(start_weekday):
        calendar_html += "<td></td>"

    # 日付セル
    for day in range(1, days_in_month + 1):
        date_str = first_day.replace(day=day).strftime("%Y-%m-%d")
        cell_content = f"<b>{day}</b>"
        # タスクがあれば表示
        if date_str in tasks_by_date:
            for idx, item in tasks_by_date[date_str]:
                style = "done" if item["done"] else ""
                cell_content += f"<br><span class='{style}'>[{item['time']}] {item['task']}</span>"
        calendar_html += f"<td>{cell_content}</td>"
        # 日曜で改行
        if (start_weekday + day) % 7 == 0:
            calendar_html += "</tr><tr>"
    # 残りの空白セル
    remain = (start_weekday + days_in_month) % 7
    if remain != 0:
        for _ in range(7 - remain):
            calendar_html += "<td></td>"
    calendar_html += "</tr></table>"

    st.markdown(calendar_html, unsafe_allow_html=True)

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
