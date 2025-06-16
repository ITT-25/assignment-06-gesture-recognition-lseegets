import pyglet
from pyglet import window, shapes, text
from recognizer import recognize

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

win = window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)
dots = []
points = []
input_gesture = None


@win.event
def on_mouse_press(x, y, button, modifiers):
    dots.clear()
    points.clear()


@win.event
def on_mouse_release(x, y, button, modifiers):
    global input_gesture
    input_gesture = recognize(points)


@win.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons & window.mouse.LEFT:
        dots.append(shapes.Rectangle(x, y, 5, 5, (255, 255, 255)))
        points.append((x, WINDOW_HEIGHT - y))
        

@win.event
def on_draw():
    win.clear()
    for i in range(0, len(dots)):
        if i == 0:
            dots[i].draw()
        else:
            dots[i].draw()
            if dots[i].x - dots[i-1].x != 0 or dots[i].y - dots[i-1].y != 0:
                shapes.Line(dots[i].x, dots[i].y, dots[i-1].x, dots[i-1].y).draw()
    text.Label(f'Input: {input_gesture}', font_size=20, x=150, y=WINDOW_HEIGHT-30, anchor_x='center').draw()

pyglet.app.run()