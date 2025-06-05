import pygame
import time
import sys
from PIL import Image
from config import load_fonts, BLACK, EMOTION_GIF_PATHS


# GIF 파일을 프레임 단위로 로딩하여 반환 (애니메이션 재생용)
def _load_gif_frames(path):
    try:
        gif = Image.open(path)
    except Exception as e:
        print(f"❌ GIF 파일 로딩 실패: {path}, 에러: {e}")
        return [], []

    frames, durations = [], []
    try:
        while True:
            frame = gif.copy().convert("RGBA")
            img = pygame.image.fromstring(frame.tobytes(), frame.size, "RGBA")
            frames.append(pygame.transform.scale(img, (800, 480)))
            durations.append(max(gif.info.get('duration', 100), 50) / 1000)  # 최소 50ms
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    return frames, durations


# 감정에 따라 지정된 GIF 애니메이션을 재생하는 함수
def draw_face_screen(screen, emotion, duration=None, stop_flag=None):
    pygame.display.set_caption(f"Emotion: {emotion}")
    frames, durations = _load_gif_frames(EMOTION_GIF_PATHS.get(emotion, EMOTION_GIF_PATHS["basic"]))

    if not frames:
        print("⚠️ 프레임이 없어 감정 화면을 출력할 수 없습니다.")
        return

    idx = 0
    last_time = time.time()
    start_time = time.time()
    clock = pygame.time.Clock()

    # 안전 장치: duration과 stop_flag가 모두 없으면 무한 루프 위험
    if duration is None and stop_flag is None:
        print("⚠️ duration과 stop_flag가 모두 None이면 무한 루프에 빠질 수 있습니다.")
        return

    while True:
        now = time.time()

        # 종료 조건
        if duration and (now - start_time >= duration):
            break
        if stop_flag and stop_flag.is_set():
            break

        # 프레임 변경
        if now - last_time > durations[idx]:
            idx = (idx + 1) % len(frames)
            last_time = now

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 화면에 현재 프레임 출력
        screen.fill(BLACK)
        screen.blit(frames[idx], (0, 0))
        pygame.display.flip()
        clock.tick(30)


