"""Evaluation Metrics for Mobile Robot Global Path Planning.

Implements the 4 official evaluation metrics defined in Section 4 of:
Cao et al., 'An Adaptive A* Algorithm for Mobile Robots Global Path Planning', Electronics 2026.
1. Planning Time (seconds)
2. Path Length (meters)
3. Number of Expanded / Traversed Nodes
4. Number of Corners with angle >= 45 degrees
"""

import math
from typing import List, Tuple
import numpy as np


def compute_path_length(path: List[Tuple[int, int]]) -> float:
    """
    Compute total geometric Euclidean path length across consecutive waypoints.
    For standard grid moves: orthogonal = 1.0 m, diagonal = sqrt(2) m.
    For smoothed shortcut segments: Euclidean segment length.
    """
    if not path or len(path) < 2:
        return 0.0

    total_length = 0.0
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        dist = math.hypot(x2 - x1, y2 - y1)
        total_length += dist

    return round(total_length, 4)


def count_corners_ge_45(path: List[Tuple[int, int]], angle_threshold_deg: float = 44.99) -> int:
    """
    Count the number of corners/directional changes along the path with angle >= 45 degrees.
    
    For 3 consecutive path points (p[k-1], p[k], p[k+1]), calculates the turning angle
    between incoming heading vector (p[k] - p[k-1]) and outgoing heading vector (p[k+1] - p[k]).
    """
    if not path or len(path) < 3:
        return 0

    corner_count = 0
    threshold_rad = math.radians(angle_threshold_deg)

    for i in range(1, len(path) - 1):
        p_prev = path[i - 1]
        p_curr = path[i]
        p_next = path[i + 1]

        v1_x = p_curr[0] - p_prev[0]
        v1_y = p_curr[1] - p_prev[1]
        v2_x = p_next[0] - p_curr[0]
        v2_y = p_next[1] - p_curr[1]

        mag1 = math.hypot(v1_x, v1_y)
        mag2 = math.hypot(v2_x, v2_y)

        if mag1 < 1e-9 or mag2 < 1e-9:
            continue

        # Cosine of the turning angle between headings
        dot = v1_x * v2_x + v1_y * v2_y
        cos_theta = dot / (mag1 * mag2)
        # Numerical clipping to prevent math domain error
        cos_theta = max(-1.0, min(1.0, cos_theta))
        theta_rad = math.acos(cos_theta)

        if theta_rad >= threshold_rad:
            corner_count += 1

    return corner_count
