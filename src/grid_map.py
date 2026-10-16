"""2D Raster Grid Map Abstraction and Spatial Connectivity.

Represents environments for mobile robot global path planning.
Follows conventions from Cao et al. (MDPI Electronics 2026):
- Passable/Free area = False (displayed as white cells)
- Environmental Obstacle = True (displayed as black cells)
- 8-neighbor connectivity with geometric movement costs (1 for orthogonal, sqrt(2) for diagonal)
"""

import math
from pathlib import Path
from typing import List, Tuple, Union, Optional
import numpy as np


class GridMap:
    """Represents a 2D occupancy grid map."""

    def __init__(self, width: int, height: int, obstacles: Optional[np.ndarray] = None):
        self.width = int(width)
        self.height = int(height)
        if obstacles is not None:
            if obstacles.shape != (self.height, self.width):
                raise ValueError(f"Obstacle array shape {obstacles.shape} does not match dimensions ({self.height}, {self.width})")
            self.obstacles = obstacles.astype(bool)
        else:
            self.obstacles = np.zeros((self.height, self.width), dtype=bool)

    def in_bounds(self, x: int, y: int) -> bool:
        """Check if (x, y) is within grid boundaries."""
        return 0 <= x < self.width and 0 <= y < self.height

    def is_free(self, x: int, y: int) -> bool:
        """Check if (x, y) is within bounds and free of obstacles."""
        return self.in_bounds(x, y) and not bool(self.obstacles[y, x])

    def is_obstacle(self, x: int, y: int) -> bool:
        """Check if (x, y) is an obstacle or out of bounds."""
        if not self.in_bounds(x, y):
            return True
        return bool(self.obstacles[y, x])

    def set_obstacle(self, x: int, y: int, is_blocked: bool = True):
        """Set obstacle status for a cell."""
        if self.in_bounds(x, y):
            self.obstacles[y, x] = bool(is_blocked)
        else:
            raise IndexError(f"Cell ({x}, {y}) out of grid bounds ({self.width}, {self.height})")

    def get_neighbors(
        self,
        node: Tuple[int, int],
        allow_diagonal: bool = True,
        prevent_corner_cut: bool = True
    ) -> List[Tuple[Tuple[int, int], float]]:
        """
        Get valid neighbors and edge movement costs from the current node.
        
        Args:
            node: (x, y) coordinate
            allow_diagonal: If True, uses 8-neighbor connectivity; else 4-neighbor.
            prevent_corner_cut: If True, forbids diagonal movement if both adjacent orthogonal
                                cells are blocked, preventing clipping through obstacle corners.
                                
        Returns:
            List of ((nx, ny), cost)
        """
        x, y = node
        neighbors = []

        # 4 orthogonal directions (cost = 1.0)
        orthogonal_moves = [
            (x + 1, y, 1.0),
            (x - 1, y, 1.0),
            (x, y + 1, 1.0),
            (x, y - 1, 1.0),
        ]
        for nx, ny, cost in orthogonal_moves:
            if self.is_free(nx, ny):
                neighbors.append(((nx, ny), cost))

        if not allow_diagonal:
            return neighbors

        # 4 diagonal directions (cost = sqrt(2))
        sqrt2 = math.sqrt(2.0)
        diagonal_moves = [
            (x + 1, y + 1, sqrt2, (x + 1, y), (x, y + 1)),
            (x + 1, y - 1, sqrt2, (x + 1, y), (x, y - 1)),
            (x - 1, y + 1, sqrt2, (x - 1, y), (x, y + 1)),
            (x - 1, y - 1, sqrt2, (x - 1, y), (x, y - 1)),
        ]
        for nx, ny, cost, adj1, adj2 in diagonal_moves:
            if not self.is_free(nx, ny):
                continue
            if prevent_corner_cut:
                # If both orthogonal adjacent cells are obstacles, do not allow cutting corner
                if self.is_obstacle(adj1[0], adj1[1]) and self.is_obstacle(adj2[0], adj2[1]):
                    continue
            neighbors.append(((nx, ny), cost))

        return neighbors

    def save_npz(self, filepath: Union[str, Path]):
        """Save grid map to compressed .npz format."""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            path,
            width=self.width,
            height=self.height,
            obstacles=self.obstacles
        )

    @classmethod
    def load_npz(cls, filepath: Union[str, Path]) -> "GridMap":
        """Load grid map from compressed .npz format."""
        path = Path(filepath)
        data = np.load(path)
        return cls(
            width=int(data["width"]),
            height=int(data["height"]),
            obstacles=data["obstacles"]
        )

    @staticmethod
    def paper_to_grid(coord: Tuple[int, int]) -> Tuple[int, int]:
        """Convert 1-based MATLAB coordinates (x, y) to 0-based Python indices."""
        return (coord[0] - 1, coord[1] - 1)

    @staticmethod
    def grid_to_paper(coord: Tuple[int, int]) -> Tuple[int, int]:
        """Convert 0-based Python indices to 1-based MATLAB coordinates (x, y)."""
        return (coord[0] + 1, coord[1] + 1)
