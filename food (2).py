from turtle import Turtle
import random


class Food(Turtle):

    def __init__(self):
        super().__init__()

        self.penup()
        self.shape("circle")
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.color("red")
        self.speed("fastest")

        self.new_location()

    def new_location(self):

        rx, ry = random.randint(-280, 280), random.randint(-280, 260)
        self.goto(rx, ry)
