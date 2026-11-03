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


class Visualizer:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 3))
        plt.subplots_adjust(bottom=0.35)

        self.ax.set_xlim(0, 256)
        self.ax.set_ylim(0, 1)
        self.ax.set_yticks([])

        self.ax.barh(0.5, 256, left=0, height=0.3, color="#ddd")

        self.ax_slider = plt.axes((0.15, 0.1, 0.7, 0.05))
        self.slider = Slider(self.ax_slider, "Mask", 0, 252,
                             valinit=0, valstep=list(MASKS.keys()))

        self.current = []

    def draw(self, mask):
        self.mask = mask
        size = 256 - mask

        for bar in self.current:
            bar.remove()
        self.current.clear()

        for sub in range(256 // size):
            first = size * sub
            left = size * sub
            container = self.ax.barh(0.5, size, left=left, height=0.3,
                                     color="tab:blue" if sub % 2 == 0
                                     else "tab:purple")
            left_id = self.ax.text(left, 0.5, str(first))
            self.current.extend(container.patches)
            self.current.append(left_id)

        self.ax.set_title(f"mask {mask} (/{MASKS[mask]}) : "
                          f"{256 // size} subnets of {size} adresses each")
        self.fig.canvas.draw_idle()

    def on_scroll(self, event):
        authorized = list(MASKS.keys())

        if event.button == 'up':
            id = authorized.index(self.mask)
            new = authorized[min(id + 1, len(authorized) - 1)]
        else:
            id = authorized.index(self.mask)
            new = authorized[max(id - 1, 0)]

        self.mask = new
        self.slider.set_val(new)
        self.draw(new)


    def run(self):
        self.slider.on_changed(self.draw)
        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.draw(0)
        plt.show()


if __name__ == "__main__":
    try:
        visualizer = Visualizer()
        visualizer.run()
    except KeyboardInterrupt:
        pass
