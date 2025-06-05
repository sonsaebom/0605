from yeelight import Bulb
from config import BULB_IP_ADDRESS, EMOTION_LIGHT_SETTINGS

# 전역 전구 인스턴스
bulb = Bulb(BULB_IP_ADDRESS)

# 전구 켜기 함수 (필요 시)
def turn_on_light():
    try:
        bulb.turn_on()
    except Exception as e:
        print(f"⚠️ 전구 켜기 실패: {e}")

# 전구 끄기 함수 (필요 시)
def turn_off_light():
    try:
        bulb.turn_off()
    except Exception as e:
        print(f"⚠️ 전구 끄기 실패: {e}")

# 감정에 따라 조명 설정
def set_emotion_light(emotion):
    setting = EMOTION_LIGHT_SETTINGS.get(emotion, EMOTION_LIGHT_SETTINGS["default"])
    try:
        bulb.set_rgb(*setting["rgb"])
        bulb.set_brightness(setting["brightness"])
    except Exception as e:
        print(f"⚠️ 조명 설정 실패 ({emotion}): {e}")


