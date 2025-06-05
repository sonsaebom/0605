import speech_recognition as sr
from config import STT_CONFIG


def recognize_speech():
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = STT_CONFIG["pause_threshold"]

    # 버튼으로 마이크 시작
    with sr.Microphone() as source:
        print("인식 중... 다시 키 누르면 종료")
        recognizer.adjust_for_ambient_noise(source, duration=STT_CONFIG["ambient_noise_duration"])

        try:
            audio = recognizer.listen(
                source, timeout=30      # 말 안 하면 30초까지 기다림
            )
        except sr.WaitTimeoutError:
            print("❌ 무음 상태로 인해 자동 종료")
            return None

    try:
        text = recognizer.recognize_google(audio, language=STT_CONFIG["language"])
        print("인식된 텍스트:", text)
        return text

    except sr.UnknownValueError:
        print("❗ 음성을 인식할 수 없습니다.")
        return None

    except sr.RequestError:
        print("❗ STT 서버에 연결할 수 없습니다. 인터넷 상태를 확인하세요.")
        return None

