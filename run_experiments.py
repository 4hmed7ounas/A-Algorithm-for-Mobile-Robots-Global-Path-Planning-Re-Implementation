"""Main Experimental Reproduction and Benchmarking Pipeline.

Executes all experimental studies specified in the research paper:
1. Table 1 Ablation Study (30x30 and 60x60)
2. Tables 2, 3, 4 Algorithm Comparisons (30x30, 60x60, 100x100)
3. Table 5 Start/End Point Sensitivity Analysis
4. Multi-seed Monte Carlo Evaluation (10 seeds per scale) for Statistical Rigor
5. High-resolution figure generation and CSV export
"""

import sys
import time
from pathlib import Path
import pandas as pd
import numpy as np

from src.config import (
    MAPS_DIR, FIGURES_DIR, TABLES_DIR,
    PAPER_SCENARIOS,
    PUBLISHED_TABLE_1_ABLATION,
    PUBLISHED_TABLE_2_30x30,
    PUBLISHED_TABLE_3_60x60,
    PUBLISHED_TABLE_4_100x100,
    PUBLISHED_TABLE_5_SENSITIVITY,
)
from src.grid_map import GridMap
from src.synthetic_maps import (
    generate_irregular_outdoor_30x30,
    generate_indoor_maze_60x60,
    generate_array_scene_100x100
)
from src.astar import run_astar_search, run_bidirectional_astar, SearchResult
from src.ablation import run_full_ablation_suite
from src.visualization import (
    plot_grid_and_path,
    plot_ablation_quad_panel,
    plot_metric_comparison_bars
)


def run_table_1_ablation():
    """Execute ablation experiments matching Table 1."""
    print("\n" + "="*80)
    print("STEP 1: REPRODUCING TABLE 1 - ABLATION STUDY (30x30 & 60x60)")
    print("="*80)

    # 30x30 Map
    grid_30 = generate_irregular_outdoor_30x30(seed=3030)
    grid_30.save_npz(MAPS_DIR / "30x30_irregular_seed3030.npz")
    start_30 = (1, 1)  # (2, 2) in paper
    goal_30 = (27, 27)  # (28, 28) in paper
    results_30 = run_full_ablation_suite(grid_30, start_30, goal_30)

    plot_ablation_quad_panel(
        grid_30, start_30, goal_30, results_30,
        map_label="30x30 Irregular Outdoor",
        save_path=FIGURES_DIR / "fig6_ablation_30x30.png"
    )

    # 60x60 Map
    grid_60 = generate_indoor_maze_60x60(seed=6060)
    grid_60.save_npz(MAPS_DIR / "60x60_maze_seed6060.npz")
    start_60 = (1, 1)  # (2, 2) in paper
    goal_60 = (57, 57)  # (58, 58) in paper
    results_60 = run_full_ablation_suite(grid_60, start_60, goal_60)

    plot_ablation_quad_panel(
        grid_60, start_60, goal_60, results_60,
        map_label="60x60 Structured Indoor Maze",
        save_path=FIGURES_DIR / "fig7_ablation_60x60.png"
    )

    # Compile Table 1 comparison
    rows = []
    # 30x30 rows
    mapping = [
        ("30x30", "A* Baseline", "baseline_astar", results_30),
        ("30x30", "Adaptive Estimation Function", "adaptive_weight_only", results_30),
        ("30x30", "Distance Model Optimization", "distance_model_only", results_30),
        ("30x30", "Redundant Point Deletion", "smoothing_only", results_30),
        ("60x60", "A* Baseline", "baseline_astar", results_60),
        ("60x60", "Adaptive Estimation Function", "adaptive_weight_only", results_60),
        ("60x60", "Distance Model Optimization", "distance_model_only", results_60),
        ("60x60", "Redundant Point Deletion", "smoothing_only", results_60),
    ]

    for pub, (map_sz, variant_name, key, res_dict) in zip(PUBLISHED_TABLE_1_ABLATION, mapping):
        res = res_dict[key]
        rows.append({
            "Map": map_sz,
            "Variant": variant_name,
            "Pub Time (s)": pub["time_s"],
            "Our Time (s)": res.runtime_seconds,
            "Pub Len (m)": pub["length_m"],
            "Our Len (m)": res.path_length,
            "Pub Nodes": pub["expanded_nodes"],
            "Our Nodes": res.expanded_nodes,
            "Pub Corners": pub["corners_ge_45"],
            "Our Corners": res.corners_ge_45,
        })

    df = pd.DataFrame(rows)
    df.to_csv(TABLES_DIR / "table_1_ablation_comparison.csv", index=False)
    print(df.to_string(index=False))
    return results_30, results_60


