import json
import random
from pathlib import Path

class QuizManager:
    def __init__(self):
        self.questions = {
            "easy": [],
            "medium": [],
            "hard": []
        }
        self.base_dir = Path(__file__).parent
        self.used_question_ids = set()

    def load_questions(self):
        try:
            questions_dir = self.base_dir / "resources" / "data" / "questions"
            
            if not questions_dir.exists():
                print(f"Erreur: Dossier introuvable - {questions_dir}")
                return False
            
            for level in self.questions.keys():
                file_path = questions_dir / f"{level}.json"
                with open(file_path, "r", encoding="utf-8") as f:
                    self.questions[level] = json.load(f)["questions"]
            return True
            
        except Exception as e:
            print(f"Erreur de chargement: {e}")
            return False

    def get_question(self, level, category):
        available = [
            q for q in self.questions[level] 
            if q["category"] == category and q["id"] not in self.used_question_ids
        ]
        
        if not available:
            # Réinitialiser si toutes les questions ont été utilisées
            self.reset_used_questions()
            available = [
                q for q in self.questions[level] 
                if q["category"] == category
            ]
        
        question = random.choice(available)
        self.used_question_ids.add(question["id"])
        return question

    def reset_used_questions(self):
        self.used_question_ids = set()

    def check_answer(self, question, selected_option):
        return selected_option == question["correct_answer"]