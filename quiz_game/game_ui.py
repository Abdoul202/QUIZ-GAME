import pygame

class GameUI:
    def __init__(self):
        # Configuration de la fenêtre
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Quiz Game")
        
        # Polices
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Couleurs
        self.colors = {
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "gray": (200, 200, 200),
            "green": (0, 200, 0),
            "red": (200, 0, 0),
            "blue": (0, 0, 200),
            "light_blue": (100, 100, 255),
            "orange": (255, 165, 0),
            "dark_green": (100, 200, 100),
            "brown": (150, 100, 50),
            "dark_blue": (50, 100, 200),
            "pink": (200, 50, 100)
        }
        
        # Horloge
        self.clock = pygame.time.Clock()
    
    def draw_menu(self):
        self.draw_text("Quiz Game", self.font_large, "black", self.width//2, 100)
        self.draw_button("Commencer", "light_blue", self.width//2, 250, 200, 50)

    def draw_level_selection(self):
        self.draw_text("Choisissez un niveau", self.font_large, "black", self.width//2, 50)
        
        buttons = [
            ("Facile", "green", 150),
            ("Moyen", "orange", 220),
            ("Difficile", "red", 290),
            ("Retour", "gray", 360)
        ]
        
        for text, color, y in buttons:
            self.draw_button(text, color, self.width//2, y, 200, 50)

    def draw_category_selection(self):
        self.draw_text("Choisissez une catégorie", self.font_large, "black", self.width//2, 50)
        
        categories = [
            ("Culture Générale", "dark_green", 150),
            ("Histoire", "brown", 220),
            ("Mathématiques", "dark_blue", 290),
            ("Science", "pink", 360),
            ("Retour", "gray", 430)
        ]
        
        for text, color, y in categories:
            self.draw_button(text, color, self.width//2, y, 300, 50)

    def draw_quiz(self, question, feedback=None, score=0, total=0):
        # Affichage score
        self.draw_text(f"Score: {score}/{total}", self.font_small, "black", self.width-100, 30)
        
        # Question
        self.draw_text(question["question"], self.font_medium, "black", 50, 50, align_left=True)
        
        # Options
        for i, option in enumerate(question["options"]):
            color = self.get_option_color(i, question, feedback)
            self.draw_button(option, color, 50, 120 + i*70, self.width-100, 60, align_left=True)
        
        # Feedback
        if feedback:
            self.draw_feedback(feedback)

    def draw_result(self, score, total):
        percentage = (score/total)*100 if total > 0 else 0
        color = "green" if percentage >= 50 else "red"
        
        self.draw_text("Résultats", self.font_large, "black", self.width//2, 100)
        self.draw_text(f"Score: {score}/{total} ({percentage:.0f}%)", 
                      self.font_medium, color, self.width//2, 200)
        
        # Message personnalisé
        if percentage >= 80:
            message = "Excellent !"
        elif percentage >= 50:
            message = "Bon travail !"
        else:
            message = "Peut mieux faire !"
        self.draw_text(message, self.font_medium, "black", self.width//2, 250)
        
        # Boutons
        self.draw_button("Recommencer", "light_blue", self.width//2 - 110, 350, 200, 50)
        self.draw_button("Menu", "light_blue", self.width//2 + 110, 350, 200, 50)

    # [...] (autres méthodes comme is_button_clicked, get_selected_option, etc.)

    # Méthodes utilitaires
    def draw_text(self, text, font, color, x, y, align_left=False):
        text_surface = font.render(text, True, self.colors[color])
        if not align_left:
            x -= text_surface.get_width() // 2
        self.screen.blit(text_surface, (x, y))

    def draw_button(self, text, color, x, y, w, h, align_left=False):
        if not align_left:
            x -= w // 2
        pygame.draw.rect(self.screen, self.colors[color], (x, y, w, h))
        btn_text = self.font_medium.render(text, True, self.colors["white"])
        self.screen.blit(btn_text, (x + w//2 - btn_text.get_width()//2, y + h//2 - btn_text.get_height()//2))

    def get_option_color(self, index, question, feedback):
        if not feedback:
            return "light_blue"
        if index == question["correct_answer"]:
            return "green"
        if (index == feedback.get("selected_option") and 
            not feedback["is_correct"]):
            return "red"
        return "light_blue"

    def draw_feedback(self, feedback):
        color = "green" if feedback["is_correct"] else "red"
        self.draw_text("Correct!" if feedback["is_correct"] else "Incorrect!", 
                      self.font_medium, color, 50, 400, align_left=True)
        self.draw_text(feedback["explanation"], self.font_small, "black", 50, 440, align_left=True)
        
        # Bouton Suivant
        self.draw_button("Suivant", "light_blue", self.width - 100, self.height - 60, 100, 50)

    def is_button_clicked(self, mouse_pos, button_name):
        x, y = mouse_pos
        buttons = {
            "start_button": (self.width//2 - 100, 250, 200, 50),
            "easy_button": (self.width//2 - 100, 150, 200, 50),
            "medium_button": (self.width//2 - 100, 220, 200, 50),
            "hard_button": (self.width//2 - 100, 290, 200, 50),
            "back_button": (self.width//2 - 100, 360, 200, 50),
            "culture_button": (self.width//2 - 150, 150, 300, 50),
            "history_button": (self.width//2 - 150, 220, 300, 50),
            "math_button": (self.width//2 - 150, 290, 300, 50),
            "science_button": (self.width//2 - 150, 360, 300, 50),
            "next_button": (self.width - 150, self.height - 80, 100, 50),
            "menu_button": (self.width//2 + 20, 350, 200, 50),
            "restart_button": (self.width//2 - 220, 350, 200, 50)
        }
        
        if button_name in buttons:
            bx, by, bw, bh = buttons[button_name]
            return bx <= x <= bx + bw and by <= y <= by + bh
        return False

    def get_selected_option(self, mouse_pos):
        x, y = mouse_pos
        for i in range(4):
            if 50 <= x <= self.width - 50 and 120 + i*70 <= y <= 180 + i*70:
                return i
        return None