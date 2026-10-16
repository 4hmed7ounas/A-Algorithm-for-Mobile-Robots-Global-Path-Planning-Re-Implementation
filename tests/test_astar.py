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

    def test_10_start_equals_goal_public_api(self):
        """Test 10: Verify public API result structure and zero-division safety when start == goal."""
        grid = GridMap(10, 10)
        target = (3, 3)

        # Baseline A*
        res_base = run_astar_search(grid, target, target, algorithm_type="baseline_astar")
        self.assertTrue(res_base.success)
        self.assertEqual(res_base.path, [target])
        self.assertEqual(res_base.path_length, 0.0)
        self.assertEqual(res_base.corners_ge_45, 0)
        self.assertEqual(res_base.expanded_nodes, 1)

        # Proposed Adaptive A* with smoothing (D=0 edge case)
        res_adap = run_astar_search(
            grid, target, target,
            algorithm_type="proposed_adaptive_astar",
            apply_smoothing=True
        )
        self.assertTrue(res_adap.success)
        self.assertEqual(res_adap.path, [target])
        self.assertEqual(res_adap.path_length, 0.0)
        self.assertEqual(res_adap.corners_ge_45, 0)
        self.assertEqual(res_adap.expanded_nodes, 1)

    def test_11_heuristic_mathematical_properties(self):
        """Test 11: Mathematically verify Octile distance, Euclidean, and hybrid distance bounds."""
        # 1. Orthogonal displacement (dx=5, dy=0)
        dx, dy = 5, 0
        h_octile_ortho = (math.sqrt(2.0) - 1.0) * min(dx, dy) + max(dx, dy)
        h_e_ortho = euclidean_distance((0, 0), (dx, dy))
        h_opt_ortho = optimized_arithmetic_mean_distance((0, 0), (dx, dy))
        self.assertAlmostEqual(h_octile_ortho, 5.0)
        self.assertAlmostEqual(h_e_ortho, 5.0)
        self.assertAlmostEqual(h_opt_ortho, 5.0)

        # 2. Diagonal displacement (dx=5, dy=5)
        dx, dy = 5, 5
        h_octile_diag = (math.sqrt(2.0) - 1.0) * min(dx, dy) + max(dx, dy)
        h_e_diag = euclidean_distance((0, 0), (dx, dy))
        h_opt_diag = optimized_arithmetic_mean_distance((0, 0), (dx, dy))
        # Octile true distance is 5 * sqrt(2) ~ 7.071068
        self.assertAlmostEqual(h_octile_diag, 5.0 * math.sqrt(2.0))
        self.assertAlmostEqual(h_e_diag, 5.0 * math.sqrt(2.0))
        # h_opt is (5*sqrt(2) + 10) / 2 ~ 8.535534
        expected_h_opt = (5.0 * math.sqrt(2.0) + 10.0) / 2.0
        self.assertAlmostEqual(h_opt_diag, expected_h_opt)
        # Directly verify overestimation ratio of h_opt over true Octile distance: ~1.2071 (20.71%)
        ratio = h_opt_diag / h_octile_diag
        self.assertAlmostEqual(ratio, (math.sqrt(2.0) + 2.0) / (2.0 * math.sqrt(2.0)), places=4)
        self.assertGreater(h_opt_diag, h_octile_diag)

        # 3. Verify adaptive weight value at d=D
        omega_d_eq_D = compute_adaptive_weight((0, 0), (10, 0), 10.0)
        self.assertGreater(omega_d_eq_D, 1.0)
        self.assertAlmostEqual(omega_d_eq_D, math.log(1.0 + math.e), places=4)

    def test_12_smoothing_modes_and_collision_freedom(self):
        """Test 12: Verify that both single_pass and multi_pass smoothing produce collision-free paths."""
        from src.smoother import bresenham_line, delete_redundant_points

        grid = GridMap(12, 12)
        # Build an obstacle wall with an opening
        for y in range(2, 10):
            grid.set_obstacle(5, y, True)
        grid.set_obstacle(5, 5, False)  # Doorway

        res = run_astar_search(grid, (1, 5), (9, 5), algorithm_type="baseline_astar", apply_smoothing=False)
        self.assertTrue(res.success)
        raw_path = res.path

        for mode in ["single_pass", "multi_pass"]:
            with self.subTest(mode=mode):
                smoothed = delete_redundant_points(raw_path, grid, mode=mode)
                self.assertEqual(smoothed[0], (1, 5))
                self.assertEqual(smoothed[-1], (9, 5))
                # Verify collision freedom along every segment
                for i in range(len(smoothed) - 1):
                    segment_cells = bresenham_line(smoothed[i], smoothed[i + 1])
                    for cx, cy in segment_cells:
                        self.assertFalse(
                            grid.is_obstacle(cx, cy),
                            f"Collision in mode {mode} along segment {smoothed[i]}->{smoothed[i+1]} at ({cx}, {cy})"
                        )


if __name__ == "__main__":
    unittest.main()

