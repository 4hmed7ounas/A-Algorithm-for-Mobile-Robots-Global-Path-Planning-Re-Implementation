# Implementation Assumptions and Methodological Deviations

This document explicitly specifies all assumptions, design decisions, coordinate conventions, and technical approximations adopted during the independent re-implementation of:

> Haixiao Cao, Zijian Guo, Yonghong Zhang, Zhuheng Lu, and Liang Jiang,  
> *"An Adaptive A\* Algorithm for Mobile Robots Global Path Planning"*,  
> *MDPI Electronics*, vol. 15, no. 13, art. 2807, 2026.

---

### 1. Coordinate System Mapping (1-Based vs 0-Based)
* **Paper Convention:** The original research was conducted in MATLAB R2023b, which uses 1-based indexing. The stated coordinates are:
  - $30 \times 30$: Start $(2, 2)$, Goal $(28, 28)$; Reversed $(28, 28) \to (2, 2)$; Random $(4, 24) \to (29, 2)$.
  - $60 \times 60$: Start $(2, 2)$, Goal $(58, 58)$; Reversed $(58, 58) \to (2, 2)$; Random $(4, 54) \to (59, 2)$.
  - $100 \times 100$: Start $(2, 2)$, Goal $(99, 99)$.
* **Implementation Decision:** Python utilizes 0-based array indexing. All paper coordinates are strictly transformed at the API boundary:
  $$(x_{0\text{-based}}, y_{0\text{-based}}) = (x_{\text{paper}} - 1, y_{\text{paper}} - 1)$$
  No ad-hoc manual coordinate shifting is applied internally.

---

### 2. Grid Connectivity and Edge Costs
* **Paper Text:** Section 3.2 notes that the distance model *"can be applied in maps with four directions, or in an eight-directional environment map"*. Figures 5, 8–12 clearly show diagonal motion segments.
* **Assumption:** The grid operates under **8-neighbor connectivity**.
* **Movement Cost:**
  - Orthogonal movements (horizontal/vertical): $c_{\text{ortho}} = 1.0\,\text{m}$.
  - Diagonal movements: $c_{\text{diag}} = \sqrt{2} \approx 1.4142\,\text{m}$.

---

### 3. Corner-Cutting Clearance Rule
* **Paper Text:** The paper does not explicitly detail corner clearance rules when moving diagonally past obstacles.
* **Assumption:** To prevent physical collisions where a robot body would clip between two touching obstacle corners, a diagonal step from $(x, y)$ to $(x + \Delta x, y + \Delta y)$ is valid if and only if:
  1. The destination cell $(x + \Delta x, y + \Delta y)$ is free.
  2. The robot does not pass through two diagonally touching obstacle corners (i.e. $(x + \Delta x, y)$ and $(x, y + \Delta y)$ cannot both be blocked).

---

### 4. Distance Metrics Inside the Adaptive Weight $\omega(n)$ and Heuristic Admissibility
* **Paper Formulation (Eq. 6):**
  $$\omega(n) = \ln\left(1 + e^{\frac{d}{D}}\right)$$
  The paper defines $d$ as *"distance between current node and target node"* and $D$ as *"distance between starting node and target node"*, but does not clarify whether $d$ and $D$ use Euclidean distance or the newly proposed arithmetic mean distance.
* **Implementation Decision:** Standard Euclidean distance is utilized for $d$ and $D$. This ensures that at the start $d = D \implies d/D = 1.0$, producing a clean, bounded ratio $d/D \in [0, 1]$. Using the arithmetic mean could artificially skew the ratio due to grid orientation effects.
* **Theoretical Admissibility Analysis under 8-Connected Movement:**
  Under 8-connected grid movement with orthogonal edge cost $1.0$ and diagonal edge cost $\sqrt{2}$, the true shortest obstacle-free distance is the **Octile Distance**:
  $$h^*(n) = (\sqrt{2} - 1)\min(\Delta x, \Delta y) + \max(\Delta x, \Delta y)$$
  - Euclidean distance $h_{\text{euclid}}(n) = \sqrt{\Delta x^2 + \Delta y^2} \le h^*(n)$ for all $\Delta x, \Delta y \ge 0$, and is therefore strictly admissible and consistent.
  - The proposed distance model $h_{\text{opt}}(n) = \frac{h_{\text{euclid}}(n) + h_{\text{manhattan}}(n)}{2}$ overestimates true Octile distance along diagonal directions where $\Delta x = \Delta y$:
    $$h_{\text{opt}}(n) = \frac{\sqrt{2}\Delta x + 2\Delta x}{2} \approx 1.7071 \Delta x > 1.4142 \Delta x = h^*(n)$$
    This represents an overestimation of up to **20.71%** over true cost.
  - Furthermore, the dynamic weight $\omega(n) = \ln(1 + e^{d/D}) > 1.0$ whenever $d/D > \ln(e - 1) \approx 0.5413$, peaking at $\omega \approx 1.31326$ when $d = D$.
  - Combined with the permanent closure of evaluated nodes without reopening (`if neighbor in closed_set: continue`, per Algorithm 1 line 11), the algorithm operates as a **dynamically weighted, potentially suboptimal heuristic search**. It trades formal shortest-path optimality guarantees for aggressive goal-directed expansion speed and node reduction.
  - *Empirical Note:* An isolated test on 100 random $20 \times 20$ obstacle grids confirmed that before smoothing, raw Adaptive A* returned a longer path than Baseline A* in 20 of the 100 tested configurations. This demonstrates potential suboptimality in those specific scenarios; it does not constitute a universal failure rate or imply an unproven $\epsilon$-suboptimality bound.

