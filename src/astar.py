"""Modular Path Planning Search Engines.

Implements:
1. Conventional Baseline A* (with Euclidean distance heuristic)
2. Proposed Adaptive A* (Eqs. 5, 6, 7 from Cao et al. 2026):
   - Adaptive Estimation Weight: omega(n) = ln(1 + e^(d/D))
   - Optimized Distance Model: h_opt(n) = (Euclidean + Manhattan) / 2
   - Redundant Point Deletion: 3-node collinearity & line-of-sight shortcutting
3. Ablation study variants (adaptive weight only, distance model only, smoothing only)
4. Comparative Baselines (Dijkstra, Bidirectional A*)
"""

import math
import time
import heapq
from dataclasses import dataclass
from typing import List, Tuple, Dict, Set, Optional, Callable
from src.grid_map import GridMap
from src.smoother import delete_redundant_points
from src.metrics import compute_path_length, count_corners_ge_45


@dataclass
class SearchResult:
    """Encapsulates all results and performance metrics of a search run."""
    success: bool
    algorithm_name: str
    path: Optional[List[Tuple[int, int]]]
    raw_path: Optional[List[Tuple[int, int]]]
    path_length: float
    expanded_nodes: int
    runtime_seconds: float
    corners_ge_45: int
    closed_set: Set[Tuple[int, int]]


# Heuristic functions
def euclidean_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
    """Euclidean distance between two 2D points."""
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def manhattan_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
    """Manhattan (L1) distance between two 2D points."""
    return float(abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]))


