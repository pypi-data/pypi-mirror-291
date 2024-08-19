def snakegame():
    import turtle
    import time
    import random

    delay = 0.1
    
    wn = turtle.Screen()
    wn.title("Snake Game")
    wn.bgcolor("green")
    wn.setup(width=600, height=600)
    wn.tracer(0)
    
    head = turtle.Turtle()
    head.speed(0)
    head.color("black")
    head.shape("square")
    head.penup()
    head.goto(0, 0)
    head.direction = "Left"
    
    food = turtle.Turtle()
    food.speed(0)
    food.color("red")
    food.shape("circle")
    food.penup()
    food.goto(0, 100)
    
    segments = []
    
    score = 0
    high_score = 0
    
    score_display = turtle.Turtle()
    score_display.speed(0)
    score_display.color("white")
    score_display.penup()
    score_display.hideturtle()
    score_display.goto(0, 260)
    score_display.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))
    
    def go_up():
        if head.direction != "Down":
            head.direction = "Up"
    
    def go_down():
        if head.direction != "Up":
            head.direction = "Down"
    
    def go_left():
        if head.direction != "Right":
            head.direction = "Left"
    
    def go_right():
        if head.direction != "Left":
            head.direction = "Right"
    
    def move():
        if head.direction == "Up":
            y = head.ycor()
            head.sety(y + 20)
    
        if head.direction == "Down":
            y = head.ycor()
            head.sety(y - 20)
    
        if head.direction == "Left":
            x = head.xcor()
            head.setx(x - 20)
    
        if head.direction == "Right":
            x = head.xcor()
            head.setx(x + 20)
    
    def check_collision_with_food():
        if head.distance(food) < 20:
            x = random.randint(-290, 290)
            y = random.randint(-290, 290)
            food.goto(x, y)
    
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("gray")
            new_segment.penup()
            segments.append(new_segment)
    
            return True
        return False
    
    def check_collision_with_segments():
        for segment in segments:
            if segment.distance(head) < 20:
                return True
        return False
    
    wn.listen()
    wn.onkeypress(go_up, "w")
    wn.onkeypress(go_down, "s")
    wn.onkeypress(go_left, "a")
    wn.onkeypress(go_right, "d")
    
    while True:
        wn.update()
    
        if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
            time.sleep(0.1)
            head.goto(0, 0)
            head.direction = "Stop"
    
            for segment in segments:
                segment.goto(1000, 1000)
    
            segments.clear()
    
            score = 0
            score_display.clear()
            score_display.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))
    
        if check_collision_with_food():
            score += 10
            if score > high_score:
                high_score = score
            score_display.clear()
            score_display.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))
    
        if check_collision_with_segments():
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "Stop"
    
            for segment in segments:
                segment.goto(1000, 1000)
    
            segments.clear()
    
            score = 0
            score_display.clear()
            score_display.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))
    
        for index in range(len(segments) - 1, 0, -1):
            x = segments[index - 1].xcor()
            y = segments[index - 1].ycor()
            segments[index].goto(x, y)
    
        if len(segments) > 0:
            x = head.xcor()
            y = head.ycor()
            segments[0].goto(x, y)
    
        move()
    
        time.sleep(delay)
    
    