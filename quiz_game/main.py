import pygame
import sys
from game_ui import GameUI
from quiz_manager import QuizManager

class QuizGame:
    def __init__(self):
        pygame.init()
        self.ui = GameUI()
        self.quiz_manager = QuizManager()
        self.reset_game_state()
        
    def reset_game_state(self):
        self.current_screen = "menu"
        self.selected_level = None
        self.selected_category = None
        self.score = 0
        self.questions_answered = 0
        self.current_question = None
        self.feedback = None
        self.MAX_QUESTIONS = 5

    def run(self):
        if not self.quiz_manager.load_questions(): 
            print("Erreur lors du chargement des questions.")
            return

        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_events(event)

            self.update_display()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.current_screen == "menu":
                if self.ui.is_button_clicked(mouse_pos, "start_button"):
                    self.current_screen = "level_selection"
            
            elif self.current_screen == "level_selection":
                self.handle_level_selection(mouse_pos)
            
            elif self.current_screen == "category_selection":
                self.handle_category_selection(mouse_pos)
            
            elif self.current_screen == "quiz":
                self.handle_quiz_interaction(mouse_pos)
            
            elif self.current_screen == "result":
                self.handle_result_interaction(mouse_pos)

    def handle_level_selection(self, mouse_pos):
        if self.ui.is_button_clicked(mouse_pos, "easy_button"):
            self.selected_level = "easy"
            self.current_screen = "category_selection"
        elif self.ui.is_button_clicked(mouse_pos, "medium_button"):
            self.selected_level = "medium"
            self.current_screen = "category_selection"
        elif self.ui.is_button_clicked(mouse_pos, "hard_button"):
            self.selected_level = "hard"
            self.current_screen = "category_selection"
        elif self.ui.is_button_clicked(mouse_pos, "back_button"):
            self.current_screen = "menu"

    def handle_category_selection(self, mouse_pos):
        categories = {
            "culture_button": "culture générale",
            "history_button": "histoire",
            "math_button": "math",
            "science_button": "science"
        }
        
        for btn, category in categories.items():
            if self.ui.is_button_clicked(mouse_pos, btn):
                self.selected_category = category
                self.current_question = self.quiz_manager.get_question(
                    self.selected_level, self.selected_category
                )
                self.current_screen = "quiz"
                self.score = 0
                self.questions_answered = 0
                return
                
        if self.ui.is_button_clicked(mouse_pos, "back_button"):
            self.current_screen = "level_selection"

    def handle_quiz_interaction(self, mouse_pos):
        if self.current_question:
            selected_option = self.ui.get_selected_option(mouse_pos)
            if selected_option is not None and self.feedback is None:
                self.process_answer(selected_option)
            
            elif self.ui.is_button_clicked(mouse_pos, "next_button"):
                self.move_to_next_question()

    def process_answer(self, selected_option):
        is_correct = self.quiz_manager.check_answer(self.current_question, selected_option)
        self.feedback = {
            "is_correct": is_correct,
            "explanation": self.current_question["explanation"],
            "selected_option": selected_option
        }
        if is_correct:
            self.score += 1
        self.questions_answered += 1

    def move_to_next_question(self):
        if self.questions_answered < self.MAX_QUESTIONS:
            self.current_question = self.quiz_manager.get_question(
                self.selected_level, self.selected_category
            )
            self.feedback = None
        else:
            self.current_screen = "result"

    def handle_result_interaction(self, mouse_pos):
        if self.ui.is_button_clicked(mouse_pos, "restart_button"):
            self.current_screen = "category_selection"
            self.feedback = None
        elif self.ui.is_button_clicked(mouse_pos, "menu_button"):
            self.reset_game_state()

    def update_display(self):
        self.ui.screen.fill((240, 240, 240))
        
        if self.current_screen == "menu":
            self.ui.draw_menu()
        elif self.current_screen == "level_selection":
            self.ui.draw_level_selection()
        elif self.current_screen == "category_selection":
            self.ui.draw_category_selection()
        elif self.current_screen == "quiz":
            self.ui.draw_quiz(
                self.current_question,
                self.feedback,
                self.score,
                self.questions_answered
            )
        elif self.current_screen == "result":
            self.ui.draw_result(self.score, self.questions_answered)

if __name__ == "__main__":
    game = QuizGame()
    game.run()