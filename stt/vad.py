import speech_recognition as sr
from config import VAD_CONFIG

def listen_with_vad(recognizer=None):

    if recognizer is None:
        recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("말할 때까지 대기 중... (무음 시 종료)")

        # 중요한 설정 부분이라 config에서 값을 정의했지만, 이 파일에서도 값을 명시하는 것.
        recognizer.adjust_for_ambient_noise(source, duration=VAD_CONFIG.get("adjust_noise_duration", 1.0))

        try:
            audio = recognizer.listen(
                source,
                timeout=VAD_CONFIG["timeout"],
                phrase_time_limit=VAD_CONFIG["phrase_time_limit"]
            )
            return audio

        except sr.WaitTimeoutError:
            print("아무 말도 안 해서 자동 종료")
            return None