def run_tables_2_3_4_algorithm_comparisons(results_30_ablation, results_60_ablation):
    """Execute algorithm comparison experiments matching Tables 2, 3, 4."""
    print("\n" + "="*80)
    print("STEP 2: REPRODUCING TABLES 2, 3, 4 - ALGORITHM BENCHMARKS")
    print("="*80)

    # 30x30 algorithms
    grid_30 = GridMap.load_npz(MAPS_DIR / "30x30_irregular_seed3030.npz")
    start_30 = (1, 1)
    goal_30 = (27, 27)

    dijkstra_30 = run_astar_search(grid_30, start_30, goal_30, algorithm_type="dijkstra")
    bidir_30 = run_bidirectional_astar(grid_30, start_30, goal_30)
    astar_30 = results_30_ablation["baseline_astar"]
    adaptive_30 = results_30_ablation["proposed_adaptive_astar"]

    # Save trajectory visualization
    plot_grid_and_path(
        grid_30, start_30, goal_30, path=adaptive_30.path, closed_set=adaptive_30.closed_set,
        title="30x30 Irregular Outdoor - Proposed Adaptive A* Path",
        save_path=FIGURES_DIR / "fig8_adaptive_astar_30x30.png"
    )

    # 60x60 algorithms
    grid_60 = GridMap.load_npz(MAPS_DIR / "60x60_maze_seed6060.npz")
    start_60 = (1, 1)
    goal_60 = (57, 57)

    dijkstra_60 = run_astar_search(grid_60, start_60, goal_60, algorithm_type="dijkstra")
    bidir_60 = run_bidirectional_astar(grid_60, start_60, goal_60)
    astar_60 = results_60_ablation["baseline_astar"]
    adaptive_60 = results_60_ablation["proposed_adaptive_astar"]

    plot_grid_and_path(
        grid_60, start_60, goal_60, path=adaptive_60.path, closed_set=adaptive_60.closed_set,
        title="60x60 Indoor Maze - Proposed Adaptive A* Path",
        save_path=FIGURES_DIR / "fig9_adaptive_astar_60x60.png"
    )

    # 100x100 Array Scene
    grid_100 = generate_array_scene_100x100(seed=100100)
    grid_100.save_npz(MAPS_DIR / "100x100_array_seed100100.npz")
    start_100 = (1, 1)  # (2, 2) in paper
    goal_100 = (98, 98)  # (99, 99) in paper

    astar_100 = run_astar_search(grid_100, start_100, goal_100, algorithm_type="baseline_astar")
    dijkstra_100 = run_astar_search(grid_100, start_100, goal_100, algorithm_type="dijkstra")
    bidir_100 = run_bidirectional_astar(grid_100, start_100, goal_100)
    adaptive_100 = run_astar_search(grid_100, start_100, goal_100, algorithm_type="proposed_adaptive_astar", apply_smoothing=True)

    plot_grid_and_path(
        grid_100, start_100, goal_100, path=adaptive_100.path, closed_set=adaptive_100.closed_set,
        title="100x100 Large Array Scene - Proposed Adaptive A* Path",
        save_path=FIGURES_DIR / "fig10_adaptive_astar_100x100.png"
    )

    # Compile benchmark table
    bench_data = [
        # 30x30
        ("30x30", "A*", astar_30, 0.04, 40.41, 130, 9),
        ("30x30", "Dijkstra", dijkstra_30, 0.14, 40.30, 632, 11),
        ("30x30", "Bidirectional A*", bidir_30, 0.03, 42.65, 156, 9),
        ("30x30", "Adaptive A*", adaptive_30, 0.01, 39.72, 36, 7),
        # 60x60
        ("60x60", "A*", astar_60, 0.18, 92.30, 716, 12),
        ("60x60", "Dijkstra", dijkstra_60, 0.39, 92.10, 1740, 13),
        ("60x60", "Bidirectional A*", bidir_60, 0.18, 93.91, 704, 12),
        ("60x60", "Adaptive A*", adaptive_60, 0.06, 90.89, 268, 8),
        # 100x100
        ("100x100", "A*", astar_100, 0.70, 146.56, 2191, 34),
        ("100x100", "Dijkstra", dijkstra_100, 1.93, 146.41, 7520, 31),
        ("100x100", "Bidirectional A*", bidir_100, 0.38, 148.38, 1126, 32),
        ("100x100", "Adaptive A*", adaptive_100, 0.25, 140.67, 113, 14),
    ]

    records = []
    for m_sz, algo_name, res, pub_t, pub_len, pub_nodes, pub_corn in bench_data:
        records.append({
            "Map Size": m_sz,
            "Algorithm": algo_name,
            "Pub Time (s)": pub_t,
            "Our Time (s)": res.runtime_seconds,
            "Time Diff (%)": round((res.runtime_seconds - pub_t) / pub_t * 100, 1) if pub_t > 0 else 0,
            "Pub Len (m)": pub_len,
            "Our Len (m)": res.path_length,
            "Len Diff (%)": round((res.path_length - pub_len) / pub_len * 100, 1),
            "Pub Nodes": pub_nodes,
            "Our Nodes": res.expanded_nodes,
            "Nodes Diff (%)": round((res.expanded_nodes - pub_nodes) / pub_nodes * 100, 1),
            "Pub Corners": pub_corn,
            "Our Corners": res.corners_ge_45,
            "Corners Diff": res.corners_ge_45 - pub_corn,
        })

    df_bench = pd.DataFrame(records)
    df_bench.to_csv(TABLES_DIR / "tables_2_3_4_algorithm_comparison.csv", index=False)
    print(df_bench.to_string(index=False))

    # Also build bar chart for Adaptive A* across the 3 scales
    chart_data = pd.DataFrame([
        {
            "label": "30x30 Adaptive A*",
            "time_s_published": 0.01, "time_s_obtained": adaptive_30.runtime_seconds,
            "length_m_published": 39.72, "length_m_obtained": adaptive_30.path_length,
            "expanded_nodes_published": 36, "expanded_nodes_obtained": adaptive_30.expanded_nodes,
            "corners_ge_45_published": 7, "corners_ge_45_obtained": adaptive_30.corners_ge_45
        },
        {
            "label": "60x60 Adaptive A*",
            "time_s_published": 0.06, "time_s_obtained": adaptive_60.runtime_seconds,
            "length_m_published": 90.89, "length_m_obtained": adaptive_60.path_length,
            "expanded_nodes_published": 268, "expanded_nodes_obtained": adaptive_60.expanded_nodes,
            "corners_ge_45_published": 8, "corners_ge_45_obtained": adaptive_60.corners_ge_45
        },
        {
            "label": "100x100 Adaptive A*",
            "time_s_published": 0.25, "time_s_obtained": adaptive_100.runtime_seconds,
            "length_m_published": 140.67, "length_m_obtained": adaptive_100.path_length,
            "expanded_nodes_published": 113, "expanded_nodes_obtained": adaptive_100.expanded_nodes,
            "corners_ge_45_published": 14, "corners_ge_45_obtained": adaptive_100.corners_ge_45
        },
    ])
    plot_metric_comparison_bars(chart_data, save_path=FIGURES_DIR / "metric_comparison_bars.png")


