
### Comp 359 Assignment 3

**Link to Repository**: [GitHub - Comp-359-Assignment-3](https://github.com/haxetros/Comp-359-Assignment-3)  
**Link to Presentation**: [YouTube Presentation](https://www.youtube.com/watch?v=E-adoHkuse0)  

---

### Contributions:

| **Date Completed** | **Task**                           | **Elijah** | **Vibhu** |
|---------------------|------------------------------------|------------|-----------|
| Nov 17 - Nov 22     | Research                          | ✓          | ✓         |
| Nov 21              | Implementation (`spatial_hash_grid.py`) |            | ✓         |
| Nov 22              | Test code (`spatial_hash_grid_test.py`)  | ✓          |           |
| Nov 17 - Nov 23     | Report (`Report.docx`)            | ✓          | ✓         |
| Nov 22 - Nov 23     | Presentation                      | ✓          | ✓         |

---

## Spatial Hash Grid  

**Authors**: Elijah Duchak & Vibhu Dikshit  
**Date**: November 23, 2024  
**Course**: COMP-359-AB1  

---

## Overview

This project focuses on implementing a **Spatial Hash Grid**, a robust and efficient data structure designed for managing and querying objects within a 2D space. The implementation addresses the need for real-time dynamic environments, where objects frequently move and interact. Key highlights of the project include:
- Object management using a spatial hash grid for efficient storage and querying.
- Real-time object visualization with dynamic state updates.
- Live reporting of object states.

---

## Features  

1. **Efficient Spatial Hash Grid**:
   - Optimized storage and querying of objects in 2D space.
   - Reduces computational overhead by limiting the search to relevant grid cells.

2. **Real-Time Visualization**:
   - Built using `tkinter` for interactive visualization.
   - Objects are represented as labeled circles, changing color dynamically based on proximity:
     - **Blue**: Default state.
     - **Green**: Within the query radius.

3. **Dynamic Reporting**:
   - Real-time state updates displayed in a side panel.

4. **Comprehensive Testing**:
   - Unit tests to ensure functionality, accuracy, and robustness.

---

## Installation  

### Prerequisites:
- Python 3.7 or higher.
- Required libraries: `tkinter`, `unittest`.

### Steps:
1. Clone the repository:
   ```
   git clone https://github.com/haxetros/Comp-359-Assignment-3
   cd spatial-hash-grid
   ```
2. Run the application:
   ```
   python spatial_hash_grid.py
   ```
3. Run unit tests:
   ```
   python -m unittest test_spatial_hash_grid.py
   ```

---

## Code Structure  

### 1. **Client Class**
- Represents individual objects in the grid.
- Attributes:
  - `position`: The object's coordinates.
  - `dimensions`: Width and height of the object.
  - `name`: Unique identifier.

### 2. **SpatialHashGrid Class**
Manages:
- **Insertion**: Adds objects to the appropriate grid cells.
- **Queries**: Finds objects within a specified radius.
- **Updates**: Handles dynamic position changes.
- **Deletion**: Removes objects from the grid.

### 3. **SpatialHashGridVisualizer Class**
- Provides a graphical representation using `tkinter`.
- Features:
  - **Dynamic Movement**: Objects move in real-time.
  - **State Updates**: Objects turn green when within query radius.
  - **Reporting**: Displays object states in a side panel.

---

## Key Methods  

| **Method**            | **Description**                                   |
|-----------------------|---------------------------------------------------|
| `new_client`          | Creates and adds a new object to the grid.        |
| `insert_client`       | Inserts the object into relevant grid cells.      |
| `find_nearby`         | Finds objects within a query radius.              |
| `update_client`       | Updates an object's position.                     |
| `delete_client`       | Removes an object from the grid.                  |
| `add_random_objects`  | Adds multiple objects with random positions.      |
| `update_positions`    | Dynamically updates object positions.             |
| `update_report`       | Updates the state reporting panel.                |

---

## Testing  

**Framework**: Python's `unittest`.  

**Test Scenarios**:
1. **Insertion and Querying**: Verifies that objects are correctly added and queried.
2. **Position Updates**: Ensures dynamic updates are reflected in the grid.
3. **Deletion**: Confirms proper removal of objects from the grid.
4. **Overlapping Objects**: Handles multiple objects in the same grid cell.
5. **Boundary Conditions**: Tests edge cases and scenarios with no objects.

**Run Tests**:
```bash
python -m unittest test_spatial_hash_grid.py
```

---

## Performance Analysis  

| **Metric**             | **Naive Approach** | **Spatial Hash Grid**       |
|------------------------|--------------------|-----------------------------|
| **Space Complexity**   | O(n)              | O(n + m) ≈ O(n)             |
| **Time Complexity**    | O(n²)             | O(n)                        |

Where:
- **n**: Number of objects.
- **m**: Number of cells in the grid.

The spatial hash grid significantly reduces computational overhead, making it ideal for applications requiring real-time object management.

