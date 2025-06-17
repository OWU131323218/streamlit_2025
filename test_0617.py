import streamlit as st
import random
import datetime

st.title("🌟 星座占いゲーム 🌟")

# 星座判定関数
def get_zodiac(month, day):
    zodiac_dates = [
        ((3,21), (4,19), "おひつじ座"),
        ((4,20), (5,20), "おうし座"),
        ((5,21), (6,21), "ふたご座"),
        ((6,22), (7,22), "かに座"),
        ((7,23), (8,22), "しし座"),
        ((8,23), (9,22), "おとめ座"),
        ((9,23), (10,23), "てんびん座"),
        ((10,24), (11,22), "さそり座"),
        ((11,23), (12,21), "いて座"),
        ((12,22), (1,19), "やぎ座"),
        ((1,20), (2,18), "みずがめ座"),
        ((2,19), (3,20), "うお座"),
    ]
    for start, end, sign in zodiac_dates:
        if (month == start[0] and day >= start[1]) or (month == end[0] and day <= end[1]):
            return sign
    return "不明"

# 今日の日付
today = datetime.date.today()
st.write(f"今日は {today.strftime('%Y年%m月%d日')} です。あなたの運勢を占いましょう！")

# 誕生日入力
birthday = st.date_input("あなたの誕生日を入力してください")
if birthday:
    zodiac = get_zodiac(birthday.month, birthday.day)
    st.write(f"あなたの星座は「{zodiac}」です。")
else:
    zodiac = None

# 占い結果を日付と星座で固定
def get_daily_fortune(zodiac, date):
    if zodiac is None or zodiac == "不明":
        return None, None
    fortunes = [
        "大吉！最高の一日になりそう！",
        "中吉。良いことがあるかも！",
        "小吉。ちょっとした幸運があるかも。",
        "吉。平和な一日になりそう。",
        "末吉。焦らずゆっくり進もう。",
        "凶。無理せず休むのも大事。",
        "大凶…でも前向きにいこう！"
    ]
    advice = [
        "ラッキーアイテム：青いペン",
        "ラッキーカラー：黄色",
        "ラッキーナンバー：7",
        "友達と話すと運気UP！",
        "新しいことに挑戦してみて",
        "甘いものを食べると吉",
        "散歩するとリフレッシュできそう"
    ]
    # 日付と星座でシードを固定
    seed = hash(zodiac + date.strftime("%Y%m%d"))
    random.seed(seed)
    result = random.choice(fortunes)
    adv = random.choice(advice)
    return result, adv

if zodiac and zodiac != "不明":
    if st.button("占う！"):
        result, adv = get_daily_fortune(zodiac, today)
        st.subheader(f"{zodiac} の今日の運勢")
        st.success(result)
