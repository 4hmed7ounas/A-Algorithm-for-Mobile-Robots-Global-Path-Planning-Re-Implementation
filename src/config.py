"""Configuration parameters, paper benchmark scenarios, and published results.

Research Reference:
Haixiao Cao, Zijian Guo, Yonghong Zhang, Zhuheng Lu, and Liang Jiang.
'An Adaptive A* Algorithm for Mobile Robots Global Path Planning',
Electronics 2026, 15, 2807. https://doi.org/10.3390/electronics15132807
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Tuple

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results"
MAPS_DIR = RESULTS_DIR / "maps"
FIGURES_DIR = RESULTS_DIR / "figures"
TABLES_DIR = RESULTS_DIR / "tables"

# Ensure output directories exist
MAPS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
TABLES_DIR.mkdir(parents=True, exist_ok=True)


@dataclass(frozen=True)
class ScenarioConfig:
    map_size: Tuple[int, int]  # (height, width)
    env_type: str             # "irregular", "maze", "array"
    start_paper: Tuple[int, int]  # 1-based (x, y) as stated in paper
    goal_paper: Tuple[int, int]   # 1-based (x, y) as stated in paper
    description: str
    seed: int

    @property
    def start_0based(self) -> Tuple[int, int]:
        """Convert 1-based MATLAB/paper coordinates to 0-based Python indices."""
        return (self.start_paper[0] - 1, self.start_paper[1] - 1)

    @property
    def goal_0based(self) -> Tuple[int, int]:
        """Convert 1-based MATLAB/paper coordinates to 0-based Python indices."""
        return (self.goal_paper[0] - 1, self.goal_paper[1] - 1)


# Scenarios defined in paper Section 4.1 & 4.4
PAPER_SCENARIOS = {
    # 30x30 Irregular Outdoor
    "30x30_main": ScenarioConfig(
        map_size=(30, 30),
        env_type="irregular",
        start_paper=(2, 2),
        goal_paper=(28, 28),
        description="30x30 Irregular Outdoor Map - Main Trajectory (Table 2)",
        seed=3030,
    ),
    "30x30_reversed": ScenarioConfig(
        map_size=(30, 30),
        env_type="irregular",
        start_paper=(28, 28),
        goal_paper=(2, 2),
        description="30x30 Irregular Outdoor Map - Reversed (Table 5)",
        seed=3030,
    ),
    "30x30_random": ScenarioConfig(
        map_size=(30, 30),
        env_type="irregular",
        start_paper=(4, 24),
        goal_paper=(29, 2),
        description="30x30 Irregular Outdoor Map - Random Endpoints (Table 5)",
        seed=3030,
    ),

    # 60x60 Structured Indoor Maze
    "60x60_main": ScenarioConfig(
        map_size=(60, 60),
        env_type="maze",
        start_paper=(2, 2),
        goal_paper=(58, 58),
        description="60x60 Structured Indoor Maze - Main Trajectory (Table 3)",
        seed=6060,
    ),
    "60x60_reversed": ScenarioConfig(
        map_size=(60, 60),
        env_type="maze",
        start_paper=(58, 58),
        goal_paper=(2, 2),
        description="60x60 Structured Indoor Maze - Reversed (Table 5)",
        seed=6060,
    ),
    "60x60_random": ScenarioConfig(
        map_size=(60, 60),
        env_type="maze",
        start_paper=(4, 54),
        goal_paper=(59, 2),
        description="60x60 Structured Indoor Maze - Random Endpoints (Table 5)",
        seed=6060,
    ),

    # 100x100 Large Array-like (PV Station / Warehouse)
    "100x100_main": ScenarioConfig(
        map_size=(100, 100),
        env_type="array",
        start_paper=(2, 2),
        goal_paper=(99, 99),
        description="100x100 Large Array-like Scene - Main Trajectory (Table 4)",
        seed=100100,
    ),
}


# Published results directly transcribed from electronics-15-02807.pdf
PUBLISHED_TABLE_1_ABLATION = [
    # Map 30x30
    {"map": "30x30", "variant": "A* Baseline", "time_s": 0.04, "length_m": 40.41, "expanded_nodes": 130, "corners_ge_45": 9},
    {"map": "30x30", "variant": "Adaptive Estimation Function", "time_s": 0.03, "length_m": 40.20, "expanded_nodes": 118, "corners_ge_45": 13},
    {"map": "30x30", "variant": "Distance Model Optimization", "time_s": 0.02, "length_m": 41.45, "expanded_nodes": 45, "corners_ge_45": 9},
    {"map": "30x30", "variant": "Redundant Point Deletion", "time_s": 0.02, "length_m": 38.74, "expanded_nodes": 130, "corners_ge_45": 5},
    # Map 60x60
    {"map": "60x60", "variant": "A* Baseline", "time_s": 0.18, "length_m": 92.30, "expanded_nodes": 716, "corners_ge_45": 12},
    {"map": "60x60", "variant": "Adaptive Estimation Function", "time_s": 0.09, "length_m": 92.05, "expanded_nodes": 412, "corners_ge_45": 12},
    {"map": "60x60", "variant": "Distance Model Optimization", "time_s": 0.12, "length_m": 91.08, "expanded_nodes": 691, "corners_ge_45": 10},
    {"map": "60x60", "variant": "Redundant Point Deletion", "time_s": 0.12, "length_m": 87.49, "expanded_nodes": 691, "corners_ge_45": 7},
]

PUBLISHED_TABLE_2_30x30 = [
    {"algorithm": "A*", "time_s": 0.04, "length_m": 40.41, "expanded_nodes": 130, "corners_ge_45": 9},
    {"algorithm": "Dijkstra", "time_s": 0.14, "length_m": 40.30, "expanded_nodes": 632, "corners_ge_45": 11},
    {"algorithm": "Chen et al.", "time_s": 0.03, "length_m": 41.69, "expanded_nodes": 129, "corners_ge_45": 9},
    {"algorithm": "Bidirectional A*", "time_s": 0.03, "length_m": 42.65, "expanded_nodes": 156, "corners_ge_45": 9},
    {"algorithm": "Zhang et al.", "time_s": 0.04, "length_m": 40.29, "expanded_nodes": 98, "corners_ge_45": 11},
    {"algorithm": "Adaptive A*", "time_s": 0.01, "length_m": 39.72, "expanded_nodes": 36, "corners_ge_45": 7},
]

PUBLISHED_TABLE_3_60x60 = [
    {"algorithm": "A*", "time_s": 0.18, "length_m": 92.30, "expanded_nodes": 716, "corners_ge_45": 12},
    {"algorithm": "Dijkstra", "time_s": 0.39, "length_m": 92.10, "expanded_nodes": 1740, "corners_ge_45": 13},
    {"algorithm": "Chen et al.", "time_s": 0.12, "length_m": 92.08, "expanded_nodes": 696, "corners_ge_45": 12},
    {"algorithm": "Bidirectional A*", "time_s": 0.18, "length_m": 93.91, "expanded_nodes": 704, "corners_ge_45": 12},
    {"algorithm": "Zhang et al.", "time_s": 0.24, "length_m": 92.11, "expanded_nodes": 523, "corners_ge_45": 10},
    {"algorithm": "Adaptive A*", "time_s": 0.06, "length_m": 90.89, "expanded_nodes": 268, "corners_ge_45": 8},
]

PUBLISHED_TABLE_4_100x100 = [
    {"algorithm": "A*", "time_s": 0.70, "length_m": 146.56, "expanded_nodes": 2191, "corners_ge_45": 34},
    {"algorithm": "Dijkstra", "time_s": 1.93, "length_m": 146.41, "expanded_nodes": 7520, "corners_ge_45": 31},
    {"algorithm": "Chen et al.", "time_s": 0.52, "length_m": 146.56, "expanded_nodes": 2168, "corners_ge_45": 34},
    {"algorithm": "Bidirectional A*", "time_s": 0.38, "length_m": 148.38, "expanded_nodes": 1126, "corners_ge_45": 32},
    {"algorithm": "Zhang et al.", "time_s": 0.45, "length_m": 146.56, "expanded_nodes": 891, "corners_ge_45": 30},
    {"algorithm": "Adaptive A*", "time_s": 0.25, "length_m": 140.67, "expanded_nodes": 113, "corners_ge_45": 14},
]

PUBLISHED_TABLE_5_SENSITIVITY = [
    {"map": "30x30", "start": "(28, 28)", "goal": "(2, 2)", "algo": "A*", "time_s": 0.03, "length_m": 40.30, "expanded_nodes": 202, "corners_ge_45": 13},
    {"map": "30x30", "start": "(28, 28)", "goal": "(2, 2)", "algo": "Adaptive A*", "time_s": 0.01, "length_m": 39.92, "expanded_nodes": 43, "corners_ge_45": 6},
    {"map": "30x30", "start": "(4, 24)", "goal": "(29, 2)", "algo": "A*", "time_s": 0.04, "length_m": 38.21, "expanded_nodes": 250, "corners_ge_45": 14},
    {"map": "30x30", "start": "(4, 24)", "goal": "(29, 2)", "algo": "Adaptive A*", "time_s": 0.01, "length_m": 37.68, "expanded_nodes": 33, "corners_ge_45": 5},
    {"map": "60x60", "start": "(58, 58)", "goal": "(2, 2)", "algo": "A*", "time_s": 0.25, "length_m": 92.08, "expanded_nodes": 898, "corners_ge_45": 19},
    {"map": "60x60", "start": "(58, 58)", "goal": "(2, 2)", "algo": "Adaptive A*", "time_s": 0.04, "length_m": 88.81, "expanded_nodes": 123, "corners_ge_45": 7},
    {"map": "60x60", "start": "(4, 54)", "goal": "(59, 2)", "algo": "A*", "time_s": 0.41, "length_m": 118.49, "expanded_nodes": 1159, "corners_ge_45": 27},
    {"map": "60x60", "start": "(4, 54)", "goal": "(59, 2)", "algo": "Adaptive A*", "time_s": 0.13, "length_m": 114.96, "expanded_nodes": 478, "corners_ge_45": 13},
]
