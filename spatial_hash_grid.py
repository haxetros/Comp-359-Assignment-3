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


# Example usage (for testing):
if __name__ == "__main__":
    # Define grid bounds and dimensions
    bounds = [(0, 800), (0, 600)]
    dimensions = (10, 10)  # 10x10 grid

    # Initialize the spatial hash grid
    grid = SpatialHashGrid(bounds, dimensions)

    # Add some test clients
    client1 = grid.new_client((100, 150), (30, 30), "Client1")
    client2 = grid.new_client((400, 300), (50, 50), "Client2")

    # Query nearby objects
    nearby_objects = grid.find_nearby((120, 160), (100, 100))
    print("Nearby objects:", [obj.name for obj in nearby_objects])
