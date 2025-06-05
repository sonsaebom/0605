import pygame

from ui.base_screen import show_idle, get_emotion, clear_emotion
from ui.stats_ui import run_stats_screen
from ui.voice_select import run_voice_select
from ui.face_display import draw_face_screen
from hardware.led_control import set_emotion_light


def run_screen_manager():
    pygame.init()
    screen = pygame.display.set_mode((800, 480))
    pygame.display.set_caption("Emotion UI")
    clock = pygame.time.Clock()

    current_screen = "base"
    last_emotion = "unknown"

    while True:
        # 1. 감정 감지 우선 처리
        emotion = get_emotion()
        if emotion != "unknown" and emotion != last_emotion:
            set_emotion_light(emotion)
            draw_face_screen(screen, emotion, duration=3)  # 감정 표정 출력
            clear_emotion()
            last_emotion = emotion
            current_screen = "base"

        # 2. 화면 전환
        if current_screen == "base":
            result = show_idle(screen)
        elif current_screen == "stats":
            result = run_stats_screen()
        elif current_screen == "voice":
            result = run_voice_select(screen)
        else:
            break  # 알 수 없는 화면 → 종료

        # 3. 다음 화면 상태 업데이트
        if result in ["base", "stats", "voice", "setting"]:
            current_screen = result
        else:
            break

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()