def optimized_arithmetic_mean_distance(p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
    """
    Optimized distance model proposed in Eq. 7 of paper:
    Arithmetic mean of Euclidean distance and Manhattan distance.
    h(n) = (d_euclid + d_manhattan) / 2
    """
    d_e = euclidean_distance(p1, p2)
    d_m = manhattan_distance(p1, p2)
    return (d_e + d_m) / 2.0


def compute_adaptive_weight(current: Tuple[int, int], target: Tuple[int, int], start_to_target_dist: float) -> float:
    """
    Adaptive heuristic weight proposed in Eq. 6 of paper:
    omega(n) = ln(1 + e^(d / D))
    Where:
      d = distance between current node and target node
      D = distance between starting node and target node
    """
    if start_to_target_dist < 1e-9:
        return 1.0

    d = euclidean_distance(current, target)
    ratio = d / start_to_target_dist
    # Bound ratio to avoid floating point overflow
    ratio = min(ratio, 20.0)
    omega = math.log(1.0 + math.exp(ratio))
    return omega


def reconstruct_path(came_from: Dict[Tuple[int, int], Tuple[int, int]], current: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Reconstruct path from parent pointers."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def run_astar_search(
    grid: GridMap,
    start: Tuple[int, int],
    goal: Tuple[int, int],
    algorithm_type: str = "baseline_astar",
    apply_smoothing: bool = False,
    smoothing_mode: str = "multi_pass"
) -> SearchResult:
    """
    Execute modular graph search.

    Supported algorithm types:
    - "baseline_astar": f(n) = g(n) + h_euclid(n)
    - "adaptive_weight_only": f(n) = g(n) + omega(n) * h_euclid(n)
    - "distance_model_only": f(n) = g(n) + h_opt(n)
    - "proposed_adaptive_astar": f(n) = g(n) + omega(n) * h_opt(n)
    - "dijkstra": f(n) = g(n)  [h(n) = 0]
    """
    # Start timer (only timing the search algorithm)
    t0 = time.perf_counter()

    if not grid.is_free(start[0], start[1]) or not grid.is_free(goal[0], goal[1]):
        runtime = time.perf_counter() - t0
        return SearchResult(
            success=False,
            algorithm_name=algorithm_type,
            path=None,
            raw_path=None,
            path_length=0.0,
            expanded_nodes=0,
            runtime_seconds=runtime,
            corners_ge_45=0,
            closed_set=set()
        )

    # Initial start-to-goal distance D for adaptive weight
    initial_start_to_goal_dist = euclidean_distance(start, goal)

    # Priority Queue: (f_score, h_score, tie_breaker_counter, node)
    counter = 0
    open_heap = []
    
    # Heuristic and initial f-score for start
    if algorithm_type == "dijkstra":
        h_start = 0.0
        f_start = 0.0
    elif algorithm_type in ("distance_model_only", "proposed_adaptive_astar"):
        h_start = optimized_arithmetic_mean_distance(start, goal)
        omega = compute_adaptive_weight(start, goal, initial_start_to_goal_dist) if algorithm_type == "proposed_adaptive_astar" else 1.0
        f_start = omega * h_start
    elif algorithm_type == "adaptive_weight_only":
        h_start = euclidean_distance(start, goal)
        omega = compute_adaptive_weight(start, goal, initial_start_to_goal_dist)
        f_start = omega * h_start
    else:  # baseline_astar
        h_start = euclidean_distance(start, goal)
        f_start = h_start

    heapq.heappush(open_heap, (f_start, h_start, counter, start))
    counter += 1

    g_score: Dict[Tuple[int, int], float] = {start: 0.0}
    came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
    closed_set: Set[Tuple[int, int]] = set()
    open_set_nodes: Set[Tuple[int, int]] = {start}
    expanded_node_count = 0

    success = False
    raw_path = None

    while open_heap:
        current_f, current_h, _, current = heapq.heappop(open_heap)
        
        if current in closed_set:
            continue
        
        open_set_nodes.discard(current)
        closed_set.add(current)
        expanded_node_count += 1

        if current == goal:
            success = True
            raw_path = reconstruct_path(came_from, current)
            break

        current_g = g_score[current]

        for neighbor, move_cost in grid.get_neighbors(current, allow_diagonal=True, prevent_corner_cut=True):
            if neighbor in closed_set:
                continue

            tentative_g = current_g + move_cost

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g

                # Compute heuristic according to algorithm type
                if algorithm_type == "dijkstra":
                    h = 0.0
                    f = tentative_g
                elif algorithm_type in ("distance_model_only", "proposed_adaptive_astar"):
                    h = optimized_arithmetic_mean_distance(neighbor, goal)
                    if algorithm_type == "proposed_adaptive_astar":
                        omega = compute_adaptive_weight(neighbor, goal, initial_start_to_goal_dist)
                        f = tentative_g + omega * h
                    else:
                        f = tentative_g + h
                elif algorithm_type == "adaptive_weight_only":
                    h = euclidean_distance(neighbor, goal)
                    omega = compute_adaptive_weight(neighbor, goal, initial_start_to_goal_dist)
                    f = tentative_g + omega * h
                else:  # baseline_astar
                    h = euclidean_distance(neighbor, goal)
                    f = tentative_g + h

                heapq.heappush(open_heap, (f, h, counter, neighbor))
                counter += 1
                open_set_nodes.add(neighbor)

    # Post-processing / smoothing
    final_path = raw_path
    if success and raw_path is not None and apply_smoothing:
        final_path = delete_redundant_points(raw_path, grid, mode=smoothing_mode)

    runtime = time.perf_counter() - t0

    path_length = compute_path_length(final_path) if (success and final_path) else 0.0
    corners = count_corners_ge_45(final_path) if (success and final_path) else 0

    return SearchResult(
        success=success,
        algorithm_name=algorithm_type,
        path=final_path,
        raw_path=raw_path,
        path_length=path_length,
        expanded_nodes=expanded_node_count,
        runtime_seconds=round(runtime, 6),
        corners_ge_45=corners,
        closed_set=closed_set
    )


def run_bidirectional_astar(
    grid: GridMap,
    start: Tuple[int, int],
    goal: Tuple[int, int]
) -> SearchResult:
    """
    Bidirectional A* search implementation (forward from start, backward from goal)
    for direct comparison against published benchmarks.
    """
    t0 = time.perf_counter()

    if not grid.is_free(start[0], start[1]) or not grid.is_free(goal[0], goal[1]):
        runtime = time.perf_counter() - t0
        return SearchResult(
            success=False,
            algorithm_name="bidirectional_astar",
            path=None,
            raw_path=None,
            path_length=0.0,
            expanded_nodes=0,
            runtime_seconds=runtime,
            corners_ge_45=0,
            closed_set=set()
        )

    # Forward search structures
    f_open = []
    f_g = {start: 0.0}
    f_came_from = {}
    f_closed = set()
    counter_f = 0
    h_start = euclidean_distance(start, goal)
    heapq.heappush(f_open, (h_start, h_start, counter_f, start))
    counter_f += 1

    # Backward search structures
    b_open = []
    b_g = {goal: 0.0}
    b_came_from = {}
    b_closed = set()
    counter_b = 0
    h_goal = euclidean_distance(goal, start)
    heapq.heappush(b_open, (h_goal, h_goal, counter_b, goal))
    counter_b += 1

    meeting_node = None
    expanded_count = 0

    while f_open and b_open:
        # Step forward
        _, _, _, curr_f = heapq.heappop(f_open)
        if curr_f not in f_closed:
            f_closed.add(curr_f)
            expanded_count += 1

            if curr_f in b_closed:
                meeting_node = curr_f
                break

            for nbr, cost in grid.get_neighbors(curr_f, allow_diagonal=True, prevent_corner_cut=True):
                if nbr not in f_closed:
                    tent_g = f_g[curr_f] + cost
                    if nbr not in f_g or tent_g < f_g[nbr]:
                        f_g[nbr] = tent_g
                        f_came_from[nbr] = curr_f
                        h = euclidean_distance(nbr, goal)
                        heapq.heappush(f_open, (tent_g + h, h, counter_f, nbr))
                        counter_f += 1

        # Step backward
        _, _, _, curr_b = heapq.heappop(b_open)
        if curr_b not in b_closed:
            b_closed.add(curr_b)
            expanded_count += 1

            if curr_b in f_closed:
                meeting_node = curr_b
                break

            for nbr, cost in grid.get_neighbors(curr_b, allow_diagonal=True, prevent_corner_cut=True):
                if nbr not in b_closed:
                    tent_g = b_g[curr_b] + cost
                    if nbr not in b_g or tent_g < b_g[nbr]:
                        b_g[nbr] = tent_g
                        b_came_from[nbr] = curr_b
                        h = euclidean_distance(nbr, start)
                        heapq.heappush(b_open, (tent_g + h, h, counter_b, nbr))
                        counter_b += 1

    success = meeting_node is not None
    path = None
    if success:
        # Reconstruct path from start to meeting_node
        path_f = reconstruct_path(f_came_from, meeting_node)
        # Reconstruct path from goal to meeting_node, then invert
        path_b = reconstruct_path(b_came_from, meeting_node)
        # Combine
        path = path_f + list(reversed(path_b[:-1]))

    runtime = time.perf_counter() - t0
    path_len = compute_path_length(path) if (success and path) else 0.0
    corners = count_corners_ge_45(path) if (success and path) else 0

    return SearchResult(
        success=success,
        algorithm_name="bidirectional_astar",
        path=path,
        raw_path=path,
        path_length=path_len,
        expanded_nodes=expanded_count,
        runtime_seconds=round(runtime, 6),
        corners_ge_45=corners,
        closed_set=f_closed.union(b_closed)
    )
