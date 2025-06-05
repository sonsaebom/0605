from evdev import InputDevice, ecodes, list_devices
import time
import select
import sys
import config

dev = None  # 전역 변수로 선언

# 블루투스 장치 이름으로 이벤트 디바이스 탐색
def find_dev(name):
    global dev
    for path in list_devices():
        try:
            dev = InputDevice(path)
            if dev.name == name:
                return dev
        except OSError:
            continue
    return None

# 버튼 이벤트 버퍼 비우기
def clear_buffer():
    if dev:
        while dev.read_one() is not None:
            pass

# 버튼 상태 감지 및 콜백 실행
def button(on, off):
    dev = find_dev(config.BUTTON_DEVICE_NAME)
    if dev is None:
        print("❌ 블루투스 버튼 장치 탐색 실패")
        sys.exit(1)
    else:
        print("✅ 블루투스 버튼 연결 성공")

    state = False  # False: 대기, True: 듣기 상태
    last_event_time = 0

    while True:
        r, _, _ = select.select([dev], [], [])
        for _ in r:
            try:
                event = dev.read_one()
            except OSError:
                print("❌ 장치 오류: 연결 끊김 또는 제거됨")
                sys.exit(1)

            if event and event.type == ecodes.EV_KEY and event.code == ecodes.KEY_VOLUMEUP and event.value == 1:
                now = time.time()
                if now - last_event_time < config.BUTTON_DEBOUNCE_DELAY:
                    continue
                last_event_time = now

                state = not state  # 토글
                if state:
                    on()
                else:
                    off()