def run_table_5_sensitivity():
    """Execute sensitivity to endpoints matching Table 5."""
    print("\n" + "="*80)
    print("STEP 3: REPRODUCING TABLE 5 - SENSITIVITY TO ENDPOINTS")
    print("="*80)

    grid_30 = GridMap.load_npz(MAPS_DIR / "30x30_irregular_seed3030.npz")
    grid_60 = GridMap.load_npz(MAPS_DIR / "60x60_maze_seed6060.npz")

    cases = [
        # (Map, name, grid, start_paper, goal_paper)
        ("30x30", "Reversed: (28,28) -> (2,2)", grid_30, (28, 28), (2, 2)),
        ("30x30", "Random: (4,24) -> (29,2)", grid_30, (4, 24), (29, 2)),
        ("60x60", "Reversed: (58,58) -> (2,2)", grid_60, (58, 58), (2, 2)),
        ("60x60", "Random: (4,54) -> (59,2)", grid_60, (4, 54), (59, 2)),
    ]

    records = []
    for (m_sz, case_desc, grid, s_pap, g_pap), pub_row in zip(cases, [PUBLISHED_TABLE_5_SENSITIVITY[i] for i in [0, 2, 4, 6]]):
        s_0 = (s_pap[0] - 1, s_pap[1] - 1)
        g_0 = (g_pap[0] - 1, g_pap[1] - 1)

        res_astar = run_astar_search(grid, s_0, g_0, algorithm_type="baseline_astar")
        res_adaptive = run_astar_search(grid, s_0, g_0, algorithm_type="proposed_adaptive_astar", apply_smoothing=True)

        records.append({
            "Map": m_sz,
            "Case": case_desc,
            "Algorithm": "A*",
            "Our Time (s)": res_astar.runtime_seconds,
            "Our Len (m)": res_astar.path_length,
            "Our Nodes": res_astar.expanded_nodes,
            "Our Corners": res_astar.corners_ge_45,
        })
        records.append({
            "Map": m_sz,
            "Case": case_desc,
            "Algorithm": "Adaptive A*",
            "Our Time (s)": res_adaptive.runtime_seconds,
            "Our Len (m)": res_adaptive.path_length,
            "Our Nodes": res_adaptive.expanded_nodes,
            "Our Corners": res_adaptive.corners_ge_45,
        })

    df_sens = pd.DataFrame(records)
    df_sens.to_csv(TABLES_DIR / "table_5_sensitivity_comparison.csv", index=False)
    print(df_sens.to_string(index=False))


