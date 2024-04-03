from turtle import Turtle

init_pos = [[-20, 0], [0, 0], [20, 0]]


class Snake:

    def __init__(self):
        self.segments = []
        self.init_body()
        self.head = self.segments[-1]

    def init_body(self):
        for i in range(3):
            self.add_segment(init_pos[i])

    def add_segment(self, pos):
        segment = Turtle("square")
        segment.penup()
        segment.color("white")
        segment.setposition(pos)

        if len(self.segments) > 1:
            segment.setheading(self.segments[-1].heading())

        self.segments.append(segment)
        self.head = self.segments[-1]

    def move(self):
        for i in range(len(self.segments)):
            self.segments[i].forward(20)

        for i in range(len(self.segments) - 1):
            self.segments[i].setheading(self.segments[i + 1].heading())

    def grow(self):
        pos = self.segments[-1].pos()
        x, y = pos[0], pos[1]

        if self.head.heading() == 0:
            x += 20
        elif self.head.heading() == 90:
            y += 20
        elif self.head.heading() == 180:
            x -= 20
        else:
            y -= 20

        self.add_segment((x, y))

    def left(self):
        if self.head.heading() != 0:
            self.head.setheading(180)

    def right(self):
        if self.head.heading() != 180:
            self.head.setheading(0)

    def up(self):
        if self.head.heading() != 270:
            self.head.setheading(90)

    def down(self):
        if self.head.heading() != 90:
            self.head.setheading(270)

    def did_hit_wall(self):
        return not(-290 < self.head.xcor() < 290 and -290 < self.head.ycor() < 290)

    def did_collide_itself(self):
        for segment in self.segments[0:len(self.segments) - 1]:
            if self.head.distance(segment) < 10:
                return True

        return False
