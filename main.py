from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time
import cv2
import numpy as np
from keras.models import load_model



# load the model
model = load_model('model.savedmodel')

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

cap=cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

roi_top = 20
roi_bottom = 300
roi_right = 300
roi_left = 600
while is_game_on:
    sucess, imgOriginal = cap.read()
    # Draw ROI Rectangle on frame copy
    cv2.rectangle(imgOriginal, (roi_left, roi_top), (roi_right, roi_bottom), (0,0,255), 5)
    # Resize the raw image into (224-height,224-width) pixels.
    img = cv2.resize(imgOriginal[roi_top:roi_bottom, roi_right:roi_left], (224, 224))
    # Show the image in a window
    cv2.imshow('Webcam Image', imgOriginal)
    # Make the image a numpy array and reshape it to the models input shape.
    img = np.asarray(img, dtype=np.float32).reshape(1, 224, 224, 3)
    # Normalize the image array
    img = (img / 127.5) - 1

    probabilities = model.predict(img)

    index = np.argmax(probabilities)
    if index == 0:
        r_paddle.go_up()
    if index == 1:
        r_paddle.go_down()


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

