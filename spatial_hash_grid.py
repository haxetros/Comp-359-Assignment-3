import tkinter as tk
from tkinter import ttk
import random


class Client:
    """
    Represents an object (client) in the spatial hash grid.
    Attributes:
        position (tuple): (x, y) coordinates of the object.
        dimensions (tuple): Width and height of the object.
        name (str): Identifier for the object.
    """
    def __init__(self, position, dimensions, name):
        self.position = position
        self.dimensions = dimensions
        self.name = name
        self.indices = None  # Stores the range of grid cells the object occupies

    def __eq__(self, other):
        return isinstance(other, Client) and self.position == other.position and self.dimensions == other.dimensions

    def __hash__(self):
        return hash((self.position, self.dimensions, self.name))


class SpatialHashGrid:
    """
    Spatial Hash Grid to manage and query objects in a 2D space.
    """
    def __init__(self, bounds, dimensions):
        """
        Initializes the grid.
        Args:
            bounds (list of tuples): [(min_x, max_x), (min_y, max_y)] defines the grid's boundaries.
            dimensions (tuple): Number of cells in (x, y).
        """
        self.bounds = bounds  # Bounds of the grid
        self.dimensions = dimensions  # Number of cells along each axis
        self.cell_map = {}  # Dictionary to map cell keys to objects

    def new_client(self, position, dimensions, name):
        """
        Adds a new object to the grid.
        Args:
            position (tuple): (x, y) coordinates of the object.
            dimensions (tuple): Width and height of the object.
            name (str): Identifier for the object.
        Returns:
            Client: The created object.
        """
        client = Client(position, dimensions, name)
        self.insert_client(client)
        return client

    def insert_client(self, client):
        """
        Inserts a client into the appropriate cells based on its position and dimensions.
        """
        min_cell, max_cell = self.get_cell_range(client.position, client.dimensions)
        client.indices = (min_cell, max_cell)  # Track which cells the object occupies
        for x in range(min_cell[0], max_cell[0] + 1):
            for y in range(min_cell[1], max_cell[1] + 1):
                key = self.get_cell_key(x, y)
                if key not in self.cell_map:
                    self.cell_map[key] = set()
                self.cell_map[key].add(client)

    def find_nearby(self, position, dimensions):
        """
        Finds all objects near a given position within specified dimensions.
        Args:
            position (tuple): (x, y) coordinates of the query point.
            dimensions (tuple): Search area width and height.
        Returns:
            list: A list of nearby objects.
        """
        nearby = set()
        min_cell, max_cell = self.get_cell_range(position, dimensions)
        for x in range(min_cell[0], max_cell[0] + 1):
            for y in range(min_cell[1], max_cell[1] + 1):
                key = self.get_cell_key(x, y)
                if key in self.cell_map:
                    nearby.update(self.cell_map[key])
        return list(nearby)

    def update_client(self, client, new_position):
        """
        Updates the position of an existing client.
        Args:
            client (Client): The client to update.
            new_position (tuple): The new (x, y) coordinates for the client.
        """
        self.delete_client(client)  # Remove the client from its old cells
        client.position = new_position  # Update the client's position
        self.insert_client(client)  # Reinsert the client into the grid

    def delete_client(self, client):
        """
        Removes a client from the grid.
        Args:
            client (Client): The client to delete.
        """
        if not client.indices:
            return  # If the client has no assigned cells, do nothing
        min_cell, max_cell = client.indices
        for x in range(min_cell[0], max_cell[0] + 1):
            for y in range(min_cell[1], max_cell[1] + 1):
                key = self.get_cell_key(x, y)
                if key in self.cell_map:
                    self.cell_map[key].discard(client)  # Remove the client from the cell
                    if not self.cell_map[key]:  # If the cell is empty, delete it
                        del self.cell_map[key]
        client.indices = None  # Clear the client's cell indices

    def get_cell_range(self, position, dimensions):
        """
        Calculates the range of grid cells an object occupies.
        """
        min_x = int((position[0] - dimensions[0] / 2 - self.bounds[0][0]) // self.cell_width())
        max_x = int((position[0] + dimensions[0] / 2 - self.bounds[0][0]) // self.cell_width())
        min_y = int((position[1] - dimensions[1] / 2 - self.bounds[1][0]) // self.cell_height())
        max_y = int((position[1] + dimensions[1] / 2 - self.bounds[1][0]) // self.cell_height())
        return (min_x, min_y), (max_x, max_y)

    def get_cell_key(self, x, y):
        """
        Generates a unique key for each cell based on its (x, y) index.
        """
        return f"{x}.{y}"

    def cell_width(self):
        """
        Calculates the width of each grid cell.
        """
        return (self.bounds[0][1] - self.bounds[0][0]) / self.dimensions[0]

    def cell_height(self):
        """
        Calculates the height of each grid cell.
        """
        return (self.bounds[1][1] - self.bounds[1][0]) / self.dimensions[1]


class SpatialHashGridVisualizer:
    """
    Visualizes the spatial hash grid using tkinter.
    Includes object reporting and state visualization.
    """
    def __init__(self, grid, width, height):
        self.grid = grid
        self.width = width
        self.height = height
        self.root = tk.Tk()
        self.root.title("Spatial Hash Grid Visualization")

        # Top explanation frame
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)
        self.heading = tk.Label(self.top_frame, text="Spatial Hash Grid", font=("Arial", 18, "bold"))
        self.heading.pack(pady=5)
        self.explanation = tk.Label(
            self.top_frame,
            text=("This visualization demonstrates the use of a spatial hash grid for efficiently managing moving objects. "
                  "Objects are tracked in cells, allowing fast lookup for nearby items."),
            wraplength=600,
            justify="center",
        )
        self.explanation.pack(pady=5)

        # Left canvas for visualization
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg="white")
        self.canvas.pack(side=tk.LEFT)

        # Right panel for reporting
        self.right_frame = ttk.Frame(self.root, width=300, height=height)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.right_frame.pack_propagate(False)
        self.report_label = tk.Label(self.right_frame, text="Object States:", font=("Arial", 14, "bold"))
        self.report_label.pack(anchor="w", padx=10, pady=5)
        self.report = tk.Text(self.right_frame, height=25, wrap=tk.WORD)
        self.report.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.objects = []
        self.previous_states = {}  # Track previous color states by object name

    def add_random_objects(self, count):
        for i in range(count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(10, 30)
            obj = self.grid.new_client((x, y), (size, size), f"Obj-{i}")
            color = "blue"
            self.objects.append(
                (
                    obj,
                    self.canvas.create_oval(
                        x - size / 2,
                        y - size / 2,
                        x + size / 2,
                        y + size / 2,
                        fill=color,
                    ),
                    self.canvas.create_text(x, y, text=obj.name, fill="black"),
                )
            )
            self.previous_states[obj.name] = "blue"  # Initialize state by name

    def update_positions(self):
        for obj, oval, label in self.objects:
            dx = random.randint(-5, 5)
            dy = random.randint(-5, 5)
            new_x = min(max(obj.position[0] + dx, 0), self.width)
            new_y = min(max(obj.position[1] + dy, 0), self.height)
            self.grid.update_client(obj, (new_x, new_y))
            self.canvas.move(oval, dx, dy)
            self.canvas.move(label, dx, dy)

    def find_nearby(self, position, radius):
        nearby_objects = self.grid.find_nearby(position, (radius * 2, radius * 2))
        updated_states = {}
        for obj, oval, label in self.objects:
            if obj in nearby_objects:
                self.previous_states[obj.name] = "green"
                self.canvas.itemconfig(oval, fill="green")
            else:
                self.previous_states[obj.name] = "blue"
                self.canvas.itemconfig(oval, fill="blue")
            updated_states[obj.name] = self.previous_states[obj.name]
        self.update_report(updated_states)

    def update_report(self, states):
        self.report.delete(1.0, tk.END)
        for name, state in states.items():
            self.report.insert(tk.END, f"{name}: {state}\n")

    def run(self):
        def update_loop():
            self.update_positions()
            self.find_nearby((self.width // 2, self.height // 2), 100)
            self.root.after(100, update_loop)

        update_loop()
        self.root.mainloop()


if __name__ == "__main__":
    # Define grid bounds and dimensions
    bounds = [(0, 800), (0, 600)]
    dimensions = (10, 10)  # 10x10 grid
    grid = SpatialHashGrid(bounds, dimensions)

    visualizer = SpatialHashGridVisualizer(grid, 800, 600)
    visualizer.add_random_objects(30)
    visualizer.run()
