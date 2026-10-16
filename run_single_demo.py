"""Single Scenario Demo and Trajectory Viewer.

Quick runner allowing students or evaluators to run any individual scenario,
print its live metrics, and optionally save or display the resulting trajectory.

Usage:
    python run_single_demo.py --scenario 30x30_main
    python run_single_demo.py --scenario 60x60_main
    python run_single_demo.py --scenario 100x100_main
"""

import argparse
from pathlib import Path
from src.config import PAPER_SCENARIOS, FIGURES_DIR
from src.synthetic_maps import get_paper_map
from src.astar import run_astar_search
from src.visualization import plot_grid_and_path


def main():
    parser = argparse.ArgumentParser(description="Run a single path planning demo.")
    parser.add_argument(
        "--scenario",
        type=str,
        default="30x30_main",
        choices=list(PAPER_SCENARIOS.keys()),
        help="Scenario identifier from paper benchmarks."
    )
    parser.add_argument(
        "--algorithm",
        type=str,
        default="proposed_adaptive_astar",
        choices=["baseline_astar", "adaptive_weight_only", "distance_model_only", "proposed_adaptive_astar", "dijkstra"],
        help="Path planning algorithm to execute."
    )
    args = parser.parse_args()

    scen = PAPER_SCENARIOS[args.scenario]
    print("=" * 70)
    print(f"RUNNING DEMO: {scen.description}")
    print(f"Algorithm:    {args.algorithm}")
    print(f"Map Size:     {scen.map_size[0]} x {scen.map_size[1]}")
    print(f"Start Point:  Paper {scen.start_paper} -> Python {scen.start_0based}")
    print(f"Goal Point:   Paper {scen.goal_paper} -> Python {scen.goal_0based}")
    print("=" * 70)

    grid = get_paper_map(args.scenario)
    apply_smoothing = (args.algorithm == "proposed_adaptive_astar")

    res = run_astar_search(
        grid,
        scen.start_0based,
        scen.goal_0based,
        algorithm_type=args.algorithm,
        apply_smoothing=apply_smoothing
    )

    print("\n--- RESULTS ---")
    print(f"Success:          {res.success}")
    print(f"Planning Time:    {res.runtime_seconds * 1000:.3f} ms ({res.runtime_seconds:.6f} s)")
    print(f"Path Length:      {res.path_length:.2f} meters")
    print(f"Expanded Nodes:   {res.expanded_nodes}")
    print(f"Corners (>= 45°): {res.corners_ge_45}")

    out_file = FIGURES_DIR / f"demo_{args.scenario}_{args.algorithm}.png"
    plot_grid_and_path(
        grid,
        scen.start_0based,
        scen.goal_0based,
        path=res.path,
        closed_set=res.closed_set,
        title=f"Demo: {scen.description} ({args.algorithm})",
        save_path=out_file
    )
    print(f"\nVisualization saved to: {out_file}")
    print("=" * 70)


if __name__ == "__main__":
    main()
