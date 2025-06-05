import pygame
import json
import os
import time
import sys

from ui.voice_select import run_voice_select
from ui.face_display import _load_gif_frames, draw_face_screen
from config import EMOTION_PATH

def get_emotion():
    if os.path.exists(EMOTION_PATH):
        with open(EMOTION_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("emotion", "unknown")
    return "unknown"

def clear_emotion():
    with open(EMOTION_PATH, "w", encoding="utf-8") as f:
        json.dump({"emotion": "unknown"}, f)

def show_idle(screen):
    # 최초 한 번만 리소스 로딩
    if not hasattr(show_idle, "initialized"):
        show_idle.frames, show_idle.durations = _load_gif_frames("image/default.gif")
        show_idle.idx = 0
        show_idle.last_frame_time = time.time()
        show_idle.voice_icon = pygame.transform.scale(pygame.image.load("image/voice_setting.png"), (60, 60))
        show_idle.stats_icon = pygame.transform.scale(pygame.image.load("image/stats_ui.png"), (60, 60))
        show_idle.voice_rect = pygame.Rect(650, 400, 60, 60)
        show_idle.stats_rect = pygame.Rect(720, 400, 60, 60)
        show_idle.last_emotion_check = time.time()
        show_idle.initialized = True

    now = time.time()

    # 애니메이션 프레임 업데이트
    if now - show_idle.last_frame_time > show_idle.durations[show_idle.idx]:
        show_idle.idx = (show_idle.idx + 1) % len(show_idle.frames)
        show_idle.last_frame_time = now

    # 화면 초기화 + 기본 표정 출력
    screen.fill((0, 0, 0))  # 배경색 (선택)
    screen.blit(show_idle.frames[show_idle.idx], (0, 0))

    # 버튼 아이콘 출력
    screen.blit(show_idle.voice_icon, show_idle.voice_rect.topleft)
    screen.blit(show_idle.stats_icon, show_idle.stats_rect.topleft)

    # 감정 출력 요청이 있는 경우 처리
    if now - show_idle.last_emotion_check > 1:
        emotion = get_emotion()
        if emotion != "unknown":
            draw_face_screen(screen, emotion, duration=3)
            clear_emotion()
        show_idle.last_emotion_check = now

    # 클릭 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 목소리 선택
            if show_idle.voice_rect.collidepoint(event.pos):
                run_voice_select(screen)
                return "base"
            # 통계
            elif show_idle.stats_rect.collidepoint(event.pos):
                return "stats"

    return None



