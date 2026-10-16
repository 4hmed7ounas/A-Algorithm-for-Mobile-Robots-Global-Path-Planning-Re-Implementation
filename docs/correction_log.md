# Research Audit Correction Log: Adaptive A* Re-Implementation

**Project:** Reproduction and Implementation Study of *"An Adaptive A\* Algorithm for Mobile Robots Global Path Planning"* (Cao et al., *MDPI Electronics*, 2026, 15(13), 2807)  
**Author:** Ahmed Younas (MS AI, Advanced Artificial Intelligence)  
**Date of Audit & Corrections:** October 2026  
**Status:** Completed & Fully Verified  

---

## 1. Executive Summary

Following a comprehensive audit of the clean-room Python re-implementation, all identified theoretical, empirical, and documentation findings (F-01 through F-07) were addressed in accordance with the five-phase correction plan and the four user-mandated adjustments:
1. **Mathematical Rigor & Suboptimality Framing:** Rather than treating inadmissibility as proof of an unproven $\epsilon$-suboptimality guarantee, the algorithm is formally characterized as a *dynamically weighted, potentially suboptimal heuristic search*. Empirical testing across 100 random $20\times 20$ grid scenarios establishes that raw Adaptive A* produced longer paths than Baseline A* in 20 tested instances, reflecting a deliberate engineering trade-off of shortest-path optimality for 62%–71% fewer node expansions and faster convergence.
2. **Identifiable Paper-Faithful Architecture & Configurable Smoothing:** Smoothing was made configurable via `mode="multi_pass"` (default, iterative convergence) and `mode="single_pass"` (single sequential pass). The default preserves existing project benchmarks while allowing direct comparison to the published corner counts.
3. **Rigorous Targeted Edge-Case Testing:** Added three dedicated unit tests to `tests/test_astar.py` (Tests 10, 11, and 12) covering public API integrity on `start == goal` (zero-division safety), direct mathematical verification of the Octile distance relationship, and Bresenham collision-free verification across both single-pass and multi-pass smoothing.
4. **Preservation of Research Integrity & PDF Citation Verification:** Published values from Cao et al. [2] were independently verified directly against the supplied PDF article (`electronics-15-02807.pdf`) with exact table, row, and page citations documented. Published metrics are explicitly distinguished from our synthetic experiment metrics. Tracking of Python bytecode cache (`__pycache__/*.pyc`) was removed from the Git index and `.gitignore` was established. No Git commits or pushes were executed without user authorization.

---

## 2. Itemized Resolution of Audit Findings

### Finding F-01: Discrepancy Between Table 1 and Table 2 Corner Counts in the Published Paper
* **Root Cause:** Table 1 (Page 11) reports 5 corners for the full Adaptive A* algorithm on the $30\times 30$ map, whereas Table 2 (Page 13) reports 7 corners for the exact same algorithm on the same map.
* **Correction Executed:**
  - Verified against `electronics-15-02807.pdf` (Page 11, Table 1 vs. Page 13, Table 2).
  - Updated `docs/final_audit_report.md` (Finding F-01) and `docs/assumptions.md` to document this published discrepancy.
  - In `report/ieee_technical_report.md`, explicitly noted both values in the discussion, distinguishing Table 1's ablation entry from Table 2's benchmark entry.

### Finding F-02: Overestimation of Octile Distance & Heuristic Inadmissibility
* **Root Cause:** The hybrid distance heuristic $h_{\text{opt}}(n) = (d_{\text{euclid}} + d_{\text{manhattan}})/2$ overestimates true 8-connected grid Octile distance by up to 20.71% along diagonal directions ($\Delta x = \Delta y$). Furthermore, dynamic weighting $\omega(n) = \ln(1 + e^{d/D}) > 1.0$ for $d/D > 0.5413$, peaking at $\approx 1.313$. With closed nodes permanently locked without reopening, shortest-path optimality cannot be guaranteed.
* **Correction Executed:**
  - Formally derived Octile distance $h^*(n) = (\sqrt{2}-1)\min(\Delta x,\Delta y) + \max(\Delta x,\Delta y)$ and the 20.71% diagonal overestimation in `docs/assumptions.md` and Section III-C of `report/ieee_technical_report.md`.
  - Reframed the algorithm as a *dynamically weighted, potentially suboptimal heuristic search*.
  - Removed all unsupported claims of $\epsilon$-suboptimality bounds.
  - Added empirical verification: raw Adaptive A* produced longer paths than Baseline A* in 20 out of 100 random $20\times 20$ grid instances before post-processing smoothing.
  - Added Test 11 in `tests/test_astar.py` to directly test the mathematical inequalities ($h_{\text{euclid}} \le h^*$, $h^* \le h_{\text{opt}}$, and the 20.71% diagonal ratio).

