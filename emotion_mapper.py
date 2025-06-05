import re
import config

def clean_emotion_string(raw_emotion):
    # 조사, 종결어미 등 제거
    emotion = re.sub(r"(입니다|이에요|예요|같아요|같은|같은데|네요|입니다요|같은거)", "", raw_emotion)
    emotion = re.sub(r"[^\uAC00-\uD7A3]+", "", emotion)  # 한글만 남김
    return emotion.strip()

def map_emotion_name(raw_emotion):
    cleaned = clean_emotion_string(raw_emotion)

    for emotion_code, synonyms in config.EMOTION_GROUPS.items():
        for word in synonyms:
            if word in cleaned:
                return emotion_code

    return config.DEFAULT_EMOTION