def run_monte_carlo_statistical_evaluation(num_seeds: int = 10):
    """
    Run 10 independent random seeds for each map scale to obtain rigorous
    statistical evidence (Mean +/- Std) for the Critical Analysis.
    """
    print("\n" + "="*80)
    print(f"STEP 4: MONTE CARLO STATISTICAL EVALUATION ({num_seeds} SEEDS PER SCALE)")
    print("="*80)

    mc_results = []
    scales = [
        ("30x30", (1, 1), (27, 27), generate_irregular_outdoor_30x30),
        ("60x60", (1, 1), (57, 57), generate_indoor_maze_60x60),
        ("100x100", (1, 1), (98, 98), generate_array_scene_100x100),
    ]

    for scale_name, start, goal, gen_func in scales:
        print(f"Running Monte Carlo on {scale_name}...")
        for seed_idx in range(num_seeds):
            seed = 1000 + seed_idx * 73
            grid = gen_func(seed=seed)

            # Baseline A*
            res_a = run_astar_search(grid, start, goal, algorithm_type="baseline_astar")
            # Adaptive A*
            res_adap = run_astar_search(grid, start, goal, algorithm_type="proposed_adaptive_astar", apply_smoothing=True)

            mc_results.append({
                "Map": scale_name,
                "Seed": seed,
                "A*_Time": res_a.runtime_seconds,
                "Adap_Time": res_adap.runtime_seconds,
                "A*_Length": res_a.path_length,
                "Adap_Length": res_adap.path_length,
                "A*_Nodes": res_a.expanded_nodes,
                "Adap_Nodes": res_adap.expanded_nodes,
                "A*_Corners": res_a.corners_ge_45,
                "Adap_Corners": res_adap.corners_ge_45,
                "Node_Reduction_%": (res_a.expanded_nodes - res_adap.expanded_nodes) / res_a.expanded_nodes * 100 if res_a.expanded_nodes > 0 else 0,
                "Corner_Reduction_%": (res_a.corners_ge_45 - res_adap.corners_ge_45) / res_a.corners_ge_45 * 100 if res_a.corners_ge_45 > 0 else 0,
            })

    df_mc = pd.DataFrame(mc_results)
    df_mc.to_csv(TABLES_DIR / "monte_carlo_raw_runs.csv", index=False)

    # Summarize Mean +/- Std
    summary_rows = []
    for scale_name in ["30x30", "60x60", "100x100"]:
        sub = df_mc[df_mc["Map"] == scale_name]
        summary_rows.append({
            "Map Size": scale_name,
            "A* Nodes (Mean±Std)": f"{sub['A*_Nodes'].mean():.1f} ± {sub['A*_Nodes'].std():.1f}",
            "Adap Nodes (Mean±Std)": f"{sub['Adap_Nodes'].mean():.1f} ± {sub['Adap_Nodes'].std():.1f}",
            "Node Reduction (%)": f"{sub['Node_Reduction_%'].mean():.1f}%",
            "A* Length (Mean±Std)": f"{sub['A*_Length'].mean():.2f} ± {sub['A*_Length'].std():.2f}",
            "Adap Length (Mean±Std)": f"{sub['Adap_Length'].mean():.2f} ± {sub['Adap_Length'].std():.2f}",
            "A* Corners (Mean±Std)": f"{sub['A*_Corners'].mean():.1f} ± {sub['A*_Corners'].std():.1f}",
            "Adap Corners (Mean±Std)": f"{sub['Adap_Corners'].mean():.1f} ± {sub['Adap_Corners'].std():.1f}",
            "Corner Reduction (%)": f"{sub['Corner_Reduction_%'].mean():.1f}%",
        })

    df_summary = pd.DataFrame(summary_rows)
    df_summary.to_csv(TABLES_DIR / "monte_carlo_statistical_summary.csv", index=False)
    print("\nSTATISTICAL SUMMARY (Mean +/- Std across 10 random seeds):")
    print(df_summary.to_string(index=False))


def main():
    print("="*80)
    print("STARTING COMPLETE RESEARCH PAPER RE-IMPLEMENTATION EXPERIMENTS")
    print("Paper: 'An Adaptive A* Algorithm for Mobile Robots Global Path Planning'")
    print("="*80)

    res_30, res_60 = run_table_1_ablation()
    run_tables_2_3_4_algorithm_comparisons(res_30, res_60)
    run_table_5_sensitivity()
    run_monte_carlo_statistical_evaluation(num_seeds=10)

    print("\n" + "="*80)
    print("ALL EXPERIMENTS SUCCESSFULLY EXECUTED AND ARTIFACTS GENERATED!")
    print(f"Maps saved to: {MAPS_DIR}")
    print(f"Figures saved to: {FIGURES_DIR}")
    print(f"Tables saved to: {TABLES_DIR}")
    print("="*80)


if __name__ == "__main__":
    main()
