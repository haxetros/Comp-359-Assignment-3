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
    print("Nearby objects:", [obj.name for obj in grid.find_nearby((120, 160), (100, 100))])

    # Update a client's position
    print("\nUpdating Client1's position...")
    grid.update_client(client1, (200, 250))
    print("Nearby objects after update:", [obj.name for obj in grid.find_nearby((200, 250), (100, 100))])

    # Delete a client
    print("\nDeleting Client2...")
    grid.delete_client(client2)
    print("Nearby objects after deletion:", [obj.name for obj in grid.find_nearby((400, 300), (100, 100))])
