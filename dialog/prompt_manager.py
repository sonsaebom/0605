import random
import config

# 사용자 입력과 감정 정보를 기반으로 GPT에게 전달할 메시지를 구성하는 클래스
class PromptManager:
    def __init__(self):
        self.conversation_history = []      # 이전 사용자-모델 대화 메시지 저장 (시스템 메시지 제외)
        self.last_insert = None             # 마지막으로 사용된 무작위 삽입 템플릿 (중복 방지를 위해)

    # 사용자 입력을 기반으로 GPT에게 전달할 메시지 리스트 생성
    def generate_prompt(self, input_json):
        # 입력 값 추출
        try:
            user_input = input_json.get("user_input", "")

            # 프롬프트 지시: 감정을 직접 추론하도록 지시
            # 시스템 메시지 구성 (GPT가 자신의 역할, 사용자의 감정을 인식하도록 유도)
            system_lines = [
                config.BASE_PROMPT_PREFIX,
                "사용자의 발화를 바탕으로 감정을 직접 추론하세요."
            ]

            insert_text = self._choose_random_insert()
            if insert_text:
                system_lines.append(insert_text)

            if config.FORBIDDEN_WORDS:
                forbidden = ", ".join(config.FORBIDDEN_WORDS)
                system_lines.append(f"절대 사용하지 말아야 할 단어: {forbidden}")

            system_lines.append(
                '반드시 다음 JSON 형식으로 응답하세요: {"response": "텍스트 응답", "emotion": "감정명"}'
            )

            system_message = " ".join(system_lines)

            messages = [{"role": "system", "content": system_message}]
            if self.conversation_history:
                messages.extend(self.conversation_history)
            messages.append({"role": "user", "content": user_input})

            return messages

        # 예외 발생 시: 사과 메시지를 system message로 반환
        except Exception as e:
            print(f"[ERROR] PromptManager.generate_prompt(): {e}")
            apology = random.choice(config.ERROR_APOLOGIES)

            return [
                {"role": "system", "content": config.BASE_PROMPT_PREFIX},
                {"role": "assistant", "content": apology}
            ]

    def _choose_random_insert(self):
        # 무작위 템플릿 중 하나를 선택 (중복 방지)
        inserts = config.RANDOM_PROMPT_INSERTS.copy()
        if self.last_insert in inserts and len(inserts) > 1:
            inserts.remove(self.last_insert)
        insert_text = random.choice(inserts) if inserts else None
        self.last_insert = insert_text
        return insert_text

    def add_to_history(self, user_input, assistant_output):
        # 이전 대화 기록에 현재 사용자 발화와 GPT 응답 추가
        # 이후 프롬프트 구성 시 문맥 유지에 활용되는 코드
        self.conversation_history.append({"role": "user", "content": user_input})
        self.conversation_history.append({"role": "assistant", "content": assistant_output})

    def reset(self):
        self.conversation_history = []
        self.last_insert = None  # 선택적 초기화


