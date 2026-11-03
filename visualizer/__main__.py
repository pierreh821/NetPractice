import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

MASKS = {
    0: 24,
    128: 25,
    192: 26,
    224: 27,
    240: 28,
    248: 29,
    252: 30
    }


def closest(val: int, allowed: list[int]):
    best = allowed[0]
    best_diff = abs(allowed[0] - val)

    for a in allowed:
        if abs(a - val) < best_diff:
            best = a
            best_diff = abs(a - val)

    return best


class MaskSlider:
    def __init__(self, win: pygame.Surface):
        self.win = win
        self.slider = Slider(win, x=0, y=50, width=100, height=20,
                             min=0, max=255, step=1)

    def layout(self):
        width = self.win.get_width()
        self.slider.setX(int(width * 0.1))
        self.slider.setWidth(int(width * 0.8))

    def round(self) -> int:
        user = self.slider.getValue()
        rounded = closest(user, list(MASKS.keys()))
        self.slider.setValue = rounded
        return rounded

    def force_value(self, val: int):
        self.slider = Slider(win, x=0, y=50, width=100, height=20, min=0,
                             max=255, step=1, initial=val)
        print(self.slider.getValue())
        self.layout()


class Text:
    def __init__(self, win: pygame.Surface):
        # self.box = TextBox(win, , 80, 100, 20)
        self.box = TextBox(win, win.get_width()/2, 80, 150, 50, fontSize=30)
        self.win = win

    def render(self, val: int):
        self.box.setText(f"{val}: /{MASKS[val]}")


class Line:
    def __init__(self, win: pygame.Surface):
        self.win = win

    def render(self) -> None:
        height = self.win.get_height()
        width = self.win.get_width()

        pygame.draw.rect(self.win, 'black', pygame.Rect(
            width * 0.1,
            (height - 70) * 0.4,
            width*0.8,
            min(100, (height - 70) * 0.8)
        ), width=5)


pygame.init()
win = pygame.display.set_mode((1000, 600), pygame.RESIZABLE)

slider = MaskSlider(win)
slider.layout()
text = Text(win)
line = Line(win)

run = True
while run:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.VIDEORESIZE:
            slider.layout()
        elif event.type == pygame.MOUSEBUTTONUP:
            val = slider.round()
            slider.force_value(val)

    win.fill((255, 255, 255))

    val = slider.round()
    text.render(val)
    line.render()
    pygame_widgets.update(events)
    pygame.display.update()

pygame.quit()
