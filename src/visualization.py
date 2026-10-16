"""Visualization and High-Resolution Plotting Module.

Generates publication-quality figures mimicking Figures 5-12 of:
Cao et al., 'An Adaptive A* Algorithm for Mobile Robots Global Path Planning', Electronics 2026.
- Raster occupancy grid visualization (obstacles black, free space white, start red, destination blue)
- Path trajectories with waypoints and corner markings
- Expanded search tree / closed set heatmaps
- Side-by-side comparative ablation plots
- Metric comparison bar charts comparing published vs obtained results
"""

from pathlib import Path
from typing import List, Tuple, Optional, Dict
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

from src.grid_map import GridMap
from src.astar import SearchResult


def plot_grid_and_path(
    grid: GridMap,
    start: Tuple[int, int],
    goal: Tuple[int, int],
    path: Optional[List[Tuple[int, int]]] = None,
    closed_set: Optional[set] = None,
    title: str = "Path Planning Trajectory",
    save_path: Optional[Path] = None,
    figsize: Tuple[int, int] = (8, 8)
):
    """
    Plot a single grid map with start, goal, and planned path matching paper aesthetics.
    """
    fig, ax = plt.subplots(figsize=figsize, dpi=300)

    # Base grid: 0 = free (white), 1 = obstacle (black)
    grid_img = np.where(grid.obstacles, 0, 1)  # 0 is black, 1 is white

    ax.imshow(
        grid_img,
        cmap="gray",
        origin="lower",
        extent=(-0.5, grid.width - 0.5, -0.5, grid.height - 0.5),
        interpolation="nearest"
    )

    # Plot expanded/explored nodes if provided
    if closed_set:
        cx = [p[0] for p in closed_set]
        cy = [p[1] for p in closed_set]
        ax.scatter(cx, cy, s=12, c="#ffeaa7", alpha=0.35, marker="s", label="Expanded Nodes")

    # Plot path
    if path and len(path) > 1:
        px = [p[0] for p in path]
        py = [p[1] for p in path]
        ax.plot(px, py, color="#d63031", linewidth=2.5, zorder=4, label="Planned Path")
        ax.scatter(px, py, color="#e17055", s=18, zorder=5)

    # Plot start and goal
    ax.scatter([start[0]], [start[1]], color="#d63031", s=130, marker="o", edgecolors="black", linewidths=1.5, zorder=6, label=f"Start ({start[0]+1}, {start[1]+1})")
    ax.scatter([goal[0]], [goal[1]], color="#0984e3", s=130, marker="s", edgecolors="black", linewidths=1.5, zorder=6, label=f"Goal ({goal[0]+1}, {goal[1]+1})")

    ax.set_title(title, fontsize=13, fontweight="bold", pad=10)
    ax.set_xlabel("X Coordinate (Grid)", fontsize=11)
    ax.set_ylabel("Y Coordinate (Grid)", fontsize=11)
    ax.set_xlim(-0.5, grid.width - 0.5)
    ax.set_ylim(-0.5, grid.height - 0.5)
    ax.grid(True, which="both", color="#dfe6e9", linestyle=":", linewidth=0.5)
    ax.legend(loc="upper left", framealpha=0.9, fontsize=9)

    plt.tight_layout()
    if save_path:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")
    plt.close(fig)


def plot_ablation_quad_panel(
    grid: GridMap,
    start: Tuple[int, int],
    goal: Tuple[int, int],
    results: Dict[str, SearchResult],
    map_label: str,
    save_path: Optional[Path] = None
):
    """
    Plot 2x2 multi-panel figure replicating Figures 6 & 7 of the paper:
    (a) Conventional A*
    (b) Adaptive Estimation Function
    (c) Distance Model Optimization
    (d) Redundant Point Deletion (Proposed)
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 14), dpi=300)
    panels = [
        ("baseline_astar", "(a) Conventional A*", axes[0, 0]),
        ("adaptive_weight_only", "(b) Adaptive Estimation Function", axes[0, 1]),
        ("distance_model_only", "(c) Distance Model Optimization", axes[1, 0]),
        ("proposed_adaptive_astar", "(d) Proposed Adaptive A* (with Deletion)", axes[1, 1]),
    ]

    grid_img = np.where(grid.obstacles, 0, 1)

    for key, panel_title, ax in panels:
        res = results.get(key)
        ax.imshow(
            grid_img,
            cmap="gray",
            origin="lower",
            extent=(-0.5, grid.width - 0.5, -0.5, grid.height - 0.5),
            interpolation="nearest"
        )

        if res and res.closed_set:
            cx = [p[0] for p in res.closed_set]
            cy = [p[1] for p in res.closed_set]
            ax.scatter(cx, cy, s=8, c="#ffeaa7", alpha=0.35, marker="s")

        if res and res.path:
            px = [p[0] for p in res.path]
            py = [p[1] for p in res.path]
            ax.plot(px, py, color="#d63031", linewidth=2.2, zorder=4)
            ax.scatter(px, py, color="#e17055", s=14, zorder=5)

        ax.scatter([start[0]], [start[1]], color="#d63031", s=110, marker="o", edgecolors="black", zorder=6)
        ax.scatter([goal[0]], [goal[1]], color="#0984e3", s=110, marker="s", edgecolors="black", zorder=6)

        stats_str = f"Time: {res.runtime_seconds*1000:.1f}ms | Len: {res.path_length:.2f}m | Nodes: {res.expanded_nodes} | Turns: {res.corners_ge_45}" if res else ""
        ax.set_title(f"{panel_title}\n{stats_str}", fontsize=11, fontweight="bold")
        ax.grid(True, which="both", color="#dfe6e9", linestyle=":", linewidth=0.5)

    plt.suptitle(f"Ablation Study Comparison on {map_label} Map", fontsize=15, fontweight="bold", y=0.99)
    plt.tight_layout()
    if save_path:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")
    plt.close(fig)


def plot_metric_comparison_bars(
    df_comparison,
    save_path: Optional[Path] = None
):
    """
    Generate side-by-side grouped bar charts comparing published vs obtained results across metrics.
    """
    metrics = ["time_s", "length_m", "expanded_nodes", "corners_ge_45"]
    metric_labels = ["Planning Time (s)", "Path Length (m)", "Expanded Nodes", "Corners >= 45 deg"]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=300)
    axes = axes.flatten()

    for idx, (m, label) in enumerate(zip(metrics, metric_labels)):
        ax = axes[idx]
        x = np.arange(len(df_comparison))
        width = 0.35

        pub_vals = df_comparison[f"{m}_published"]
        our_vals = df_comparison[f"{m}_obtained"]

        ax.bar(x - width/2, pub_vals, width, label="Published (Cao et al. 2026)", color="#0984e3")
        ax.bar(x + width/2, our_vals, width, label="Our Independent Re-Implementation", color="#e84393")

        ax.set_title(label, fontsize=12, fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels(df_comparison["label"], rotation=18, ha="right", fontsize=9)
        ax.legend(fontsize=8)
        ax.grid(True, axis="y", linestyle="--", alpha=0.6)

    plt.suptitle("Experimental Benchmark Comparison: Published vs Obtained Results", fontsize=14, fontweight="bold")
    plt.tight_layout()
    if save_path:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
