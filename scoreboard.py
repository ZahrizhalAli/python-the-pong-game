from turtle import Turtle


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(0, 200)
        self.l_score = 0
        self.r_score = 0
        self.refresh()

    def refresh(self):
        self.clear()
        self.write(f"{self.l_score}  {self.r_score}", align="center", font=("Courier", 80, "normal"))

