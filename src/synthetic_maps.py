"""Deterministic Synthetic Map Generators matching Paper Environments.

Generates the 3 experimental environment categories described in Section 4.1:
1. Map 1 (30x30): Irregular outdoor scenes (irregular obstacle clusters)
2. Map 2 (60x60): Structured indoor scenes (mazes, corridors, wall segments)
3. Map 3 (100x100): Large array-like scenes (photovoltaic arrays / warehouse racks)

Ensures that all specified start and goal positions are guaranteed to be free and navigable.
"""

from typing import Tuple, List, Optional
import numpy as np
from src.grid_map import GridMap


def ensure_clearance(grid: GridMap, points_0based: List[Tuple[int, int]], radius: int = 1):
    """Ensure a circular or box clearance zone around designated critical points."""
    for px, py in points_0based:
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                nx, ny = px + dx, py + dy
                if grid.in_bounds(nx, ny):
                    grid.set_obstacle(nx, ny, False)


def generate_irregular_outdoor_30x30(
    seed: int = 3030,
    preserved_points_0based: Optional[List[Tuple[int, int]]] = None
) -> GridMap:
    """
    Generate 30x30 irregular outdoor environment matching Figure 5a.
    Features scattered, irregularly shaped obstacles of various dimensions.
    """
    rng = np.random.default_rng(seed)
    width, height = 30, 30
    grid = GridMap(width, height)

    # Place irregular clusters / rectangles
    num_obstacles = 16
    for _ in range(num_obstacles):
        ow = rng.integers(2, 6)
        oh = rng.integers(2, 6)
        ox = rng.integers(1, width - ow - 1)
        oy = rng.integers(1, height - oh - 1)
        grid.obstacles[oy:oy + oh, ox:ox + ow] = True

    # Add scattered single/double cells to mimic irregular outdoor terrain
    scatter_count = 20
    for _ in range(scatter_count):
        sx = rng.integers(1, width - 1)
        sy = rng.integers(1, height - 1)
        grid.set_obstacle(sx, sy, True)

    # Ensure critical endpoints are free
    if preserved_points_0based is None:
        # Default 30x30 paper points: (2,2), (28,28), (4,24), (29,2) in 1-based -> (1,1), (27,27), (3,23), (28,1)
        preserved_points_0based = [(1, 1), (27, 27), (3, 23), (28, 1)]

    ensure_clearance(grid, preserved_points_0based, radius=1)
    return grid


def generate_indoor_maze_60x60(
    seed: int = 6060,
    preserved_points_0based: Optional[List[Tuple[int, int]]] = None
) -> GridMap:
    """
    Generate 60x60 structured indoor maze/corridors matching Figure 5b.
    Features walls, partitioned corridors, and structured barriers.
    """
    rng = np.random.default_rng(seed)
    width, height = 60, 60
    grid = GridMap(width, height)

    # Create horizontal and vertical corridor walls with periodic door openings
    wall_spacing = 8
    # Vertical partition walls
    for wx in range(wall_spacing, width - 4, wall_spacing):
        grid.obstacles[3:height - 3, wx:wx + 2] = True
        # Create 2-3 doorways in each wall
        num_doors = rng.integers(2, 4)
        door_ys = rng.choice(range(5, height - 8), size=num_doors, replace=False)
        for dy in door_ys:
            grid.obstacles[dy:dy + 4, wx:wx + 2] = False

    # Horizontal connector walls
    for wy in range(wall_spacing, height - 4, wall_spacing):
        for wx in range(0, width - 4, wall_spacing * 2):
            if rng.random() > 0.35:
                w_len = rng.integers(6, wall_spacing + 2)
                grid.obstacles[wy:wy + 2, wx:min(width - 2, wx + w_len)] = True
                # Ensure a door
                door_x = rng.integers(wx, min(width - 2, wx + w_len))
                grid.obstacles[wy:wy + 2, door_x:min(width - 2, door_x + 3)] = False

    # Add several interior pillar obstacles
    for _ in range(25):
        px = rng.integers(2, width - 4)
        py = rng.integers(2, height - 4)
        pw = rng.integers(2, 4)
        ph = rng.integers(2, 4)
        grid.obstacles[py:py + ph, px:px + pw] = True

    # Ensure critical endpoints are free
    if preserved_points_0based is None:
        # 60x60 paper points: (2,2), (58,58), (4,54), (59,2) in 1-based -> (1,1), (57,57), (3,53), (58,1)
        preserved_points_0based = [(1, 1), (57, 57), (3, 53), (58, 1)]

    ensure_clearance(grid, preserved_points_0based, radius=2)
    return grid


def generate_array_scene_100x100(
    seed: int = 100100,
    preserved_points_0based: Optional[List[Tuple[int, int]]] = None
) -> GridMap:
    """
    Generate 100x100 large array-like scene matching Figure 5c.
    Represents photovoltaic panel arrays or dense warehouse shelving racks.
    """
    rng = np.random.default_rng(seed)
    width, height = 100, 100
    grid = GridMap(width, height)

    # Grid array blocks (e.g. 4x8 blocks arranged with aisles)
    block_w = 8
    block_h = 4
    aisle_x = 5
    aisle_y = 4

    for y in range(6, height - 8, block_h + aisle_y):
        for x in range(6, width - 8, block_w + aisle_x):
            # Sometimes leave an opening or missing array block (90% occupancy)
            if rng.random() < 0.90:
                grid.obstacles[y:y + block_h, x:x + block_w] = True

    # Ensure critical endpoints are free
    if preserved_points_0based is None:
        # 100x100 paper points: (2,2), (99,99) in 1-based -> (1,1), (98,98)
        preserved_points_0based = [(1, 1), (98, 98)]

    ensure_clearance(grid, preserved_points_0based, radius=3)
    return grid


def get_paper_map(scenario_key: str, seed: Optional[int] = None) -> GridMap:
    """Retrieve or generate the deterministic map for a specific scenario."""
    from src.config import PAPER_SCENARIOS

    scen = PAPER_SCENARIOS[scenario_key]
    actual_seed = seed if seed is not None else scen.seed

    if scen.env_type == "irregular":
        return generate_irregular_outdoor_30x30(seed=actual_seed)
    elif scen.env_type == "maze":
        return generate_indoor_maze_60x60(seed=actual_seed)
    elif scen.env_type == "array":
        return generate_array_scene_100x100(seed=actual_seed)
    else:
        raise ValueError(f"Unknown environment type: {scen.env_type}")
