import turtle
import random
def draw_stars(n, x, angle):
    turtle.speed(speed='fastest')
    # loop for number of stars
    for i in range(n):

        turtle.colormode(255)

        # choosing random integers
        # between 0 and 255
        # to generate random rgb values
        a = random.randint(0, 255)
        b = random.randint(0, 255)
        c = random.randint(0, 255)

        # setting the outline
        # and fill colour
        turtle.pencolor(a, b, c)
        turtle.fillcolor(a, b, c)

        # begins filling the star
        turtle.begin_fill()

        # loop for drawing each star
        for j in range(5):
            turtle.forward(5 * n - 5 * i)
            turtle.right(x)
            turtle.forward(5 * n - 5 * i)
            turtle.right(72 - x)

        # colour filling complete
        turtle.end_fill()

        # rotating for
        # the next star
        turtle.rt(angle)

def example_draw_stars():
    # setting the parameters
    n = 50  # number of stars
    x = 144  # exterior angle of each star
    angle = 18  # angle of rotation for the spiral

    draw_stars(n, x, angle)