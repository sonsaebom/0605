import os
import json
import pandas as pd
from datetime import datetime, timedelta
from config import EMOTION_PATH, CSV_LOG_PATH

def append_emotion_to_csv():
    # JSON 읽기
    if not os.path.exists(EMOTION_PATH):
        print("❗ 감정 JSON 파일이 없습니다.")
        return

    with open(EMOTION_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    today = datetime.now().date()
    current_date_str = today.strftime("%Y-%m-%d")

    new_data = pd.DataFrame([{
        "date": current_date_str,
        "emotion": data.get("emotion", "unknown")
    }])

    # 기존 CSV 불러오기 or 새로 생성
    if os.path.exists(CSV_LOG_PATH):
        df = pd.read_csv(CSV_LOG_PATH)
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d", errors='coerce').dt.date
        df.dropna(subset=["date"], inplace=True)
    else:
        df = pd.DataFrame(columns=["date", "emotion"])

    # 7일 이상 지난 데이터 삭제
    cutoff_date = today - timedelta(days=6)
    df = df[df["date"] >= cutoff_date]

    # 새 데이터 추가 후 저장
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(CSV_LOG_PATH, index=False, encoding="utf-8-sig")
    print(f"✅ 감정 기록이 {CSV_LOG_PATH}에 저장되었습니다.")

