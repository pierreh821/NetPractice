from matplotlib.container import BarContainer
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

MASKS = {
    0: 24,
    128: 25,
    192: 26,
    224: 27,
    240: 28,
    248: 29,
    252: 30
    }

fig, ax = plt.subplots(figsize=(10, 3))
plt.subplots_adjust(bottom=0.35)

ax.set_xlim(0, 256)
ax.set_ylim(0, 1)
ax.set_yticks([])

ax.barh(0.5, 256, left=0, height=0.3, color="#ddd")

current: list[BarContainer | plt.Text] = []


def draw(mask):
    size = 256 - mask

    for bar in current:
        bar.remove()
    current.clear()

    for sub in range(256 // size):
        first = size * sub
        left = size * sub
        container = ax.barh(0.5, size, left=left, height=0.3,
                            color="tab:blue" if sub % 2 == 0 else "tab:red")
        left_id = ax.text(left, 0.5, str(first))
        current.extend(container.patches)
        current.append(left_id)

    ax.set_title(f"masque {mask} (/{MASKS[mask]}) : "
                 f"{256 // size} sous-réseaux de {size} adresses")
    fig.canvas.draw_idle()


ax_slider = plt.axes((0.15, 0.1, 0.7, 0.05))
slider = Slider(ax_slider, "Masque", 0, 252, valinit=0,
                valstep=list(MASKS.keys()))
slider.on_changed(draw)

draw(0)
plt.show()
