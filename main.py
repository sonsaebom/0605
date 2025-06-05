import ctypes


import pygame
import atexit
from threading import Thread, Event

import config

from stt.stt import recognize_speech                                # STT
from tts.tts import generate_tts_audio                              # TTS

from dialog.chatgpt_client import get_chatgpt_response              # GPT

from ui.face_display import draw_face_screen                        # UI
from ui.stats_ui import run_stats_screen
from ui.base_screen import show_idle

from hardware.motor import motor_control                            # motor
from hardware.led_control import set_emotion_light                  # light
from hardware.button import button, clear_buffer                    # button





# 버튼 1번 누름 → 음성 인식 시작 + 모터 ON + "듣는 중" 화면 표시
# 버튼 2번 누름 → 음성 인식 종료 + 모터 OFF → GPT 분석 → 감정 분석 결과 기반 화면 출력 + TTS 재생





# 상태 및 전역 변수
current_state = "idle"                  # 초기 상태: 대기
current_emotion = "basic"               # 기본 감정
emotion_duration = 3.0                  # 초깃값일 뿐 TTS 출력 길이만큼 출력되도록 코드 작성함
stop_flag = Event()                     # 듣기 중지 제어용 플래그
is_recording = False                    # STT 녹음 중 여부
user_input = None                       # 음성 인식 결과 텍스트 저장용


# 종료 시 리소스 정리 함수
def cleanup():
    print("시스템 종료 처리 중...")
    motor_control(False)                # 모터 정지
    set_emotion_light("off")            # 조명 OFF
    pygame.quit()                       # Pygame 종료

atexit.register(cleanup)                # 시스템 종료 시 자동 호출


def process_interaction(screen):
    global current_state, current_emotion, emotion_duration, user_input

    if not user_input:
        print("음성 인식 실패")
        current_state = "idle"
        return

    print("GPT 처리 중...")
    current_state = "processing"
    stop_flag.clear()

    gpt_result = get_chatgpt_response(user_input)
    stop_flag.set()

    if "error_type" in gpt_result:
        print("GPT 응답 오류:", gpt_result["text"])
        current_state = "idle"
        return

    response_text = gpt_result.get("response", "")
    emotion = gpt_result.get("emotion", "unknown")

    # fallback 처리
    current_emotion = emotion if emotion in config.EMOTION_GIF_PATHS else "basic"
    print(f"GPT 응답: {response_text}\n감정 코드: {current_emotion}")

    # 조명 및 TTS
    set_emotion_light(current_emotion)
    emotion_duration = max(generate_tts_audio(response_text), 1.0)

    current_state = "emotion"
    clear_buffer()  # TTS 종료 후 다음 입력을 위해 버퍼 비움


# 프로그램 메인 루프
def main():
    global current_state, is_recording, user_input

    pygame.init()
    screen = pygame.display.set_mode((800, 480))            # 디스플레이 설정
    pygame.display.set_caption("감정 공감 로봇")             # 창 제목
    clock = pygame.time.Clock()

    # 버튼 이벤트 연결: 버튼 눌렀을 때 (STT 시작/종료 제어)
    def on_button():
        nonlocal screen
        global is_recording, current_state, user_input

        if not is_recording:
            print("버튼 눌림 → 음성 인식 시작")
            is_recording = True
            current_state = "listening"
            stop_flag.clear()
            motor_control(True)
            user_input = None

            def record():
                global user_input
                user_input = recognize_speech()
            Thread(target=record, daemon=True).start()

        else:
            print("버튼 다시 눌림 → 음성 인식 종료")
            is_recording = False
            stop_flag.set()
            motor_control(False)
            Thread(target=process_interaction, args=(screen,), daemon=True).start()

    # 버튼 다시 눌렀을 때 (무시됨 - on_button에서 처리됨)
    def off_button():
        pass

    # 버튼 입력 스레드 시작
    Thread(target=button, args=(on_button, off_button), daemon=True).start()

    print("로봇이 실행되었습니다. 버튼을 누르어 음성을 입력하세요.")

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return      # 종료 신호 수신 → finally로 cleanup (수동 종료)

            # 상태별 화면 출력
            if current_state == "idle":
                result = show_idle(screen)
                if result == "stats":
                    run_stats_screen()
                elif result == "base":
                    current_state = "idle"      # 명시적으로 유지

            elif current_state == "listening":
                draw_face_screen(screen, "listening", stop_flag=stop_flag)

            elif current_state == "processing":
                draw_face_screen(screen, "processing", stop_flag=stop_flag)

            elif current_state == "emotion":
                draw_face_screen(screen, current_emotion, duration=emotion_duration)
                current_state = "idle"

            pygame.display.flip()
            clock.tick(30)      # 루프의 실행 속도: 화면 전환을 부드럽게 유지하기 위함 + CPU 과부하 방지 등..

    finally:
        cleanup()


if __name__ == "__main__":
    main()