---

### 5. Resolution of Textual Ambiguity in Heuristic Weight Description
* **Paper Text (Page 7):** Mentions *"the weight of the function changes dynamically based on the ratio of the distance between the current node and the starting point to the distance to the destination"*.
* **Mathematical Definition (Eq. 6):**
  $$\omega(n) = \ln\left(1 + e^{\frac{d}{D}}\right), \quad d = \text{dist}(n, \text{goal}), \quad D = \text{dist}(\text{start}, \text{goal})$$
* **Resolution:** The mathematical formula is the authoritative definition. At the start of the search, $d = D \implies \omega \approx 1.313$ (strong goal bias). Near the goal, $d \to 0 \implies \omega \to 0.693$ (giving dominance to actual cost $g(n)$). The introductory English sentence contained a typographical inversion.

---

### 6. Redundant Point Deletion: Single-Pass vs Multi-Pass Smoothing
* **Paper Specification (Section 3.3, Steps 1–4):**  
  The paper specifies a 3-node sliding window check $(p_i, p_{i+1}, p_{i+2})$ evaluating collinearity and obstacle intersection across connecting lines $p_i \to p_{i+2}$. Step 4 states: *"Inspect all the nodes in the path node set and eliminate all superfluous nodes from the path to link the remaining path nodes to form a new path."*
* **Implementation Interpretations:**
  - **Single-Pass (`mode="single_pass"`):** Executes exactly one sequential sweep across consecutive triplets of the initial path. On our benchmark maps, single-pass produces **3 corners** on $30 \times 30$ and **9 corners** on $60 \times 60$, which aligns closely with the published paper's reported values (**7 corners** in Table 2 for $30 \times 30$, and **8 corners** in Table 3 for $60 \times 60$).
  - **Multi-Pass (`mode="multi_pass"`, default):** Iteratively applies the 3-node elimination until convergence (up to 5 passes). This allows newly joined shortcut vertices to be re-evaluated across open spaces, eliminating virtually all intermediate stair-stepping down to 1 corner on $30 \times 30$ and 2 corners on $60 \times 60$.
  - Both modes are fully implemented, configurable in `delete_redundant_points(mode="...")`, and verified to be 100% collision-free. The default `multi_pass` is retained to preserve existing benchmark output.

---

### 7. Definition of Expanded Nodes
* **Paper Metric:** "Expanded nodes" / "traversed nodes".
* **Implementation Decision:** A node is counted as expanded if and only if it is removed from the priority queue (`heapq.heappop`) and evaluated as the `current` search state. Nodes that are merely generated as tentative neighbors and pushed to the Open List are not counted as expanded until popped.

---

### 8. Definition of Corner Turn ($\ge 45^\circ$)
* **Paper Metric:** "Number of corners with angle $\ge 45^\circ$".
* **Implementation Decision:** For three consecutive path points $(p_{k-1}, p_k, p_{k+1})$, the turning angle $\theta$ between the incoming vector $\vec{v}_1 = p_k - p_{k-1}$ and outgoing vector $\vec{v}_2 = p_{k+1} - p_k$ is computed via:
  $$\cos \theta = \frac{\vec{v}_1 \cdot \vec{v}_2}{\|\vec{v}_1\| \|\vec{v}_2\|}, \quad \theta = \arccos(\text{clip}(\cos \theta, -1.0, 1.0))$$
  If $\theta \ge 44.99^\circ$, it is counted as a corner.

---

### 9. Synthetic Map Environments
* **Paper Status:** The original MATLAB matrices/seeds are unpublished.
* **Implementation Decision:** Deterministic procedurally generated maps matching the exact structural descriptions and densities (30x30 irregular outdoor, 60x60 structured maze, 100x100 array blocks) were generated using fixed seeds (`seed=3030`, `seed=6060`, `seed=100100`) and saved to `results/maps/`.
