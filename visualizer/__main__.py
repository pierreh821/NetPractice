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


def bin_to_cidr(mask: int, byte: int):
    res = ['1' * 8 for _ in range(byte - 1)]
    res.append(str(bin(mask)))
    return ''.join(res).count('1')


class Visualizer:
    def __init__(self):
        self.byte = 4
        self.fig, self.ax = plt.subplots(figsize=(10, 3))
        plt.subplots_adjust(bottom=0.35)

        self.ax.set_xlim(0, 256)
        self.ax.set_ylim(0, 1)
        self.ax.set_yticks([])

        self.ax.barh(0.5, 256, left=0, height=0.3, color="#ddd")

        self.ax_slider = plt.axes((0.15, 0.1, 0.7, 0.05))
        self.slider = Slider(self.ax_slider, "Mask", 0, 252,
                             valinit=0, valstep=list(MASKS.keys()))

        self.ay_slider = plt.axes((0.02, 0.25, 0.0225, 0.63))
        self.b_slider = Slider(self.ay_slider, "Byte", 1, 4,
                               valinit=4, valstep=1, orientation='vertical')

        self.current = []

    def draw_byte_changed(self, byte: int):
        self.byte = byte
        self.draw(self.mask)

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

        self.ax.set_title(f"mask {mask} (/{bin_to_cidr(mask, self.byte)}) : "
                          f"{256 // size} subnets of {size} adresses each")
        self.fig.canvas.draw_idle()

    def on_scroll(self, event):
        auth_masks = list(MASKS.keys())

        window = self.fig.get_window_extent()
        x, y = event.x, event.y
        wx, wy = window.x1, window.y1
        rx, ry = x / wx, y / wy

        if rx > 0.12 or ry < 0.21:  # Mask
            if event.button == 'up':
                id = auth_masks.index(self.mask)
                new = auth_masks[min(id + 1, len(auth_masks) - 1)]
            else:
                id = auth_masks.index(self.mask)
                new = auth_masks[max(id - 1, 0)]

            self.mask = new
            self.slider.set_val(new)

        else:  # Bytes
            if event.button == 'up':
                new = min(self.byte + 1, 4)
            else:
                new = max(self.byte - 1, 1)

            self.byte = new
            self.b_slider.set_val(new)

        self.draw(self.mask)

    def run(self):
        self.slider.on_changed(self.draw)
        self.b_slider.on_changed(self.draw_byte_changed)  # pas adapte
        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.draw(0)
        plt.show()


if __name__ == "__main__":
    try:
        visualizer = Visualizer()
        visualizer.run()
    except KeyboardInterrupt:
        pass
