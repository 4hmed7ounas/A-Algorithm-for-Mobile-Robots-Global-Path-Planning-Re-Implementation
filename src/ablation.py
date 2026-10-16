"""Ablation Study Runner matching Table 1 of Cao et al. (2026).

Evaluates the isolated impact of:
1. Baseline A*
2. Adaptive Estimation Function alone: f = g + omega(n) * h_euclid
3. Distance Model Optimization alone: f = g + h_opt
4. Redundant Point Deletion alone: Baseline A* + smoothing
5. Full Proposed Adaptive A*: f = g + omega(n) * h_opt + smoothing
"""

from typing import Dict, Tuple
from src.grid_map import GridMap
from src.astar import run_astar_search, SearchResult


def run_full_ablation_suite(
    grid: GridMap,
    start: Tuple[int, int],
    goal: Tuple[int, int]
) -> Dict[str, SearchResult]:
    """
    Execute all ablation configurations on a given grid map.
    """
    results = {}

    # 1. Baseline A*
    results["baseline_astar"] = run_astar_search(
        grid, start, goal,
        algorithm_type="baseline_astar",
        apply_smoothing=False
    )

    # 2. Adaptive Estimation Function alone
    results["adaptive_weight_only"] = run_astar_search(
        grid, start, goal,
        algorithm_type="adaptive_weight_only",
        apply_smoothing=False
    )

    # 3. Distance Model Optimization alone
    results["distance_model_only"] = run_astar_search(
        grid, start, goal,
        algorithm_type="distance_model_only",
        apply_smoothing=False
    )

    # 4. Redundant Point Deletion alone (applied to baseline A* path)
    results["smoothing_only"] = run_astar_search(
        grid, start, goal,
        algorithm_type="baseline_astar",
        apply_smoothing=True
    )

    # 5. Full Proposed Adaptive A* (Adaptive weight + Distance model + Smoothing)
    results["proposed_adaptive_astar"] = run_astar_search(
        grid, start, goal,
        algorithm_type="proposed_adaptive_astar",
        apply_smoothing=True
    )

    return results
