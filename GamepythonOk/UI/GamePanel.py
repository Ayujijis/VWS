import tkinter as tk
import pickle
import random
from world.World import World
from organisms.animal.Sheep import Sheep
from organisms.animal.CyberSheep import CyberSheep
from organisms.animal.Human import Human
from organisms.animal.Wolf import Wolf
from organisms.animal.Fox import Fox
from organisms.animal.Antelope import Antelope
from organisms.animal.Turtle import Turtle
from organisms.plants.Hogweed import Hogweed
from organisms.plants.Grass import Grass
from organisms.plants.Guarana import Guarana
from organisms.plants.Belladonna import Belladonna
from organisms.plants.SowThistle import SowThistle
from world.Position import Position

CELL_SIZE = 30
GRID_WIDTH = 20
GRID_HEIGHT = 20
SAVE_FILE = "savegame.pkl"

class GamePanel(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.canvas = tk.Canvas(self, width=GRID_WIDTH*CELL_SIZE, height=GRID_HEIGHT*CELL_SIZE, bg="white")
        self.canvas.pack()

        self.log_box = tk.Text(self, height=6, width=60)
        self.log_box.pack()

        self.bind_keys()

        self.organism_images = {}
        self.load_images()

        self.new_game()

    def bind_keys(self):
        """Binds all user input keys."""
        self.master.bind("<Up>", lambda e: self.make_move(0, -1))
        self.master.bind("<Down>", lambda e: self.make_move(0, 1))
        self.master.bind("<Left>", lambda e: self.make_move(-1, 0))
        self.master.bind("<Right>", lambda e: self.make_move(1, 0))
        self.master.bind("h", lambda e: self.activate_human_ability())
        self.master.bind("s", lambda e: self.save_game())
        self.master.bind("l", lambda e: self.load_game())
        self.canvas.bind("<Button-2>", self.on_right_click)
        self.canvas.bind("<Button-3>", self.on_right_click)

    def unbind_keys(self):
        """Unbinds all user input keys to prevent actions after game over."""
        self.master.unbind("<Up>")
        self.master.unbind("<Down>")
        self.master.unbind("<Left>")
        self.master.unbind("<Right>")
        self.master.unbind("h")
        self.master.unbind("s")
        self.master.unbind("l")
        self.canvas.unbind("<Button-2>")
        self.canvas.unbind("<Button-3>")

    def load_images(self):
        """Loads images for each organism type."""
        organism_types = [Sheep, CyberSheep, Wolf, Fox, Antelope, Turtle, Human,
                          Grass, Guarana, Belladonna, SowThistle, Hogweed]
        for org_class in organism_types:
            if hasattr(org_class, 'IMAGE_FILE'):
                try:
                    image = tk.PhotoImage(file=getattr(org_class, 'IMAGE_FILE'))
                    self.organism_images[org_class] = image
                except tk.TclError as e:
                    print(f"Error loading image for {org_class.__name__}: {e}")

    def new_game(self):
        self.world = World(GRID_WIDTH, GRID_HEIGHT)
        self.human = Human(self.world, Position(8, 8))
        self.world.add_organism(self.human)
        self.seed_random_organisms(30)
        self.draw_world()

    def seed_random_organisms(self, count):
        organism_types = [Sheep, CyberSheep, Wolf, Fox, Antelope, Turtle,
                          Grass, Guarana, Belladonna, SowThistle, Hogweed]
        for _ in range(count):
            cls = random.choice(organism_types)
            for _ in range(100):
                x, y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
                pos = Position(x, y)
                if self.world.get_organism_at(pos) is None:
                    self.world.add_organism(cls(self.world, pos))
                    break

    def draw_world(self):
        """Draws the world grid and the organisms."""
        self.canvas.delete("all")
        for i in range(GRID_WIDTH):
            self.canvas.create_line(i * CELL_SIZE, 0, i * CELL_SIZE, GRID_HEIGHT * CELL_SIZE, fill="lightgray")
        for j in range(GRID_HEIGHT):
            self.canvas.create_line(0, j * CELL_SIZE, GRID_WIDTH * CELL_SIZE, j * CELL_SIZE, fill="lightgray")

        for organism in self.world.organisms:
            if organism.alive:
                x = organism.position.x * CELL_SIZE
                y = organism.position.y * CELL_SIZE
                org_image = self.organism_images.get(type(organism))
                if org_image:
                    self.canvas.create_image(x, y, image=org_image, anchor='nw')
                else:
                    self.canvas.create_rectangle(
                        x, y, x + CELL_SIZE, y + CELL_SIZE,
                        fill=organism.color, outline="black"
                    )

    def next_turn(self):
        """Processes a single game turn and checks for game over condition."""
        # Prevent turns if human is already dead
        if not self.human.alive:
            return

        self.world.organisms.sort(key=lambda o: (-o.initiative, -o.age))
        for organism in self.world.organisms[:]:
            if organism.alive:
                organism.increment_age()
                organism.action()
        self.update_log()
        self.draw_world()

        # Check if the human died during this turn
        if not self.human.alive:
            self.game_over()

    def game_over(self):
        """Handles the game over sequence."""
        self.unbind_keys()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        # Create a semi-transparent rectangle for better text visibility
        self.canvas.create_rectangle(0, 0, width, height, fill="black", stipple="gray50")
        self.canvas.create_text(
            width / 2, height / 2,
            text="GAME OVER",
            font=("Helvetica", 60, "bold"),
            fill="red"
        )
        # Schedule the window to close after 3 seconds
        self.master.after(3000, self.master.destroy)


    def make_move(self, dx, dy):
        new_x = self.human.position.x + dx
        new_y = self.human.position.y + dy
        new_pos = Position(new_x, new_y)
        if self.world.in_bounds(new_pos):
            target = self.world.get_organism_at(new_pos)
            if target:
                target.collision(self.human)
            elif target is None:
                self.world.move_organism(self.human, new_pos)
        self.next_turn()

    def update_log(self):
        self.log_box.delete(1.0, tk.END)
        for line in self.world.log_messages[-5:]:
            self.log_box.insert(tk.END, line + "\n")

    def activate_human_ability(self):
        self.human.activate_ability()
        self.next_turn()

    def save_game(self):
        with open(SAVE_FILE, "wb") as f:
            pickle.dump((self.world, self.human), f)
        self.world.log("Game saved.")
        self.update_log()

    def load_game(self):
        try:
            with open(SAVE_FILE, "rb") as f:
                self.world, self.human = pickle.load(f)
            # Re-bind keys in case a game was loaded from a game-over state
            self.bind_keys()
            self.draw_world()
            self.update_log()
            self.world.log("Game loaded.")
        except Exception as e:
            self.world.log(f"Failed to load game: {e}")
            self.update_log()

    def on_right_click(self, event):
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE
        pos = Position(x, y)
        if not self.world.in_bounds(pos) or self.world.get_organism_at(pos):
            return

        self.menu = tk.Menu(self, tearoff=0)
        options = [
            ("Sheep", Sheep), ("CyberSheep", CyberSheep), ("Wolf", Wolf), ("Fox", Fox), ("Antelope", Antelope), ("Turtle", Turtle),
            ("Grass", Grass), ("Guarana", Guarana), ("Belladonna", Belladonna), ("Sow Thistle", SowThistle), ("Hogweed", Hogweed)
        ]
        for name, cls in options:
            self.menu.add_command(label=name, command=lambda c=cls: self.spawn(c, pos))
        self.menu.tk_popup(event.x_root, event.y_root)

    def spawn(self, organism_class, pos):
        organism = organism_class(self.world, pos)
        self.world.add_organism(organism)
        self.world.log(f"Spawned {organism.__class__.__name__} at {pos.x},{pos.y}")
        self.draw_world()
        self.update_log()
