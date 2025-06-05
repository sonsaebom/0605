# OpenAI API를 직접 호출하고 응답을 받아오는 모듈

import openai
import config
import json

from dialog.prompt_state import pm
from emotion_mapper import map_emotion_name

# OpenAI API 키 설정
openai.api_key = config.OPENAI_API_KEY

# 감정 유효성 확인 함수
# 감정 값 "angrryy" 같은 오탈자 응답 대비
def validate_emotion(emotion):
    return emotion if emotion in config.EMOTION_GROUPS else config.DEFAULT_EMOTION

# 금지어 필터링 함수 (GPT 응답에서 금지어 포함 여부 확인)
def contains_forbidden_words(response_text):
    return any(word in response_text for word in config.FORBIDDEN_WORDS)

# ChatGPT에 요청하고 응답을 받아오는 함수
def get_chatgpt_response(user_input):
    try:
        messages = pm.generate_prompt({"user_input": user_input})

        response = openai.ChatCompletion.create(
            model=config.MODEL_NAME,
            messages=messages,
            temperature=config.TEMPERATURE,
            max_tokens=config.MAX_TOKENS,
            timeout=config.TIMEOUT_SECONDS
        )

        content = response['choices'][0]['message']['content'].strip()

        try:
            parsed = json.loads(content)
            raw_emotion = parsed.get("emotion", "").strip().lower()
            mapped_emotion = map_emotion_name(raw_emotion)

            text = parsed.get("response", "죄송해요, 응답 파싱에 실패했어요.")

            if contains_forbidden_words(text):
                print("🚫 금지어 포함됨 → 필터링 응답 반환")
                return {
                    "text": "죄송해요, 적절하지 않은 표현이 포함되어 응답을 수정 중이에요.",
                    "emotion": config.DEFAULT_EMOTION
                }

            return {
                "response": text,
                "emotion": mapped_emotion
            }

        except json.JSONDecodeError:
            print("⚠️ JSON 파싱 실패:", content)
            return {
                "text": "죄송해요, 응답 처리 중 오류가 발생했어요.",
                "emotion": config.DEFAULT_EMOTION,
                "error_type": "parse_error"
            }

    except Exception as e:
        print(f"❌ ChatGPT API 오류 : {e}")
        return {
            "text": "죄송해요, 네트워크 상의 문제가 발생했어요.",
            "emotion": config.DEFAULT_EMOTION,
            "error_type": "api_error"
        }

