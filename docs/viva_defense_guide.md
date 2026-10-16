# Viva Voce Defense Guide: Questions, Technical Justifications & Key Insights

This guide prepares you for the oral examination (Viva Voce) by providing technically grounded answers to anticipated examiner questions.

---

### Core Questions & Answers

#### Q1: Why did you choose this specific research article?
* **Answer:**  
  *"The selection strictly adhered to the assignment's Original Implementation Requirement, which mandates choosing a paper whose source code is not publicly available to prevent plagiarism and ensure independent implementation. Other candidates (such as deep feature selectors or timetabling genetic algorithms) have public repositories on GitHub and Zenodo. In contrast, Cao et al. (MDPI Electronics 2026) published no source code or obstacle matrices. Furthermore, its modular 3-stage architecture (adaptive heuristic, distance model optimization, and redundant point deletion) allowed for rigorous ablation studies and clear mathematical reproduction."*

---

#### Q2: How does the Adaptive Estimation Function work mathematically, and is it admissible?
* **Answer:**  
  *"The standard evaluation function is modified to $f(n) = g(n) + \omega(n) \cdot h(n)$, where $\omega(n) = \ln(1 + e^{d/D})$. Here, $d$ is the Euclidean distance from the current node to the goal, and $D$ is the initial start-to-goal distance.*  
  *At the beginning of search ($d \approx D$), $d/D = 1$, yielding $\omega \approx \ln(1 + e) \approx 1.313$. As the robot approaches the destination ($d \to 0$), $d/D \to 0$, causing $\omega \to \ln(2) \approx 0.693$.*  
  *Crucially, the heuristic is **mathematically inadmissible** early in the search for two reasons: (1) $\omega(n) > 1.0$ whenever $d/D > 0.5413$; and (2) the hybrid distance model $h_{\text{opt}}(n)$ overestimates true 8-connected Octile distance by up to $20.71\%$ along diagonal directions ($\Delta x = \Delta y$). Because closed nodes are permanently closed without reopening, the algorithm operates as a **dynamically weighted, potentially suboptimal heuristic search**—trading theoretical shortest-path guarantees for dramatic node reductions and planning speed. We empirically demonstrated this on 100 random grids, finding that raw Adaptive A* produced slightly longer paths in 20% of cases before smoothing."*

---

#### Q3: Why did the authors combine Euclidean and Manhattan distances in the Distance Model?
* **Answer:**  
  *"In 8-connected grid maps, neither metric is ideal in isolation. Euclidean distance accurately measures straight-line displacement but requires square root calculations and can create estimation deviations on discrete grids. Manhattan distance measures 4-directional grid steps and can significantly overestimate distances when diagonal movement is permitted. By taking their arithmetic mean:
  $$h(n) = \frac{\sqrt{\Delta x^2 + \Delta y^2} + (|\Delta x| + |\Delta y|)}{2}$$
  the heuristic balances directional guidance with discrete grid movement costs, reducing invalid node exploration without excessive computational overhead."*

---

#### Q4: What is the Redundant Point Deletion strategy, and how do single-pass and multi-pass differ?
* **Answer:**  
  *"The paper introduces a 3-node sliding window smoothing rule evaluated across triplets $(p_i, p_{i+1}, p_{i+2})$:*  
  *1. Check if $p_i, p_{i+1}, p_{i+2}$ are collinear. If collinear and obstacle-free, eliminate $p_{i+1}$.*  
  *2. If not collinear (Step 3), check whether the direct connection line $p_i \to p_{i+2}$ intersects an obstacle. If obstacle-free, eliminate intermediate node $p_{i+1}$ (corner shortcutting). If blocked, retain $p_{i+1}$ and advance.*  
  *Regarding Step 4, we evaluated both interpretations:*  
  *- **Single-Pass:** Evaluates the initial path sequence once, producing **3 corners** on $30 \times 30$ and **9 corners** on $60 \times 60$, which matches very closely with the published paper's **7 corners** in Table 2 and **8 corners** in Table 3.*  
  *- **Multi-Pass (Default):** Iterates until convergence (up to 5 passes), chaining shortcuts across open spaces down to 1–2 corners.*  
  *Both modes were verified using Bresenham line checks to be 100% collision-free."*

---

#### Q5: Did your implementation produce exact numerical matches with the published results?
* **Answer (Critical Viva Talking Point):**  
  *"No, and claiming exact numerical equivalence would be scientifically unsound because the original paper did not publish the MATLAB random seeds or binary obstacle matrices for the three environment maps. We independently generated deterministic synthetic maps matching the descriptive characteristics (irregular outdoor, indoor maze, dense warehouse arrays).*  
  *While absolute numbers depend on obstacle placement, our implementation fully reproduced the **relative quantitative and qualitative trends** reported in the paper:*  
  * *Search nodes were reduced by **67.9%** on $30 \times 30$, **71.2%** on $60 \times 60$, and **62.0%** on $100 \times 100$ (paper reported $72.3\%$, $62.6\%$, and $94.8\%$).*  
  * *Corner turns were reduced by **81.8% to 89.9%** in multi-pass and **47% to 66%** in single-pass.*  
  * *Path length was consistently shortened by $1.5\%$ to $5.1\%$.*  
  * *Planning time was reduced by up to an order of magnitude."*

---

#### Q6: Why did your Python implementation run significantly faster than the paper's MATLAB reported runtimes?
* **Answer:**  
  *"In our experiments, planning times were on the order of 1–10 ms, whereas the paper reported 10–700 ms. This difference is explained by two technical factors:*
  *1. **Priority Queue Architecture:** We used Python's C-accelerated binary min-heap (`heapq`) with $O(\log N)$ push/pop operations, whereas standard MATLAB implementations frequently use table sorting or linear array searches which scale as $O(N)$ or $O(N \log N)$.*
  *2. **Hardware & Measurement Scope:** The paper ran on an Intel Core i5-1340P inside MATLAB R2023b. We measured purely the core search loop using `time.perf_counter()`, strictly excluding map generation, file I/O, and plot rendering."*

---

#### Q7: What did the Ablation Study demonstrate?
* **Answer:**  
  *"Our ablation study (matching Table 1 of the paper) clearly isolated the contribution of each individual module:*
  * *The **Adaptive Estimation Function** alone reduced node expansion by $\sim 40\%$ without altering path length.*
  * *The **Distance Model Optimization** dramatically focused the search beam toward the target, yielding the lowest node count during search.*
  * *The **Redundant Point Deletion** alone was solely responsible for reducing corner count (from 9 down to 0 on $30 \times 30$, and 13 down to 3 on $60 \times 60$) and shortening total length by cutting diagonal corners.*
  * *Combining all three into the **Full Proposed Adaptive $A^*$** achieved the optimal synergy of lowest runtime, minimum node expansion, shortest path, and smoothest trajectory."*

---

#### Q8: What ambiguities or errors did you discover in the original paper?
* **Answer:**  
  *"We identified two notable issues:*
  *1. **Textual vs Mathematical Inconsistency (Page 7):** The introductory text claims the heuristic weight depends on the ratio of 'distance to start' to 'distance to goal', but Equation 6 and the subsequent derivations correctly define $d$ as distance to goal over $D$ (initial start-to-goal distance). We adhered to the mathematical formula.*
  *2. **Underspecified Distance Model Inside $\omega(n)$:** The paper does not clarify whether $d$ and $D$ are computed using Euclidean distance or the proposed arithmetic mean. We adopted Euclidean distance to maintain a normalized ratio $d/D \in [0, 1]$."*
