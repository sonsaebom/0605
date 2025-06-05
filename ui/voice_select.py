import pygame
import os
import json
from config import WHITE, BLACK, LIGHT_BLUE, LIGHT_PINK, BLUE, PINK, BACKGROUND_GRAY, load_fonts, VOICE_SETTING_PATH


def run_voice_select(screen):
    clock = pygame.time.Clock()

    font_medium, font_small = load_fonts()
    if not font_medium or not font_small:
        return None

    base_dir = os.path.dirname(__file__)
    image_dir = os.path.join(base_dir, '..', 'image')
    male_icon = pygame.image.load(os.path.join(image_dir, "male.png"))
    female_icon = pygame.image.load(os.path.join(image_dir, "female.png"))

    male_icon = pygame.transform.scale(male_icon, (150, 150))
    female_icon = pygame.transform.scale(female_icon, (150, 150))

    selected_gender = None

    def draw_text(text, font, color, center):
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=center)
        screen.blit(surface, rect)

    def draw_select_screen():
        screen.fill(BACKGROUND_GRAY)
        male_rect = pygame.Rect(0, 0, 400, 360)
        female_rect = pygame.Rect(400, 0, 400, 360)
        confirm_button = pygame.Rect(300, 380, 200, 60)

        pygame.draw.rect(screen, LIGHT_BLUE if selected_gender == "male" else WHITE, male_rect)
        pygame.draw.rect(screen, LIGHT_PINK if selected_gender == "female" else WHITE, female_rect)

        screen.blit(male_icon, (male_rect.centerx - 75, 50))
        screen.blit(female_icon, (female_rect.centerx - 75, 50))

        draw_text("남자", font_medium, BLACK, (male_rect.centerx, 230))
        draw_text("여자", font_medium, BLACK, (female_rect.centerx, 230))

        pygame.draw.circle(screen, BLUE if selected_gender == "male" else WHITE, (male_rect.centerx, 280), 10)
        pygame.draw.circle(screen, BLACK, (male_rect.centerx, 280), 10, 2)

        pygame.draw.circle(screen, PINK if selected_gender == "female" else WHITE, (female_rect.centerx, 280), 10)
        pygame.draw.circle(screen, BLACK, (female_rect.centerx, 280), 10, 2)

        pygame.draw.rect(screen, WHITE, confirm_button)
        pygame.draw.rect(screen, BLACK, confirm_button, 2)

        draw_text("선택 완료", font_small, BLACK, confirm_button.center)

        return male_rect, female_rect, confirm_button


    running = True
    while running:
        male_rect, female_rect, confirm_btn = draw_select_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if male_rect.collidepoint(mouse_pos):
                    selected_gender = "male"
                elif female_rect.collidepoint(mouse_pos):
                    selected_gender = "female"
                elif confirm_btn.collidepoint(mouse_pos) and selected_gender:
                    # 선택된 성별 저장
                    with open(VOICE_SETTING_PATH, "w", encoding="utf-8") as f:
                        json.dump({"voice": selected_gender}, f)

                    return selected_gender  # 선택 완료 후 종료

        pygame.display.flip()
        clock.tick(30)

    # 명시적 반환 추가 (경고 해결)
    return None


