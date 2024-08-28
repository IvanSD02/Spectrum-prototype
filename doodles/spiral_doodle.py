import turtle
import colorsys

def draw_spiral():
    turtle.bgcolor('black')
    turtle.tracer(500)
    h = 0
    for i in range(100):
        c = colorsys.hsv_to_rgb(h,1,1)
        h += 0.5
        turtle.up()
        turtle.goto(0,0)
        turtle.down()
        turtle.color('white')
        turtle.fillcolor (c)
        turtle.begin_fill()
        turtle.rt (98)
        turtle.circle(i,12)
        turtle.fd(i)
        turtle.lt (29)
        for j in range(129):
          turtle.fd(i)
          turtle.circle(j, 299, steps=2)
        turtle.end_fill()

