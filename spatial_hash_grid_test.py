from spatial_hash_grid import SpatialHashGrid, Client
import unittest

class TestSpatialHashGrid(unittest.TestCase):
    def setUp(self):
        bounds = [(0, 100), (0, 100)]
        dimensions = (10, 10)
        self.grid = SpatialHashGrid(bounds, dimensions)

    def test_insert_and_find_client(self):
        client = self.grid.new_client((50, 50), (10, 10), 'TestClient')
        nearby = self.grid.find_nearby((50, 50), (10, 10))
        self.assertIn(client, nearby, "Client should be found near its own position.")

    def test_update_client_position(self):
        client = self.grid.new_client((50, 50), (5, 5), 'TestClient') 
        self.grid.update_client(client, (80, 80))
        nearby_old = self.grid.find_nearby((50, 50), (5, 5))
        nearby_new = self.grid.find_nearby((80, 80), (5, 5))
        self.assertNotIn(client, nearby_old, "Client should not be found at old position after update.")
        self.assertIn(client, nearby_new, "Client should be found at new position after update.")

    def test_delete_client(self):
        client = self.grid.new_client((50, 50), (10, 10), 'TestClient')
        self.grid.delete_client(client)
        nearby = self.grid.find_nearby((50, 50), (10, 10))
        self.assertNotIn(client, nearby, "Client should not be found after deletion.")

    def test_multiple_clients_in_same_cell(self):
        client1 = self.grid.new_client((20, 20), (10, 10), 'Client1')
        client2 = self.grid.new_client((25, 25), (10, 10), 'Client2')
        nearby = self.grid.find_nearby((22, 22), (10, 10))
        self.assertIn(client1, nearby, "Client1 should be found near position.")
        self.assertIn(client2, nearby, "Client2 should be found near position.")

    def test_clients_in_different_cells(self):
        client1 = self.grid.new_client((10, 10), (5, 5), 'Client1')
        client2 = self.grid.new_client((90, 90), (5, 5), 'Client2')
        nearby = self.grid.find_nearby((10, 10), (10, 10))
        self.assertIn(client1, nearby, "Client1 should be found near its position.")
        self.assertNotIn(client2, nearby, "Client2 should not be found near Client1.")

    def test_client_equality(self):
        client1 = Client((50, 50), (10, 10), 'Client1')
        client2 = Client((50, 50), (10, 10), 'Client2')
        self.assertEqual(client1, client2, "Clients with same position and dimensions should be equal.")

if __name__ == '__main__':
    unittest.main()
