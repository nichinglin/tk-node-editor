import tkinter as tk

from node_graphics_scene import NodeGraphicsScene


class NodeEditorWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # self.geometry("800x600")
        self.title("Node Editor Window")

        self.frame = tk.Frame(self)
        self.frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # create graphics scene
        self.view = NodeGraphicsScene(self.frame)
        self.view.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=3, pady=3)

        # # create graphics view
        # self.view = tk.Canvas(self.frame, bg="white")
        # self.view.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=3, pady=3)

        self.mainloop()


if __name__ == "__main__":
    app = NodeEditorWindow()