### Finding F-03: Redundant Point Deletion Single-Pass vs. Multi-Pass Ambiguity
* **Root Cause:** Section 3.3, Step 4 of the published paper states: *"Inspect all the nodes in the path node set and eliminate all superfluous nodes..."*, leaving open whether this is a single sequential pass or an iterative convergence loop.
* **Correction Executed:**
  - Enhanced `src/smoother.py` and `src/astar.py` with a configurable `mode` parameter: `mode="multi_pass"` (default, up to 5 iterative convergence passes) and `mode="single_pass"` (single sequential pass).
  - Documented the empirical performance of both modes:
    - On $30\times 30$: Multi-pass yields 1 corner (38.44 m); Single-pass yields 3 corners (39.16 m); Raw yields 7 corners (39.70 m); Published Table 2 reports 7 corners (39.72 m).
    - On $60\times 60$: Multi-pass yields 2 corners (86.22 m); Single-pass yields 9 corners (89.66 m); Raw yields 17 corners (90.91 m); Published Table 3 reports 8 corners (90.89 m).
    - On $100\times 100$: Multi-pass yields 4 corners (144.58 m); Single-pass yields 4 corners (144.58 m); Raw yields 21 corners (145.40 m); Published Table 4 reports 14 corners (140.67 m).
  - Added Test 12 in `tests/test_astar.py` verifying that both smoothing modes produce collision-free paths.

### Finding F-04: Start-Equals-Goal Edge Case Safety
* **Root Cause:** When `start == goal`, Euclidean distance $D = 0$, risking a potential `ZeroDivisionError` in $\omega(n) = \ln(1 + e^{d/D})$.
* **Correction Executed:**
  - Verified that `src/astar.py` guards against $D = 0$ by clamping `D = max(D, 1e-6)` and immediately returning a valid single-node path when `start == goal`.
  - Added Test 10 in `tests/test_astar.py` validating the public API result structure (`success=True`, `path=[(x, y)]`, `path_length=0.0`, `expanded_nodes=0`, `corners=0`) and verifying no division-by-zero occurs.

### Finding F-05: Untracked Bytecode & Missing `.gitignore`
* **Root Cause:** Python compiled bytecode files (`.pyc`) under `src/__pycache__` and `tests/__pycache__` were tracked in the Git staging index.
* **Correction Executed:**
  - Created root `.gitignore` ignoring `__pycache__/`, `*.pyc`, `*.pyo`, `.pytest_cache/`, and `.coverage`.
  - Removed all cached `.pyc` files from the Git staging index via `git rm --cached`.

### Finding F-06: Statistical Notation in Monte Carlo Evaluation
* **Root Cause:** Standard deviation reporting in Table IV lacked explicit notation regarding whether it represented population or sample standard deviation, and degrees of freedom.
* **Correction Executed:**
  - Updated Table IV title and notes in `report/ieee_technical_report.md` to: `Sample Mean ± Sample Standard Deviation (s, N = 10, ddof = 1) across 10 synthetic map instances per scale`.

### Finding F-07: Verification of Published Reference Values Against PDF
* **Root Cause:** Published benchmark values in `src/config.py` needed independent verification against the original PDF (`electronics-15-02807.pdf`) rather than self-referential acceptance.
* **Correction Executed:**
  - Inspected `electronics-15-02807.pdf` directly.
  - Documented exact locations:
    - Table 1 (Page 11): Ablation study ($30\times 30$ and $60\times 60$).
    - Table 2 (Page 13): $30\times 30$ benchmarks (A*: 0.04s, 40.41m, 130 nodes, 9 corners; Adaptive A*: 0.01s, 39.72m, 36 nodes, 7 corners).
    - Table 3 (Page 13): $60\times 60$ benchmarks (A*: 0.18s, 92.30m, 716 nodes, 12 corners; Adaptive A*: 0.06s, 90.89m, 268 nodes, 8 corners).
    - Table 4 (Page 14): $100\times 100$ benchmarks (A*: 0.70s, 146.56m, 2191 nodes, 34 corners; Adaptive A*: 0.25s, 140.67m, 113 nodes, 14 corners).
    - Table 5 (Page 15): Sensitivity across reversed and random endpoints.
  - Updated Section VII in `report/ieee_technical_report.md` with explicit page and table citations.

