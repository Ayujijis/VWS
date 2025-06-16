import tkinter as tk
from UI.GamePanel import GamePanel


def main():
    root = tk.Tk()
    root.title("Virtual World Simulator")
    app = GamePanel(root)
    app.pack()
    root.mainloop()


if __name__ == "__main__":
    main()
