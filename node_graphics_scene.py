import tkinter as tk
import numpy as np
import sys

SCENE_WIDTH = 800
SCENE_HIGH = 600
CANVAS_WIDTH = 6400
CANVAS_HIGH = 1000
GRID_SIZE = 50
BACKGROUND_COLOR = "#192026"
GRID_COLOR = "#3b3c3d"


class NodeGraphicsScene(tk.Canvas):
    def __init__(self, parent=None, move=True, zoom=True):
        super().__init__(
            master=parent,
            background=BACKGROUND_COLOR,
            relief=tk.GROOVE,
            width=SCENE_WIDTH,
            height=SCENE_HIGH,
            scrollregion=(0, 0, CANVAS_WIDTH, CANVAS_HIGH),
            xscrollincrement=GRID_SIZE // 5,
            yscrollincrement=GRID_SIZE // 5,
        )

        # create scrollbar
        x_scroll = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        x_scroll.config(command=self.xview)
        y_scroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        y_scroll.config(command=self.yview)
        self.config(xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)
        self.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        self.draw_background()

        # if move:
        #     if sys.platform.startswith("darwin"):
        #         self.tag_bind(self, "<ButtonPress-3>", lambda e: self.getpos(e, 1))
        #         self.tag_bind(self, "<ButtonRelease-3>", lambda e: self.getpos(e, 0))
        #         self.tag_bind(self, "<B3-Motion>", self.move_grid)
        #     else:
        #         self.tag_bind(self, "<ButtonPress-2>", lambda e: self.getpos(e, 1))
        #         self.tag_bind(self, "<ButtonRelease-2>", lambda e: self.getpos(e, 0))
        #         self.tag_bind(self, "<B2-Motion>", self.move_grid)

        # if zoom:
        #     self.bind("<MouseWheel>", self.do_zoom)
        #     self.tag_bind(self, "<Button-4>", lambda e: self.do_zoom(e, 120))
        #     self.tag_bind(self, "<Button-5>", lambda e: self.do_zoom(e, -120))

    def draw_background(self):
        # create vertical grid line
        line_count = 0
        for i in range(0, CANVAS_WIDTH, GRID_SIZE):
            if line_count == 5:
                line_count = 0
                self.create_line(
                    [(i, 0), (i, CANVAS_HIGH)],
                    width=2,
                    fill=GRID_COLOR,
                    tag="grid_line",
                )
            else:
                self.create_line(
                    [(i, 0), (i, CANVAS_HIGH)],
                    width=1,
                    fill=GRID_COLOR,
                    tag="grid_line",
                )
            line_count += 1

        # create horizontal grid line
        line_count = 0
        for i in range(0, CANVAS_HIGH, GRID_SIZE):
            if line_count == 5:
                line_count = 0
                self.create_line(
                    [(0, i), (CANVAS_WIDTH, i)],
                    width=2,
                    fill=GRID_COLOR,
                    tag="grid_line",
                )
            else:
                self.create_line(
                    [(0, i), (CANVAS_WIDTH, i)],
                    width=1,
                    fill=GRID_COLOR,
                    tag="grid_line",
                )
            line_count += 1

    def move_grid(self, event):
        """move the contents of the canvas except the grid image"""

        self.all_items = list(self.find_all())
        self.all_items.pop(self.all_items.index(self))

        for i in self.all_items:
            self.move(i, event.x - self.xy_set[0], event.y - self.xy_set[1])
        self.xy_set = (event.x, event.y)

        for i in self.node_list:
            i.update_sockets()

    def do_zoom(self, event, delta=None):
        """zoom in/out the canvas by changing the coordinates of all canvas items"""

        self.all_items = list(self.find_all())
        self.all_items.pop(self.all_items.index(self))

        if not delta:
            delta = event.delta

        if delta > 0:
            for i in self.all_items:
                self.scale(i, event.x, event.y, 1.1, 1.1)
            self.gain_in += 1
        else:
            for i in self.all_items:
                self.scale(i, event.x, event.y, 0.9, 0.9)
            self.gain_out += 1

        for i in self.node_list:
            i.update_sockets()