---

## 3. Test Suite & Verification Results

### Unit Test Execution (`tests/test_astar.py`)
Ran `python -m unittest discover -s tests -v`:
```
test_01_empty_grid_pathfinding ... ok
test_02_completely_blocked_goal ... ok
test_03_diagonal_movement_cost ... ok
test_04_obstacle_avoidance ... ok
test_05_path_reconstruction_endpoints ... ok
test_06_heuristic_and_adaptive_weight ... ok
test_07_redundant_point_deletion ... ok
test_08_corner_counting ... ok
test_09_all_search_variants_succeed ... ok
test_10_start_equals_goal_public_api ... ok
test_11_heuristic_mathematical_properties ... ok
test_12_smoothing_modes_and_collision_freedom ... ok

Ran 12 tests in 0.008s
OK
```

### Single Demo Execution (`run_single_demo.py`)
Ran `python run_single_demo.py`:
- Map: $30\times 30$ Irregular Outdoor Map.
- Algorithm: Proposed Adaptive A*.
- Result: Planning Time = 0.92 ms, Path Length = 38.44 m, Expanded Nodes = 53, Corners = 1.
- Output: Generated figure saved to `results/figures/demo_30x30_main_proposed_adaptive_astar.png`.

---

## 4. Modified Files Summary

| File | Type | Description of Changes |
| :--- | :--- | :--- |
| `.gitignore` | Config | Added to ignore `__pycache__`, `*.pyc`, `*.pyo`, and IDE artifacts. |
| `src/smoother.py` | Implementation | Added `mode="multi_pass"` (default) and `mode="single_pass"` parameter to `smooth_path()`. |
| `src/astar.py` | Implementation | Added `smoothing_mode` parameter to `adaptive_astar()`, passing through to `smooth_path()`. |
| `tests/test_astar.py` | Tests | Added Test 10 (`start == goal`), Test 11 (Octile inequality), and Test 12 (collision freedom across smoothing modes). |
| `docs/assumptions.md` | Documentation | Added Octile distance derivation, dynamic weight inflation, permanent closed set analysis, and smoothing pass comparison. |
| `docs/viva_defense_guide.md` | Documentation | Updated Q2 (inadmissibility & suboptimality), Q4 (single vs multi-pass), and Q5 (Monte Carlo scaling). |
| `docs/final_audit_report.md` | Audit | Corrected F-01 (Table 1 vs Table 2), F-02 (suboptimality without $\epsilon$-admissibility claim), and marked all findings resolved. |
| `report/ieee_technical_report.md` | Academic Report | Added exact PDF citations (table, row, page), sample standard deviation notation ($s, N=10, \text{ddof}=1$), suboptimality trade-off analysis, and research limitations. |
| `docs/correction_log.md` | Documentation | This document: comprehensive record of all audit resolutions and verification results. |

---

## 5. Research Limitations & Future Directions

1. **Synthetic vs. Proprietary Maps:** Because the authors did not publish their raw MATLAB obstacle arrays, results reflect synthetic maps replicating the specified dimensions and obstacle distributions. While qualitative trends (62%–71% node reductions) align closely, exact bit-level node counts on $100\times 100$ reflect differences in corridor layouts.
2. **Suboptimality vs. Efficiency Trade-off:** The algorithm intentionally sacrifices theoretical shortest-path guarantees for speed. On 8-connected grids, users requiring strictly optimal paths should deploy Baseline A* with Octile distance, whereas real-time applications benefit from Adaptive A*'s faster planning.
3. **Continuous Kinematics:** The algorithm produces discrete 2D waypoint paths; hardware deployment on physical mobile robots requires continuous trajectory smoothing (e.g., cubic B-splines or quintic polynomials) and kinematic controller tracking.
