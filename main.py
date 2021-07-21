from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time

screen = Screen()
screen.setup(800, 600)
screen.bgcolor("black")
screen.listen()
screen.tracer(0)

r_paddle = Paddle((350, 0))
l_paddle = Paddle((-350, 0))
ball = Ball()
score = Scoreboard()


screen.onkeypress(l_paddle.go_up, "w")
screen.onkeypress(l_paddle.go_down, "s")
screen.onkeypress(r_paddle.go_up, "Up")
screen.onkeypress(r_paddle.go_down, "Down")
is_game_on = True
while is_game_on:
    time.sleep(ball.move_speed)
    screen.update()
    ball.move()

    # Detect collision with upper and lower walls
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

    # Detect collision with paddle
    if ball.distance(r_paddle) < 70 and ball.xcor() > 320 or ball.distance(l_paddle) < 70 and ball.xcor() < -320:
        ball.bounce_x()

    elif ball.xcor() > 380:
        print("L paddle wins")
        score.l_score += 1
        score.refresh()
        ball.move_speed = 0.1
        ball.goto(0, 0)
        time.sleep(0.3)
        ball.bounce_x()
    elif ball.xcor() < -380:
        print("R paddle wins")
        score.r_score += 1
        score.refresh()
        ball.move_speed = 0.1
        ball.goto(0, 0)
        time.sleep(0.3)
        ball.bounce_x()


screen.exitonclick()
