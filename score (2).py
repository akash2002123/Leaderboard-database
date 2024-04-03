from turtle import Turtle


class Score(Turtle):

    def __init__(self):
        super().__init__()

        self.penup()

        self.color("white")
        self.hideturtle()
        self.shapesize(stretch_len=2, stretch_wid=2)
        self.goto(0, 270)
        self.score = -1

        self.update_score()

    def update_score(self):
        self.clear()
        self.score += 1
        self.write(f"Score: {self.score}", False, "center", font=("Arial", 20, "normal"))

    def game_over(self):
        self.goto(0, 0)
        self.write("Game Over!", False, "center", font=("Arial", 30, "normal"))
