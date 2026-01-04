import pgzero.screen

class HighScore:
    def __init__(self, height):
        self.height = height
        self.score = 0
    
    def add_distance(self, dist):
        self.score += dist

    def draw(self, screen: pgzero.screen.Screen):
        screen.draw.text(f"Score: {self.score}", topleft=(0, 0), fontsize=self.height, color='white')
