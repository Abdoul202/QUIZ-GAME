class Difficulty:
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    
    @staticmethod
    def get_all_levels():
        return [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD]