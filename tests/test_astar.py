"""Comprehensive Unit Tests for Re-Implemented Algorithms and Data Structures."""

import math
import unittest
import numpy as np

from src.grid_map import GridMap
from src.metrics import compute_path_length, count_corners_ge_45
from src.smoother import is_collinear, is_line_free, delete_redundant_points
from src.astar import (
    run_astar_search,
    run_bidirectional_astar,
    euclidean_distance,
    manhattan_distance,
    optimized_arithmetic_mean_distance,
    compute_adaptive_weight,
)


class TestAStarReimplementation(unittest.TestCase):
    """Test suite for path planning foundation and proposed modifications."""

    def setUp(self):
        self.empty_grid = GridMap(10, 10)

    def test_01_empty_grid_pathfinding(self):
        """Test 1: A* finds optimal path on empty grid."""
        res = run_astar_search(self.empty_grid, (0, 0), (9, 9), algorithm_type="baseline_astar")
        self.assertTrue(res.success)
        self.assertIsNotNone(res.path)
        self.assertEqual(res.path[0], (0, 0))
        self.assertEqual(res.path[-1], (9, 9))
        # Pure diagonal path from (0,0) to (9,9) should have 10 nodes and length 9 * sqrt(2)
        expected_len = 9 * math.sqrt(2)
        self.assertAlmostEqual(res.path_length, expected_len, places=3)

    def test_02_completely_blocked_goal(self):
        """Test 2: A* returns success=False when goal is enclosed by obstacles."""
        grid = GridMap(10, 10)
        # Block all neighbors of (9, 9): (8, 9), (9, 8), (8, 8)
        grid.set_obstacle(8, 9, True)
        grid.set_obstacle(9, 8, True)
        grid.set_obstacle(8, 8, True)

        res = run_astar_search(grid, (0, 0), (9, 9), algorithm_type="baseline_astar")
        self.assertFalse(res.success)
        self.assertIsNone(res.path)
        self.assertEqual(res.path_length, 0.0)

    def test_03_diagonal_movement_cost(self):
        """Test 3: Verify diagonal movement edge cost is sqrt(2)."""
        nbrs = self.empty_grid.get_neighbors((5, 5))
        diagonal_nbrs = [c for n, c in nbrs if abs(n[0] - 5) == 1 and abs(n[1] - 5) == 1]
        self.assertEqual(len(diagonal_nbrs), 4)
        for cost in diagonal_nbrs:
            self.assertAlmostEqual(cost, math.sqrt(2.0), places=5)

    def test_04_obstacle_avoidance(self):
        """Test 4: Verify path circumvents a vertical wall obstacle."""
        grid = GridMap(10, 10)
        # Vertical wall from y=1 to y=8 at x=5
        for y in range(1, 9):
            grid.set_obstacle(5, y, True)

        res = run_astar_search(grid, (2, 5), (8, 5), algorithm_type="baseline_astar")
        self.assertTrue(res.success)
        for pt in res.path:
            self.assertFalse(grid.is_obstacle(pt[0], pt[1]))

    def test_05_path_reconstruction_endpoints(self):
        """Test 5: Verify first node is start and final node is goal."""
        res = run_astar_search(self.empty_grid, (1, 2), (7, 8))
        self.assertTrue(res.success)
        self.assertEqual(res.path[0], (1, 2))
        self.assertEqual(res.path[-1], (7, 8))

    def test_06_heuristic_and_adaptive_weight(self):
        """Test 6: Verify mathematical properties of optimized distance and adaptive weight."""
        p1 = (0, 0)
        p2 = (3, 4)
        # Euclidean: 5.0, Manhattan: 7.0, Arithmetic Mean: 6.0
        self.assertAlmostEqual(euclidean_distance(p1, p2), 5.0)
        self.assertAlmostEqual(manhattan_distance(p1, p2), 7.0)
        self.assertAlmostEqual(optimized_arithmetic_mean_distance(p1, p2), 6.0)

        # Adaptive weight omega(n) = ln(1 + e^(d/D))
        D = 10.0
        # At start d = D => omega = ln(1 + e^1) ~ 1.31326
        omega_start = compute_adaptive_weight((0, 0), (10, 0), D)
        self.assertAlmostEqual(omega_start, math.log(1.0 + math.e), places=4)

        # At goal d = 0 => omega = ln(1 + e^0) = ln(2) ~ 0.693147
        omega_goal = compute_adaptive_weight((10, 0), (10, 0), D)
        self.assertAlmostEqual(omega_goal, math.log(2.0), places=4)

    def test_07_redundant_point_deletion(self):
        """Test 7: Verify collinearity and 3-node redundant point deletion."""
        # Collinear line: (0,0) -> (1,1) -> (2,2)
        self.assertTrue(is_collinear((0, 0), (1, 1), (2, 2)))
        self.assertFalse(is_collinear((0, 0), (1, 2), (2, 2)))

        grid = GridMap(10, 10)
        collinear_path = [(0, 0), (1, 1), (2, 2), (3, 3)]
        smoothed = delete_redundant_points(collinear_path, grid)
        # Intermediate points should be deleted, leaving start and end
        self.assertEqual(smoothed, [(0, 0), (3, 3)])

        # Now test when obstacle blocks direct shortcut
        path_around_obstacle = [(0, 1), (1, 0), (2, 1)]
        grid.set_obstacle(1, 1, True)  # Block direct shortcut
        smoothed_blocked = delete_redundant_points(path_around_obstacle, grid)
        # Intermediate point should be preserved to avoid colliding
        self.assertEqual(smoothed_blocked, path_around_obstacle)

    def test_08_corner_counting(self):
        """Test 8: Verify corners with angle >= 45 degrees."""
        # Straight line: 0 corners
        straight_path = [(0, 0), (1, 1), (2, 2), (3, 3)]
        self.assertEqual(count_corners_ge_45(straight_path), 0)

        # 90-degree turn: (0,0) -> (2,0) -> (2,2)
        right_angle_path = [(0, 0), (2, 0), (2, 2)]
        self.assertEqual(count_corners_ge_45(right_angle_path), 1)

        # 45-degree turn: (0,0) -> (1,0) -> (2,1)
        turn_45_path = [(0, 0), (1, 0), (2, 1)]
        self.assertEqual(count_corners_ge_45(turn_45_path), 1)

    def test_09_all_search_variants_succeed(self):
        """Test 9: Verify all algorithm variants execute and find valid paths."""
        variants = [
            "baseline_astar",
            "adaptive_weight_only",
            "distance_model_only",
            "proposed_adaptive_astar",
            "dijkstra"
        ]
        grid = GridMap(15, 15)
        # Add a block obstacle
        grid.obstacles[4:9, 7:9] = True

        for v in variants:
            with self.subTest(algorithm=v):
                res = run_astar_search(grid, (2, 2), (12, 12), algorithm_type=v, apply_smoothing=(v == "proposed_adaptive_astar"))
                self.assertTrue(res.success, f"Algorithm {v} failed to find path")
                self.assertGreater(res.path_length, 0.0)
                self.assertGreater(res.expanded_nodes, 0)

        # Also test Bidirectional A*
        res_bi = run_bidirectional_astar(grid, (2, 2), (12, 12))
        self.assertTrue(res_bi.success)


if __name__ == "__main__":
    unittest.main()
